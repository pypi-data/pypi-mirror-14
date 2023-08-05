#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  wb_livestatus.py
#
#  Copyright 2016 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from wishbone import Actor
from wishbone.event import Event as WB_Event
from gevent import socket
from gevent import sleep
from gevent.event import Event
from json import loads


class LiveStatus(Actor):

    '''**Queries Livestatus at the chosen interval.**

    Queries LiveStatus with the predefined query and returns each returned
    record as new event


    Parameters:

        - host(str)("127.0.0.1")
           |  The Livestatus address/hostname to connect to.

        - port(int)(6557)
           |  Explaining the parameter.

        - timeout(int)(10)
           |  Timeout in seconds to connect.

        - query(str)("GET Status")
           |  The query to execute

        - interval(int)(10)
           |  The interval to query

    Queues:

        - outbox
           |  A description of the queue

    '''

    def __init__(self, actor_config, host="127.0.0.1", port=6557, timeout=10, query="GET status", interval=10):
        Actor.__init__(self, actor_config)

        self.pool.createQueue("outbox")

        self._connect = Event()
        self._connect.set()

        self._query = Event()
        self._query.clear()

    def preHook(self):

        if not self.kwargs.query.endswith("\nOutputFormat: json"):
            self.kwargs.query = "%s\nOutputFormat: json" % (self.kwargs.query)
        self.sendToBackground(self.executeQuery)

    def executeQuery(self):

        while self.loop():
            s = self.setupConnection()
            try:
                s.send("%s\n" % (self.kwargs.query))
                s.shutdown(socket.SHUT_WR)
                response = self.drain(s)
                if response == "":
                    self.logging.error("The query returned no results.")
                else:
                    for item in self.processResponse(response):
                        self.submit(WB_Event(item), self.pool.queue.outbox)
            except Exception as err:
                self.logging.error("Failed to submit request.  Reason: %s" % (err))
            finally:
                sleep(self.kwargs.interval)

    def processResponse(self, data):

        data = loads(data)
        for line in data[1:]:
            yield dict(zip(data[0], line))

    def setupConnection(self):

        while self.loop():
            try:
                s = socket.socket()
                s.settimeout(self.kwargs.timeout)
                s.connect((self.kwargs.host, self.kwargs.port))
            except Exception as err:
                self.logging.error("Failed to connect.  Reason: %s" % (err))
                sleep(1)
            else:
                return s

    def drain(self, s):
        answer = []
        while self.loop():
            data = s.recv(10000)
            if data != "":
                answer.append(data)
            else:
                return "".join(answer)

