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
    
#    jobdef = [('ping_gen', [(9, 0), (18, 0), 5], ['host', num]),
#              ('http_gen', [(9, 15), (10, 0), 10], ['host', num]),
#              ('smtp_gen', [(9, 0), (18, 0), 10], ['host', 'smtp_user', 'smtp_pass', 'mail_from', 'mail_to'])
#              ]
    
    jobdef = []