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


#
# This is a default configuration for the SecMonet test network
#
class Conf(object):
    # maximum number of worker threads that can be used to execute the jobs.
    # the program will start using 3 threads and spawn new ones if needed.
    # this setting depends on the number of jobs that have to be executed
    # simultaneously (not the number of jobs given in the config file).
    maxthreads = 15

    # set to "logging.INFO" or "logging.DEBUG"
    loglevel = logging.DEBUG

    # ssh commands that will be randomly executed by the ssh traffic generator
    ssh_commands = ['ls', 'cd', 'cd /etc', 'ps ax', 'date', 'mount', 'free', 'vmstat',
                    'touch /tmp/tmpfile', 'rm /tmp/tmpfile', 'ls /tmp/tmpfile',
                    'tail /etc/hosts', 'tail /etc/passwd', 'tail /etc/fstab',
                    'cat /var/log/messages', 'cat /etc/group', 'cat /etc/mtab']

    # urls the http generator will randomly fetch from
    http_extern = ['http://web.extern.ndsec']
    http_intern = ['http://web.intern.ndsec']

    # a number of files that will randomly be used for ftp upload
    ftp_put = ['S:/share/files/file%s' % i for i in xrange(0, 9)]

    # a number of files that will randomly be used for ftp download
    ftp_get = ['~/files/file%s' % i for i in xrange(0, 9)]

    # array of source-destination tuples for sftp upload
    sftp_put = [('S:/share/files/file%s' % i, '/tmp/file%s' % i) for i in xrange(0, 9)]

    # array of source-destination tuples for sftp download
    sftp_get = [('/media/share/files/file%s' % i, 'S:/share/files/tmp/file%s' % i) for i in xrange(0, 9)]

    # significant part of the shell prompt to be able to recognize
    # the end of a telnet data transmission
    telnet_prompt = "$ "

    # job configuration (see config.example.py)
    jobdef = [
              # ping
              # ('ping_gen', [(10, 0), (15, 0), (240, 0)], ['telnet.intern.ndsec', 4]),
              # ('ping_gen', [(16, 0), (16, 30), (5, 0)], ['127.0.0.1', 4]),
              #
              # http (intern)
              ('http_gen', [(9, 0), (16, 30), (60, 0)], [http_intern, 2, 30]),
              ('http_gen', [(9, 55), (9, 30), (5, 0)], [http_intern, 5, 20]),
              # ('http_gen', [(12, 0), (12, 30), (2, 0)], [http_intern, 6, 10]),
              # ('http_gen', [(10, 50), (12, 0), (10, 0)], [http_intern, 2, 10]),
              ('http_gen', [(15, 0), (17, 30), (30, 0)], [http_intern, 8, 20]),
              #
              # http (extern)
              ('http_gen', [(12, 0), (12, 30), (5, 0)], [http_extern, 10, 20]),
              ('http_gen', [(9, 0), (17, 0), (30, 0)], [http_extern, 5, 30]),
              ('http_gen', [(9, 0), (12, 0), (60, 0)], [http_extern, 30, 30]),
              ('http_gen', [(9, 0), (17, 0), (90, 0)], [http_extern, 10, 30]),
              ('http_gen', [(12, 0), (12, 10), (5, 0)], [http_extern, 15, 20]),
              #
              # smtp
              ('smtp_gen', [(9, 0), (18, 0), (120, 0)], ['mail.extern.ndsec', 'mail2', 'mail', 'mail2@mail.extern.ndsec', 'mail52@mail.extern.ndsec']),
              ('smtp_gen', [(12, 0), (13, 0), (30, 0)], ['mail.extern.ndsec', 'mail2', 'mail', 'mail2@mail.extern.ndsec', 'mail51@mail.extern.ndsec']),
               #
              # ftp
              # ('ftp_gen', [(9, 0), (11, 0), (15, 0)], ['ftp.intern.ndsec', 'ndsec', 'ndsec', ftp_put, ftp_get, 10, False, 5]),
              # ('ftp_gen', [(10, 0), (18, 0), (135, 0)], ['ftp.intern.ndsec', 'ndsec', 'ndsec', ftp_put, [], 2, False]),
              #
              # nfs / smb
              # ('copy_gen', [(9, 0), (12, 0), (90, 0)], [None, 'Z:/tmp/dummyfile.txt', 30]),
              # ('copy_gen', [(10, 0), (16, 0), (120, 0)], [None, 'Z:/tmp/dummyfile.txt', 80]),
              # ('copy_gen', [(12, 0), (17, 0), (160, 0)], [None, 'Z:/tmp/dummyfile.txt', 180]),
              # ('copy_gen', [(9, 0), (18, 0), (0, 10)], ['file1', 'file2']),
              #
              # telnet
              # ('telnet_gen', [(9, 0), (18, 0), (60, 0)], ['telnet.intern.ndsec', None, 'ndsec', 'ndsec', 5, ssh_commands, telnet_prompt, 10]),
              ('telnet_gen', [(9, 0), (18, 0), (240, 0)], ['telnet.intern.ndsec', 23, 'ndsec', 'ndsec', 2, [], telnet_prompt]),
              # ('telnet_gen', [(16, 0), (18, 0), (120, 0)], ['telnet.intern.ndsec', 23, 'ndsec', 'wrongpass', 2, [], telnet_prompt]),
              #
              # ssh
              # ('ssh_gen', [(9, 0), (18, 0), (120, 0)], ['ssh.intern.ndsec', 22, 'ndsec', 'ndsec', 5, ssh_commands]),
              ('ssh_gen', [(9, 0), (18, 0), (240, 0)], ['ssh.intern.ndsec', 22, 'ndsec', 'ndsec', 30, [], 20]),
              # ('ssh_gen', [(9, 0), (18, 0), (120, 0)], ['192.168.10.50', 22, 'dummy1', 'dummy1', 5, ssh_commands]),
              # ('ssh_gen', [(12, 0), (14, 0), (120, 0)], ['ssh.intern.ndsec', 22, 'dummy1', 'wrongpass', 5, ssh_commands]),
              #
              # sftp
              # ('sftp_gen', [(17, 0), (18, 0), (60, 0)], ['127.0.0.1', 22, 'user', 'pass', sftp_put, sftp_get, 5, 1]),
              #
              # xmpp
              ('xmpp_gen', [(9, 0), (15, 0), (100, 0)], ['xmpp.intern.ndsec', 5222, 'xmpp12@xmpp.intern.ndsec', 'xmpp', 'xmpp12', 120, ['xmpp%s@xmpp.intern.ndsec' % i for i in xrange(1, 15)]]),
              #
              # reboot
              # ('reboot_gen', [(7, 50), (8, 0), (10, 0)], []),
              ('reboot_gen', [(9, 0), (9, 5), (5, 0)], [])
              ]
