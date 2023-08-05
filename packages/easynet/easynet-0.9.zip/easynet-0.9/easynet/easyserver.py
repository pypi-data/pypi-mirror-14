#!/usr/bin/python3

import socket
import threading
import time


class Slave(object):
    def __init__(self, adr, lastrcv):
        self.adr = adr
        self.lastrcv = lastrcv
        self.ucount = 1
        self.lastpingrequest = 0
        self.achievedpings = []

    def __eq__(self, other):
        return self.adr == other.adr


class Message(object):
    def __init__(self, text, sender):
        self.text =  text
        self.sender = sender


class Server(object):
    def __init__(self, serverip="localhost", serverport=1337):
        self.slavebasket = []
        self.serversock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)

        self.serverip = serverip
        self.serverport = serverport

        if "localhost" in self.serverip or "127.0.0.1" in self.serverip:
            self.serverip = ""

        self.serveradr = (self.serverip, self.serverport)
        self.datalist = []
        self.maxclientinactivity = 3
        self.stopsignal = False

    def _rcv(self):
        while not self.stopsignal:
            data, adr = self.serversock.recvfrom(1024)
            conslave = Slave(adr, time.time())

            if data == b"_rc_":
                if conslave not in self.slavebasket:
                    self.slavebasket.append(conslave)
                    print("Accepted a new slave: " + str(adr) + "!")

                else:
                    for slaveB in self.slavebasket:
                        if slaveB.adr == conslave.adr:
                            slaveB.lastrcv = time.time()
                            slaveB.ucount += 1

            elif data == b"_pong_":
                    for slaveB in self.slavebasket:
                        if slaveB == conslave:
                            slaveB.achievedpings.append(round((time.time()-slaveB.lastpingrequest)*1000, 2))
                            print(str(conslave.adr) + " answered the ping "
                            "request after " + str(round((time.time()-slaveB.lastpingrequest)*1000, 2)) + " ms.")

            else:
                self.datalist.append(Message(data, adr))

    def _sweep(self):
        while not self.stopsignal:
            for nslave in self.slavebasket:
                if time.time() - nslave.lastrcv > self.maxclientinactivity:
                    print("Taking " + str(nslave.adr) + " out of the list for inactivity!")
                    self.slavebasket.remove(nslave)
            time.sleep(1)

    def showpings(self):
        for slave in self.slavebasket:
            if len(slave.achievedpings) != 0:
                print("Slave", slave.adr, "averaged a ping of", sum(slave.achievedpings)/len(slave.achievedpings),
                      " ms.")

    def sendall(self, msg):
        for slave in self.slavebasket:
            self.serversock.sendto(msg, slave.adr)

    def sendtarget(self, msg, targetadr):
        self.serversock.sendto(msg, targetadr)

    def ping(self, num=1, delay=1):
        while num > 0:
            for slave in self.slavebasket:
                self.sendtarget(b"ping", slave.adr)
                slave.lastpingrequest = time.time()
            num -= 1
            time.sleep(delay)

    def start(self):
        self.serversock.bind(self.serveradr)

        recvthread = threading.Thread(target=self._rcv)
        recvthread.start()

        sweepthread = threading.Thread(target=self._sweep)
        sweepthread.start()

    def stop(self):
        self.stopsignal = True





