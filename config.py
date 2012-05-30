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
    threads = 5
    
    loglevel = logging.DEBUG
    
#    jobdef = [('ping_gen', [(9, 0), (18, 0), (0, 5)], ['host', num]),
#              ('http_gen', [(9, 15), (10, 0), (10, 0)], ['host', num]),
#              ('smtp_gen', [(9, 0), (18, 0), (10, 0)], ['host', 'smtp_user', 'smtp_pass', 'mail_from', 'mail_to']),
#              ('ftp_gen', [(9, 0), (18, 0), (60, 0)], ['host', 'user', 'pass', 'file_put', 'file_get', num, ssl]),
#              ('copy_gen', [(9, 0), (18, 0), (0, 5)], ['src', dst]),
#              ('ssh_gen', [(9, 0), (18, 0), (0, 5)], ['host', 'user', 'pass']),
#              ('sftp_gen', [(9, 0), (18, 0), (0, 5)], ['host', 'user', 'pass', 'src', 'dst'])
#              ]
    
    #jobdef = [('ftp_gen', [(9, 0), (18, 0), 10], ['127.0.0.1', 'lain', 'lain', 'small.bin', 'small.bin', 2])]
    
    jobdef = [# ping
              #('ping_gen', [(9, 0), (18, 0), (60, 0)], ['127.0.0.1', 4]),
              #('ping_gen', [(16, 0), (16, 30), (5, 0)], ['127.0.0.1', 4]),
              # http
              #('http_gen', [(8, 50), (16, 30), (10, 0)], ['127.0.0.1', 1]),
              #('http_gen', [(9, 15), (10, 15), (10, 0)], ['127.0.0.1', 5]),
              #('http_gen', [(9, 15), (17, 15), (10, 0)], ['https://www.google.com', 2]),
              # smtp
              #('smtp_gen', [(9, 0), (18, 0), (10, 0)], ['host', 'smtp_user', 'smtp_pass', 'mail_from', 'mail_to']),
              # ftp
              #('ftp_gen', [(9, 0), (18, 0), (10, 0)], ['127.0.0.1', 'lain', 'lain', 'small.bin', 'small.bin', 2, False]),
              #('ftp_gen', [(9, 0), (18, 0), (10, 0)], ['127.0.0.1', 'lain', 'lain', 'small.bin', 'small.bin', 2, True]),
              #
              #('copy_gen', [(9, 0), (18, 0), (0, 10)], ['/home/reissmann/Dev/PyTgen/files/small.bin', '/tmp']),
              #('ssh_gen', [(9, 0), (18, 0), (0, 15)], ['127.0.0.1', 'xx', 'xx'])
              ]
