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
import sys

import ping
import urllib2
import smtplib
import ftplib
import shutil
import telnetlib
import paramiko
import xmpp


class ping_gen():
    '''
    ping generator
    sends a number of ICMP-PING messages to a destination. the pings are
    delayed by n seconds (default = 1 second)
    '''
    __generator__ = 'ping'

    def __init__(self,
                 params):
        self._host = params[0]
        self._num = params[1]
        self._delay = 1

        if len(params) == 3:
            self._delay = params[2]

    def __call__(self):
        logging.getLogger(self.__generator__).info("Sending %s PING messages to %s (delay: %s)",
                                                   self._num,
                                                   self._host,
                                                   self._delay)

        for _ in range(self._num):
            if ping.do_one(dest_addr = self._host,
                           timeout = 5,
                           psize = 64) is not None:
                logging.getLogger(self.__generator__).debug("Got PONG from %s",
                                                            self._host)

            else:
                logging.getLogger(self.__generator__).debug("No response from %s",
                                                            self._host)

            time.sleep(self._delay)

class http_gen():
    '''
    http and https generator
    send HTTP GET requests to a webserver to retrieve a given URL n times.
    delay the requests by a random time controlled by a multiplier. 
    to get best results with this generator, the size of the http answers 
    should differ (send random data)
    '''
    __generator__ = 'http'

    def __init__(self,
                 params):
        self._urls = params[0]
        self._num = params[1]
        self._multiplier = 5

        if len(params) == 3:
            self._multiplier = params[2]

    def __call__(self):
        for _ in range(self._num):
            url = self._urls[random.randint(0, (len(self._urls) - 1))]
            logging.getLogger(self.__generator__).info("Requesting: %s", url)

            try:
                for __ in range(int(random.random() * 10 + 1)):
                  response = urllib2.urlopen(url)
                  logging.getLogger(self.__generator__).debug("Recieved %s bytes from %s",
                                                              str(len(response.read())),
                                                              url)

            except:
                logging.getLogger(self.__generator__).debug("Failed to request %s",
                                                            url)

            time.sleep(random.random() * self._multiplier)

class smtp_gen():
    '''
    smtp generator
    connect to an smtp server and send an email containing a random length
    string to a destination email address.
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
        rnd = ''.join(random.choice(string.letters) for _ in xrange(int(3000 * random.random())))

        msg = "From: " + self._from + "\r\n" \
            + "To: " + self._to + "\r\n" \
            + "Subject: PyTgen " + str(datetime.datetime.now()) + "\r\n\r\n" \
            + rnd + "\r\n"

        logging.getLogger(self.__generator__).info("Sending email to %s (size: %s)",
                                                   self._host,
                                                   len(rnd))

        try:
            sender = smtplib.SMTP(self._host, 25)

            try:
                logging.getLogger(self.__generator__).debug("Using TLS")
                sender.starttls()

            except:
                pass

            try:
                sender.login(self._user, self._pass)

            except smtplib.SMTPAuthenticationError:
                logging.getLogger(self.__generator__).debug("Using PLAIN auth")
                sender.docmd("AUTH LOGIN", base64.b64encode(self._user))
                sender.docmd(base64.b64encode(self._pass), "")

            sender.sendmail(self._from, self._to, msg)
            logging.getLogger(self.__generator__).debug("Email sent successful")

        except:
            raise

        else:
            sender.quit()

class ftp_gen():
    '''
    ftp and ftp_tls generator
    connect to a host using ftp and start uploading and downloading files. 
    The files to be put or retrieved are specified in an array and are
    randomly choosen. An empty array will skip upload or download.
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
        self._multiplier = 5

        if len(params) == 7:
            self._multiplier = params[6]

    def __call__(self):
        ftp = None
        if self._tls == True:
            logging.getLogger(self.__generator__).info("Connecting to ftps://%s",
                                                       self._host)
            try:
                # 20% chanche to login with a wrong password at first try
                if random.random() > 0.8:
                    try:
                        logging.getLogger(self.__generator__).debug("Logging in with wrong credentials")
                        ftp = ftplib.FTP_TLS(self._host,
                                             self._user,
                                             "wrongpass")
                    except:
                        pass

                    time.sleep(2 * random.random())

                ftp = ftplib.FTP_TLS(self._host,
                                     self._user,
                                     self._pass)
                ftp.prot_p()

            except:
                logging.getLogger(self.__generator__).debug("Error connecting to ftps://%s",
                                                            self._host)

        else:
            logging.getLogger(self.__generator__).info("Connecting to ftp://%s",
                                                       self._host)
            try:
                # 20% chanche to login with a wrong password at first try
                if random.random() > 0.8:
                    try:
                        logging.getLogger(self.__generator__).debug("Logging in with wrong credentials")
                        ftp = ftplib.FTP(self._host,
                                         self._user,
                                         "wrongpass")
                    except:
                        pass

                    time.sleep(2 * random.random())

                ftp = ftplib.FTP(self._host,
                                 self._user,
                                 self._pass)

            except:
                logging.getLogger(self.__generator__).debug("Error connecting to ftp://%s",
                                                            self._host)

        if ftp is not None:
            ftp.retrlines('LIST')

            for _ in xrange(self._num):
                if len(self._put) is not 0:
                    ressource = self._put[random.randint(0, (len(self._put) - 1))]
                    (path, filename) = os.path.split(ressource)

                    logging.getLogger(self.__generator__).debug("Uploading %s",
                                                                ressource)

                    f = open(ressource, 'r')
                    ftp.storbinary("STOR " + filename, f)
                    f.close()

                time.sleep(self._multiplier * random.random())

                if len(self._get) is not 0:
                    ressource = self._get[random.randint(0, (len(self._get) - 1))]

                    logging.getLogger(self.__generator__).debug("Downloading %s",
                                                                ressource)

                    ftp.retrbinary('RETR ' + ressource, self._getfile)

                time.sleep(self._multiplier * random.random())

            ftp.quit()

    def _getfile(self,
                 ressource):
        pass

class copy_gen():
    '''
    copy generator.
    copy files or directories from a source to a destination. this generator
    can be used to generate traffic on network filesystems like nfs or smb.
    A random source file will be generated if the source parameter is set to
    "None". The size of the generated source file can be controlled by an 
    optional size parameter (default = 8192 byte)
    '''
    __generator__ = "copy"

    def __init__(self,
                 params):
        self._src = params[0]
        self._dst = params[1]
        self._size = 8192

        if len(params) == 3:
            self._size = params[2] * 1024

    def __call__(self):
        if self._src is not None:
            logging.getLogger(self.__generator__).info("Copying from %s to %s",
                                                       self._src,
                                                       self._dst)

            if os.path.isdir(self._src):
                dst = self._dst + "/" + self._src

                if os.path.exists(dst):
                    logging.getLogger(self.__generator__).debug("Destination %s exists. Deleting it.",
                                                                dst)
                    shutil.rmtree(dst)

                try:
                    shutil.copytree(self._src, dst)
                except:
                    logging.getLogger(self.__generator__).debug("Error copying %s to %s",
                                                                self._src,
                                                                dst)

            else:
                try:
                    shutil.copy2(self._src, self._dst)
                except:
                    logging.getLogger(self.__generator__).debug("Error copying %s to %s",
                                                                self._src,
                                                                self._dst)

        else:
            if (not os.path.exists(self._dst)) or (os.path.isfile(self._dst)):
                rnd = ''.join(random.choice(string.letters) for _ in xrange(int(self._size * random.random())))

                logging.getLogger(self.__generator__).info("Writing %s byte to %s",
                                                           len(rnd),
                                                           self._dst)

                try:
                    f = open(self._dst, "w")
                    f.write(rnd)

                except:
                    logging.getLogger(self.__generator__).debug("Error writing to %s",
                                                                self._dst)

                else:
                    f.close()

            else:
                logging.getLogger(self.__generator__).info("Destination %s is not a file",
                                                           self._dst)


class telnet_gen():
    '''
    telnet generator.
    connect to a host using telnet and start sending commands to the host. The 
    connection will be kept open until the connection time provided in the 
    config is over. If the commands array is empty, the connection will idle 
    until connection time is over.
    '''
    __generator__ = "telnet"

    def __init__(self,
                 params):
        self._host = params[0]
        self._port = params[1]
        self._user = params[2]
        self._pass = params[3]
        self._time = params[4]
        self._cmds = params[5]
        self._prompt = params[6]
        self._multiplier = 60

        if len(params) == 8:
            self._multiplier = params[7]

    def __call__(self):
        logging.getLogger(self.__generator__).info("Connecting to %s",
                                                   self._host)

        realmin = self._time * 2 * random.random()
        endtime = datetime.datetime.now() + datetime.timedelta(minutes = realmin)

        try:
            tn = telnetlib.Telnet(self._host, self._port)

            try:
                tn.read_until("login: ")
                tn.write(self._user + "\n")
                if self._pass is not None:
                    tn.read_until("Password: ")
                    tn.write(self._pass + "\n")

            except:
                logging.getLogger(self.__generator__).debug("Error logging in")

        except:
            logging.getLogger(self.__generator__).debug("Error connecting to %s",
                                                        self._host)

        else:
            while datetime.datetime.now() < endtime:
                if len(self._cmds) is not 0:
                    self._send_cmds(tn)

                else:
                    time.sleep(realmin)
                    break

                time.sleep(self._multiplier * random.random())

            tn.write("exit\n")
            tn.read_all()

    def _send_cmds(self,
                   tn):
        for _ in xrange(int(6 * random.random())):
            cmd = self._cmds[random.randint(0, (len(self._cmds) - 1))]
            logging.getLogger(self.__generator__).debug("Sending command: %s",
                                                        cmd)
            tn.read_very_eager()
            tn.write(cmd + '\n')
            tn.read_eager()
            time.sleep(5 * random.random())

class ssh_gen():
    '''
    ssh generator.
    connect to a host using ssh and start sending commands to the host. The 
    connection will be kept open until the connection time provided in the 
    config is over. If the commands array is empty, the connection will idle 
    until connection time is over.
    '''
    __generator__ = "ssh"

    def __init__(self,
                 params):
        self._host = params[0]
        self._port = params[1]
        self._user = params[2]
        self._pass = params[3]
        self._time = params[4]
        self._cmds = params[5]
        self._multiplier = 60

        if len(params) == 7:
            self._multiplier = params[6]

    def __call__(self):
        logging.getLogger("paramiko").setLevel(logging.INFO)
        logging.getLogger(self.__generator__).info("Connecting to %s",
                                                   self._host)

        realmin = self._time * 2 * random.random()
        endtime = datetime.datetime.now() + datetime.timedelta(minutes = realmin)

        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # 20% chanche to login with a wrong password at first try
            if random.random() > 0.8:
                try:
                    client.connect(self._host,
                                   self._port,
                                   self._user,
                                   "wrongpass")
                except:
                    pass

                time.sleep(2 * random.random())

            client.connect(self._host,
                           self._port,
                           self._user,
                           self._pass)

        except:
            logging.getLogger(self.__generator__).debug("Error connecting to %s",
                                                        self._host)

        else:
            while datetime.datetime.now() < endtime:
                if len(self._cmds) is not 0:
                    self._send_cmds(client)

                else:
                    time.sleep(realmin)
                    break

                time.sleep(self._multiplier * random.random())

            client.close()

    def _send_cmds(self,
                   client):
        for _ in xrange(3):
            cmd = self._cmds[random.randint(0, (len(self._cmds) - 1))]
            logging.getLogger(self.__generator__).debug("Sending command: %s",
                                                        cmd)
            client.exec_command(cmd)
            time.sleep(5 * random.random())

class sftp_gen():
    '''
    sftp generator.
    this generator will connect to a host using ssh subsystem sftp. It then 
    starts sending uploading and downloading files provided via the _get and
    _put parameters.
    '''
    __generator__ = "sftp"

    def __init__(self,
                 params):
        self._host = params[0]
        self._port = params[1]
        self._user = params[2]
        self._pass = params[3]
        self._put = params[4]
        self._get = params[5]
        self._time = params[6]
        self._multiplier = 60

        if len(params) == 8:
            self._multiplier = params[7]

    def __call__(self):
        logging.getLogger("paramiko").setLevel(logging.INFO)
        logging.getLogger(self.__generator__).info("Connecting to %s", self._host)

        realmin = self._time * 2 * random.random()
        endtime = datetime.datetime.now() + datetime.timedelta(minutes = realmin)

        try:
            transport = paramiko.Transport((self._host,
                                            self._port))
            transport.connect(username = self._user,
                              password = self._pass)

            sftp = paramiko.SFTPClient.from_transport(transport)

        except:
            logging.getLogger(self.__generator__).debug("Error connecting to %s",
                                                        self._host)

        else:
            while datetime.datetime.now() < endtime:
                put = self._put
                get = self._get

                if len(put) is 0 and len(get) is 0:
                    time.sleep(realmin)
                    break

                while len(put) is not 0:
                    (src, dst) = put.pop(len(put) - 1)

                    logging.getLogger(self.__generator__).debug("Uploading %s to %s",
                                                                src, dst)
                    sftp.put(src, dst)
                    time.sleep(2 * random.random())

                while len(get) is not 0:
                    (src, dst) = get.pop(len(get) - 1)

                    logging.getLogger(self.__generator__).debug("Downloading %s to %s",
                                                                src, dst)
                    sftp.get(src, dst)
                    time.sleep(2 * random.random())

                time.sleep(self._multiplier * random.random())

            sftp.close()
            time.sleep(0.2)
            transport.close()

class xmpp_gen():
    '''
    xmpp generator.
    this generator will connect to a jabber/xmpp server and stay online for
    some time
    '''
    __generator__ = "xmpp"

    def __init__(self,
                 params):
        self._host = params[0]
        self._port = params[1]
        self._jid = params[2]
        self._pass = params[3]
        self._ressource = params[4]
        self._minutes = params[5]
        self._users = params[6]

    def __call__(self):
        def receive_callback(sess,
                             mess):
            pass

        jid = xmpp.protocol.JID(self._jid)
        client = xmpp.Client(jid.getDomain(), debug = [])

        logging.getLogger(self.__generator__).info('Connecting to %s',
                                                   self._host)

        realmin = self._minutes * 60 * 2 * random.random()
        endtime = datetime.datetime.now() + datetime.timedelta(minutes = realmin)

        if client.connect(server = (self._host, self._port), use_srv = False):
            if client.auth(jid.getNode(), self._pass, self._ressource):
                if client.isConnected():
                    client.RegisterHandler('message', receive_callback)
                    client.sendInitPresence()

                    while datetime.datetime.now() < endtime:
                        to_user = self._users[random.randint(0, (len(self._users) - 1))]
                        msg = ''.join(random.choice(string.letters) for _ in xrange(int(60 * random.random())))

                        message = xmpp.Message(to_user, msg)
                        message.setAttr('type', 'chat')
                        client.send(message)

                        if random.random() > 0.5:
                            time.sleep(30 * 60 * random.random())

                        time.sleep(20 * random.random())

                    client.disconnect()

                else:
                    logging.getLogger(self.__generator__).debug('Error authenticating')

        else:
            logging.getLogger(self.__generator__).debug("Error connecting to %s",
                                                        self._host)


class reboot_gen():
    '''
    reboot generator.
    this generator will initiate a system reboot on linux or windows machines.
    it is used to simulate system startups including dhcp requests, network
    filesystem mounts, ntp requests and so on.
    '''
    __generator__ = "reboot"

    def __init__(self,
                 params):
        self._platform = sys.platform

    def __call__(self):
        if self._platform == "linux2":
            logging.getLogger(self.__generator__).info("Rebooting %s ...",
                                                       self._platform)

            try:
                os.system('/sbin/shutdown -r now')

            except:
                logging.getLogger(self.__generator__).debug("Error calling shutdown")

        elif self._platform == "win32":
            logging.getLogger(self.__generator__).info("Rebooting %s ...",
                                                       self._platform)

            try:
                os.system('shutdown -r -t 1')

            except:
                logging.getLogger(self.__generator__).debug("Error calling shutdown")

        else:
            logging.getLogger(self.__generator__).info("Unknown Operating System: %s",
                                                       self._platform)
