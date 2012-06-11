'''
Copyright (c) 2012 Dustin Frisch <fooker@lab.sh>, 
                   Sven Reissmann <sven@0x80.io>

This file is part of the PyTgen traffic generator.

PyTgen is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyTgen is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyTgen. If not, see <http://www.gnu.org/licenses/>.
'''

import threading
import Queue
import logging

class worker(threading.Thread):
    def __init__(self,
                 name,
                 queue,
                 create,
                 destroy):
        threading.Thread.__init__(self)

        self.__name = name
        self.__queue = queue

        self.__create = create
        self.__destroy = destroy

        self.__dismissed = threading.Event()

        self.daemon = True
        self.name = self.__name

        self.start()

    def run(self):
        if self.__create:
            self.__create()

        logging.getLogger(self.__name).debug('main loop started')

        while True:
            if self.__dismissed.is_set():
                break

            try:
                action = self.__queue.get(block=True,
                                          timeout=10)

            except:
                continue

            else:
                try:
                    action()

                except:
                    raise

        logging.getLogger(self.__name).debug('main loop finished')

        if self.__destroy:
            self.__destroy()

    def dismiss(self):
        self.__dismissed.set()

class runner(object):
    def __init__(self,
                 maxthreads=10,
                 thread_create=None,
                 thread_destroy=None):
        self.__queue = Queue.Queue()
        self.__maxthreads = maxthreads

        logging.getLogger('runner').info('creating runner with 3 initial threads')

        self.__workers = []
        for i in xrange(0, 3):
            name = 'worker_%d' % i

            logging.getLogger('runner').debug('creating worker thread: %s',
                                              name)

            self.__workers.append(worker(name=name,
                                         queue=self.__queue,
                                         create=thread_create,
                                         destroy=thread_destroy))

    def __call__(self,
                 action):
        self.__queue.put(action)

        if (self.__queue.qsize() > 2):
            if (len(self.__workers) < self.__maxthreads):
                self._spawn()
            else:
                logging.getLogger('Runner').warning('Not enough worker threads to handle queue')

    def _spawn(self):
        name = 'worker_%d' % (len(self.__workers) + 1)
        logging.getLogger('Runner').info('spawning new worker thread: %s', name)
        self.__workers.append(worker(name=name,
                                     queue=self.__queue,
                                     create=None,
                                     destroy=None))

    def stop(self):
        for worker in self.__workers:
            worker.dismiss()

        for worker in self.__workers:
            worker.join()
