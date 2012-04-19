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
import random
import datetime
import time
import base64
import string

import ping
import urllib2
import smtplib

class ping_gen():
    __name = 'ping'
    
    def __init__(self,
                 params):
        self.__host = params[0]
        self.__num = params[1]
        
    def __call__(self):
        for _ in range(self.__num):
            logging.getLogger(self.__name).debug("Pinging: %s", self.__host)
            if ping.do_one(dest_addr=self.__host,
                           timeout=5,
                           psize=64) is not None:
                logging.getLogger(self.__name).debug("Got PONG from %s", self.__host)

class http_gen():
    __name = 'http'
    
    def __init__(self, 
                 params):
        self.__url = params[0]
        self.__num = params[1]
        
    def __call__(self):
        for _ in range(self.__num):
            logging.getLogger(self.__name).debug("Requesting: %s", self.__url)
            response = urllib2.urlopen(self.__url)
            logging.getLogger(self.__name).debug("Recieved %s byte from %s", str(len(response.read())), self.__url)
            time.sleep(random.random() * 5)
    
class smtp_gen():
    __name = "smtp"
    
    def __init__(self,
                 params):
        self.__host = params[0]
        self.__user = params[1]
        self.__pass = params[2]
        self.__from = params[3]
        self.__to = params[4]
        
    def __call__(self):
        rnd = ''
        for _ in xrange(int(10000 * random.random())):
            rnd = rnd + random.choice(string.letters)
        
        msg = "From: " + self.__from + "\r\n" \
            + "To: " + self.__to + "\r\n" \
            + "Subject: PyTgen " + str(datetime.datetime.now()) + "\r\n\r\n" \
            + rnd + "\r\n"
        
        logging.getLogger(self.__name).debug("Connecting to %s", self.__host)
        
        try: 
            sender = smtplib.SMTP(self.__host, 25)
        
            try:
                sender.starttls()
            except:
                pass
            
            try:
                sender.login(self.__user, self.__pass)
            except smtplib.SMTPAuthenticationError:
                sender.docmd("AUTH LOGIN", base64.b64encode(self.__user))
                sender.docmd(base64.b64encode(self.__pass), "")
            
            sender.sendmail(self.__from, self.__to, msg)
            logging.getLogger(self.__name).debug("Sent mail via %s", self.__host)
                
        except:
            raise
        
        else:
            sender.quit()
