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
import os

import ping
import urllib2
import smtplib
import ftplib
import shutil
import paramiko


class ping_gen():
    '''
    ping generator
    '''
    __generator__ = 'ping'
    
    def __init__(self,
                 params):
        self._host = params[0]
        self._num = params[1]
        
    def __call__(self):
        for _ in range(self._num):
            logging.getLogger(self.__generator__).info("Pinging: %s", self._host)
            if ping.do_one(dest_addr=self._host,
                           timeout=5,
                           psize=64) is not None:
                logging.getLogger(self.__generator__).debug("Got PONG from %s", self._host)

class http_gen():
    '''
    http and https generator
    '''
    __generator__ = 'http'
    
    def __init__(self,
                 params):
        self._url = params[0]
        self._num = params[1]
        
    def __call__(self):
        for _ in range(self._num):
            logging.getLogger(self.__generator__).info("Requesting: %s", self._url)
            try:
                response = urllib2.urlopen(self._url)
                logging.getLogger(self.__generator__).debug("Recieved %s byte from %s", str(len(response.read())), self._url)

            except:
                logging.getLogger(self.__generator__).debug("Failed to request %s", self._url)

            time.sleep(random.random() * 5)    
    
class smtp_gen():
    '''
    smtp generator
    '''
    __generator__ = "smtp"
    
    def __init__(self,
                 params):
        self._host = params[0]
        self._user = params[1]
        self._pass = params[2]
        self._from = params[3]
        self._to = params[4]
        
    def __call__(self):
        rnd = ''
        for _ in xrange(int(10000 * random.random())):
            rnd = rnd + random.choice(string.letters)
        
        msg = "From: " + self._from + "\r\n" \
            + "To: " + self._to + "\r\n" \
            + "Subject: PyTgen " + str(datetime.datetime.now()) + "\r\n\r\n" \
            + rnd + "\r\n"
        
        logging.getLogger(self.__generator__).info("Connecting to %s", self._host)
        
        try: 
            sender = smtplib.SMTP(self._host, 25)
        
            try:
                sender.starttls()
            except:
                pass
            
            try:
                sender.login(self._user, self._pass)
            except smtplib.SMTPAuthenticationError:
                sender.docmd("AUTH LOGIN", base64.b64encode(self._user))
                sender.docmd(base64.b64encode(self._pass), "")
            
            sender.sendmail(self._from, self._to, msg)
            logging.getLogger(self.__generator__).debug("Sent mail via %s", self._host)
                
        except:
            raise
        
        else:
            sender.quit()

class ftp_gen():
    '''
    ftp and ftp_tls generator
    '''
    __generator__ = 'ftp'
    
    def __init__(self,
               params):
        self._host = params[0]
        self._user = params[1]
        self._pass = params[2]
        self._put = params[3]
        self._get = params[4]
        self._num = params[5]
        self._tls = params[6]
        
    def __call__(self):
        ftp = None
        if self._tls == True:
            logging.getLogger(self.__generator__).info("Connecting to ftps://%s", self._host)
            try:
                ftp = ftplib.FTP_TLS(self._host,
                                     self._user,
                                     self._pass)
                ftp.prot_p()
            except:
                logging.getLogger(self.__generator__).debug("Error connecting to ftps://%s", self._host)
            
        else:
            logging.getLogger(self.__generator__).info("Connecting to ftp://%s", self._host)
            try:
                ftp = ftplib.FTP(self._host,
                                 self._user,
                                 self._pass)
            except:
                logging.getLogger(self.__generator__).debug("Error connecting to ftp://%s", self._host)
        
        if ftp is not None:
            ftp.retrlines('LIST')
            
            for _ in xrange(self._num):
                if self._put is not None:
                    logging.getLogger(self.__generator__).debug("Uploading %s", self._put)
                    f = open("files/" + self._put, 'r')
                    ftp.storbinary("STOR " + self._put, f)
                    f.close()
                
                time.sleep(5 * random.random())   
                
                if self._get is not None:
                    logging.getLogger(self.__generator__).debug("Downloading %s", self._get)
                    ftp.retrbinary('RETR ' + self._get, self._getfile)
                    
                time.sleep(5 * random.random())
        
            ftp.quit()
        
    def _getfile(self,
                  file):
        pass

class copy_gen():
    __generator__ = "copy"
    
    def __init__(self,
                 params):
        self._src = params[0]
        self._dst = params[1]
        
    def __call__(self):
        logging.getLogger(self.__generator__).info("Copying from %s to %s", self._src, self._dst)
        
        if os.path.isdir(self._src):
            dst = self._dst + "/" + self._src
            
            if os.path.exists(dst):
                logging.getLogger(self.__generator__).debug("Destination %s exists. Deleting it.", dst)
                shutil.rmtree(dst)
                
            shutil.copytree(self._src, dst)
            
        else:
            shutil.copy2(self._src, self._dst)

class ssh_gen():
    __generator__ = "ssh"
    
    def __init__(self,
                 params):
        self._host = params[0]
        self._port = params[1]
        self._user = params[2]
        self._pass = params[3]
        self._time = params[4]
        self._cmds = params[5]

    def __call__(self):
        logging.getLogger(self.__generator__).info("Connecting to %s", self._host)
        
        endtime = datetime.datetime.now() + datetime.timedelta(minutes = self._time * 2 * random.random())
        
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            client.connect(self._host, 
                           self._port, 
                           self._user, 
                           self._pass)
            
        except:
            logging.getLogger(self.__generator__).debug("Error connecting to %s", self._host)
            
        else:
            # simulate some stupid work until requested connection time is over
            while datetime.datetime.now() < endtime:
                if len(self._cmds) is not 0:
                    self._send_cmds(client)
                time.sleep(30 * random.random())
            
            client.close()
        
    def _send_cmds(self,
                   client):
        client.exec_command(self._cmds[random.randint(0, (len(self._cmds) - 1))])
        time.sleep(5 * random.random())
        client.exec_command(self._cmds[random.randint(0, (len(self._cmds) - 1))])
        time.sleep(5 * random.random())
        client.exec_command(self._cmds[random.randint(0, (len(self._cmds) - 1))])
        
class sftp_gen():
    __generator__ = "sftp"
    
    def __init__(self,
                 params):
        self._host = params[0]
        self._port = params[1]
        self._user = params[2]
        self._pass = params[3]
        self._src = params[4]
        self._dst = params[5]

    def __call__(self):
        logging.getLogger(self.__generator__).info("Connecting to %s", self._host)
        
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self._host, 
                       self._port, 
                       self._user, 
                       self._pass)
        
        sftp = paramiko.SFTPClient(client.get_transport())
        #sftp.get(self._dst, self._src, self._getfile)
        #sftp.put(self._src, self._dst)
        
        client.close()
        
    def _getfile(self,
                  file):
        pass