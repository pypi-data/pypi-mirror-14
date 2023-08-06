#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
# VERY inspired by the work of David Beazley
# https://raw.githubusercontent.com/dabeaz/concurrent/
#
# Licensed under LGPLv3, see file LICENSE in this source tree.
"""
Request handling

"""

import msgsocket
import socket
import time
import queue
import threading
import msgauth
import pickle

            
class BacnetRequest:
    def __init__(self, bacnet):
        self._send_pending = None
        self._outgoing = queue.Queue()
        self._reply = None
        self._reply_evt = threading.Event()
        self.network = bacnet

    # Connect to a server (launches a handler thread)
    def connect(self):
        thr = threading.Thread(target=self._server_connection_thread)
        thr.daemon = True
        thr.start()

    # Thread that tries keep a permanent connection with a server
    def _server_connection_thread(self):
        while True:
            # Establish the connection
            #while True:
            #    try:
            #        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #        sock.connect(address)
            #        break
            #    except socket.error:
            #        time.sleep(1)
            #        continue

            # Once connected, process messages
            msock = msgsocket.MessageSocket(sock)
            while True:
                # Get an outgoing message from the queue
                msg = self._outgoing.get()
                # Try to send it and get a reply
                try:
                    msock.send(msg)
                    self._reply = msock.recv()
                    self._reply_evt.set()
                except Exception as e:
                    # Something went horribly wrong 
                    print("Lost connection: Reason:",e)
                    msock.close()
                    self._reply = b''
                    self._reply_evt.set()
                    break

    # Send a message by queuing it and letting a server handle it
    def send_bytes(self,msg):
        if self._send_pending:
            raise RuntimeError("Must call recv() after send()")
        self._reply_evt.clear()
        self._outgoing.put(msg)
        self._send_pending = True

    # Receive a message from the queue
    def recv_bytes(self):
        if not self._send_pending:
            raise RuntimeError("Must call send() first")
        # Wait for reply to come back and return it
        self._reply_evt.wait()
        self._send_pending = False
        reply = self._reply
        del self._reply
        return reply

    # Pickle support
    def send(self,obj):
        self.send_bytes(pickle.dumps(obj))

    def recv(self):
        return pickle.loads(self.recv_bytes())


if __name__ == '__main__':
    s = RequestSocket()
    # Connect to a pool of possible servers
    s.connect(("localhost",20000),authkey=b"peekaboo")
    s.send(b"Hello")
    print(s.recv())