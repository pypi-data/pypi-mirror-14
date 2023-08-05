#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  httpoutclient.py
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

from gevent import monkey; monkey.patch_socket()
from wishbone import Actor
import requests


class HTTPOutClient(Actor):

    '''**Posts data to the requested URL**

    Posts data to a remote URL


    Parameters:

        - selection(str)("@data")
           |  The part of the event to submit externally.
           |  Use an empty string to refer to the complete event.

        - method(str)("PUT")
           |  The http method to use. PUT/POST

        - content_type(str)("application/json")
           |  The content type to use.

        - accept(str)("text/plain")
           |  The accept value to use.

        - url(str)("http://localhost")
           |  The url to submit the data to

        - username(str)
           |  The username to authenticate

        - password(str)
           |  The password to authenticate


    Queues:

        - inbox
           |  Incoming messages

        - outbox
           |  Outgoing messges
    '''

    def __init__(self, config, selection="@data", method="PUT", content_type="application/json", accept="text/plain", url="https://localhost", username=None, password=None):

        Actor.__init__(self, config)
        self.pool.createQueue("inbox")
        self.registerConsumer(self.consume, "inbox")

    def preHook(self):

        if self.kwargs.method == "PUT":
            self.submitToResource = self.__put
        elif self.kwargs.method == "POST":
            self.submitToResource = self.__post
        else:
            raise Exception("Invalid http method defined: '%s'." % self.kwargs.method)

        if self.kwargs.url.startswith('https'):
            monkey.patch_ssl()

    def consume(self, event):

        try:
            response = self.submitToResource(event.get(self.kwargs.selection))
            response.raise_for_status()
        except Exception as err:
            self.logging.error("Failed to submit data.  Reason: %s" % (err))
            event.set(str(response.text), "@tmp.%s.server_response" % (self.name))
            raise

    def __put(self, data):

        return requests.put(self.kwargs.url, data=data, auth=(self.kwargs.username, self.kwargs.password), headers={'Content-type': self.kwargs.content_type, 'Accept': self.kwargs.accept})

    def __post(self, data):

        return requests.post(self.kwargs.url, data=data, auth=(self.kwargs.username, self.kwargs.password), headers={'Content-type': self.kwargs.content_type, 'Accept': self.kwargs.accept})
