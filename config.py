'''
Copyright (c) 2012 Sven Reissmann <sven@0x80.io>

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

import logging

class Conf(object):
    # maximum number of worker threads that can be used to execute the jobs.
    # the program will start using 3 threads and spawn new ones if needed.
    # this setting depends on the number of jobs that have to be executed
    # simultaneously (not the number of jobs given in the config file). 
    maxthreads = 10

    # set to "logging.INFO" or "logging.DEBUG"
    loglevel = logging.INFO

    # logfile location (None = log to console)
    logfile = "pytgen.log"

    # ssh commands that will be randomly executed by the ssh traffic generator
    ssh_commands = ['ls', 'cd', 'cd /etc', 'ps ax', 'date', 'mount', 'free', 'vmstat',
                    'touch /tmp/tmpfile', 'rm /tmp/tmpfile', 'ls /tmp/tmpfile',
                    'tail /etc/hosts', 'tail /etc/passwd', 'tail /etc/fstab',
                    'cat /var/log/messages', 'cat /etc/group', 'cat /etc/mtab']

    # a number of files that will randomly be used for ftp upload
    ftp_put = ['file1', 'file2', 'file3']

    # a number of files that will randomly be used for ftp download
    ftp_get = ['file1', 'file2', 'file3']

    # array of source-destination tuples for sftp upload
    sftp_put = [('file1', 'file1'),
                ('file2', 'file2'),
                ('file3', 'file3')
                ]

    # array of source-destination tuples for sftp download
    sftp_get = [('file1', 'file1'),
                ('file2', 'file2'),
                ('file3', 'file3')
                ]

    # job configuration (see config.example.py)
    jobdef = [# ping
              #('ping_gen', [(9, 0), (18, 0), (10, 0)], ['127.0.0.1', 5, 2]),
              #('ping_gen', [(16, 0), (16, 30), (5, 0)], ['127.0.0.1', 4]),
              #
              # http
              #('http_gen', [(8, 50), (16, 30), (10, 0)], ['http://127.0.0.1', 1, 10]),
              #('http_gen', [(9, 15), (17, 15), (10, 0)], ['https://www.google.com', 2]),
              #
              # smtp
              #('smtp_gen', [(9, 0), (18, 0), (10, 0)], ['host', 'smtp_user', 'smtp_pass', 'mail_from', 'mail_to']),
              #
              # ftp
              #('ftp_gen', [(9, 0), (18, 0), (1, 0)], ['127.0.0.1', 'user', 'pass', ftp_put, ftp_get, 10, False, 5]),
              #('ftp_gen', [(9, 0), (18, 0), (0, 10)], ['127.0.0.1', 'user', 'pass', ftp_put, [], 2, True]),
              #
              # nfs / smb
              #('copy_gen', [(9, 0), (18, 0), (0, 10)], [None, 'file1', 50]),
              #('copy_gen', [(9, 0), (18, 0), (0, 10)], ['file1', 'file2']),
              #
              # ssh
              #('ssh_gen', [(9, 0), (18, 0), (120, 0)], ['127.0.0.1', 22, 'user', 'pass', 5, ssh_commands]),
              #('ssh_gen', [(9, 0), (18, 0), (240, 0)], ['127.0.0.1', 22, 'user', 'pass', 30, []]),
              #
              # sftp
              #('sftp_gen', [(17, 0), (18, 0), (60, 0)], ['127.0.0.1', 22, 'user', 'pass', sftp_put, sftp_get]),
              #
              # reboot
              #('reboot_gen', [(9, 0), (18, 0), (0, 10)], [])
              ]
