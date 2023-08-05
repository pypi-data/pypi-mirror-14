#!/usr/bin/python3

import socket
import threading
import time


class Client(object):
    def __init__(self, clientip="localhost", clientport=1336, serverip="84.200.52.231", serverport=1337):
        self.serverip = serverip
        self.serverport = serverport
        self.serveradr = (serverip, serverport)

        self.clientip = clientip

        if "localhost" in self.clientip or "127.0.0.1" in self.clientip:
            self.clientip = ""

        self.clientport = clientport
        self.clientadr = (self.clientip, self.clientport)

        self.udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.updatecount = 0    # How often has the Client sent an update?
        self.sleeptime = 1      # For how long should the client slepp until sending next update?
        self.stopsignal = False
        self.datalist = []      # List of messages the Client has received

    def __eq__(self, other):
        a_bool = self.clientadr == other.clientadr
        b_bool = self.serveradr == other.serveradr
        return a_bool == b_bool

    def _sendupdate(self):
        while not self.stopsignal:
            self.udpsock.sendto(b'_rc_', self.serveradr)
            self.updatecount += 1
            time.sleep(self.sleeptime)

    def send(self, message):
        self.udpsock.sendto(message, self.serveradr)

    def _rcv(self):
        while not self.stopsignal:
            try:

                data, adr = self.udpsock.recvfrom(1024)

                if adr == self.serveradr or adr == ("127.0.0.1", self.serverport):
                    if data == b'ping':
                        self.send(b'_pong_')
                    else:
                        self.datalist.append(data)

            except ConnectionError:
                exit()

    def start(self):
        self.udpsock.bind(self.clientadr)

        hellothread = threading.Thread(target=self._sendupdate)
        hellothread.start()

        rcvthread = threading.Thread(target=self._rcv)
        rcvthread.start()

    def stop(self):
        self.stopsignal = True


