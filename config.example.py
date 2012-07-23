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

# example job definition
#
#    jobdef = [('ping_gen', [(h, m), (h, m), (m, s)], ['host', count [, delay]]),
#              ('http_gen', [(h, m), (h, m), (m, s)], ['url', count [, delay]]),
#              ('smtp_gen', [(h, m), (h, m), (m, s)], ['host', 'smtp_user', 'smtp_pass', 'mail_from', 'mail_to']),
#              ('ftp_gen', [(h, m), (h, m), (m, s)], ['host', 'user', 'pass', [put], [get], count, ssl [, delay]]),
#              ('copy_gen', [(h, m), (h, m), (m, s)], ['src', dst]),
#              ('ssh_gen', [(h, m), (h, m), (m, s)], ['host', port, 'user', 'pass', minutes, commands]),
#              ('sftp_gen', [(h, m), (h, m), (m, s)], ['host', port, 'user', 'pass', [put], [get]),
#              ('reboot_gen', [(h, m), (h, m), (m, s)], [])
#              ]


# regular configuration format for each job
#
# ('generator_name', [(start_hour, start_min), (end_hour, end_min), (freq_min, freq_sec)], [parameters])


# parameters for each monitor
#
# ping_gen
#   - host      hostname or ip adress to ping
#   - count     number of ping packets to send
#   - [delay]   delay between sending in seconds (optional, default = 1)
#
# http_gen
#   - url       url to fetch (http://x.y.z or https://x.y.z)
#   - count     number of requests to send
#   - [delay]   multiplier to the random delay between requests in seconds (optional, default = 5)
#
# smtp_gen
#   - host      hostname or ip adress
#   - smtp_user username to authenticate with
#   - smtp_pass password to authenticate with
#   - mail_from sender email address
#   - mail_to   recipient email adress
#
# ftp_gen
#    - host     host or ip address to connect to
#    - user     username to authenticate with
#    - pass     password to authenticate with
#    - file_put array of files to upload to the server ([] to skip upload)
#    - file_get array of files to download from server ([] to skip download)
#    - count    number of downloads/uploads of the files
#    - ssl      True to connect with ssl, otherwise False
#    - [delay]  multiplier to the random delay between requests in seconds (optional, default = 5)
#
# copy_gen
#    - src      file or directory to copy ("None" to generate a file with random content)
#    - dst      destination to copy to
#    - size     the size of a randomly generated file (used in combination with src = None)
#
# ssh_gen
#    - host     host or ip to connect to
#    - port     port to connect to
#    - user     username to authenticate woith
#    - pass     password to authenticate with
#    - minutes  time the connection should be active in minutes
#    - commands array with commands to execute (or empty array to just idle)
#
# sftp_gen
#    - host     host or ip to connect to
#    - port     port to connect to
#    - user     username to authenticate woith
#    - pass     password to authenticate with
#    - src      file to copy
#    - dst      destination to copy to
#
# reboot_gen
#    - no parameters
