#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  modify.py
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
from copy import deepcopy
import re
import arrow

VALID_EXPRESSIONS = ["add_item",
                     "copy",
                     "del_item",
                     "delete",
                     "extract",
                     "lowercase",
                     "set",
                     "template",
                     "uppercase",
                     "time",
                     ]


class Modify(Actor):

    '''**Modify and manipulate datastructures.**

    This module modifies the data of an event using a **sequential** list of
    expressions.

    Expressions are dictionaries containing 1 item. The key is a string and
    the value is a list of parameters accepted by the expression.

    For example::

        {"set": ["hi", "@data.one"]}


    Sets the value *"hi"* to key *"@data.one"*.

    In the the YAML formatted bootstrap file that would look like::

        module: wishbone.function.modify
        arguments:
          expressions:
            - set: [ "hi", "@data.one" ]


    Valid expressions are:


      - **add_item**::

          add_item: [<item>, <key>]

        Adds *<item>* to the list stored under *<key>*.


      - **copy**::

          copy: [<source_key>, <destination_key>, <default_value>]

        Copies *<source_key>* to *<destination_key>* and overwrites
        *<destination_key>* when it exists.  If <source_key> does not exist,
        <default_value> is taken instead.


      - **del_item**::

          del_item: [<key>, <item>]

        Deletes first occurance of *<item>* from the list stored under
        *<source_key>*.


      - **delete**::

          delete: [<key>]

        Deletes *<key>* from the event.


      - **extract**::

          extract: [<destination>, <regex>, <source>]

        Makes use of Python re module to extract named groups from *<source>*
        using *<regex>* and add the resulting matches to *<destination>*.

        The following example would extract the words "one" and "two" from
        "@data.test" and add the to @data.extract:

          expression::

            extract: ["@data.extract", '(?P<first>.*?);(?P<second>.*)', "@data.test"]

          result::

            {"@data":{"test:"one;two", extract:{"first": "one", "second": "two"}}}


      - **lowercase**::

          lowercase: [<key>]

        Turns the string stored under *<key>* to lowercase.


      - **set**::

          set: [<value>, <key>]

        Sets *<value>* to the event *<key>*.


      - **uppercase**::

          uppercase: [<key>]

        Turns the string stored under *<key>* to uppercase.


      - **template**::

          template: [<destination_key>, <template>, <source_key>]

        Uses the dictionary stored in *<source_key>* to complete *<template>*
        and stores the results into key *<destination_key>*. The templating
        language used is Python's builtin string format one.


      - **time**::

          time: [<destination_key>, <format>]

        Modifies the *<@timestamp>* value according the the *<format>* specification
        and stores it into *<destination_key>*.
        See http://crsmithdev.com/arrow/#format for the format.



    Parameters:

        - expressions(list)([])
           |  A list of expressions to apply.

    Queues:

        - inbox:
           |  Incoming messages

        - outbox:
           |  Outgoing modified messages
    '''

    def __init__(self, actor_config, expressions=[]):
        Actor.__init__(self, actor_config)
        self.pool.createQueue("inbox")
        self.pool.createQueue("outbox")
        self.registerConsumer(self.consume, "inbox")

    def consume(self, event):

        for expression in self.kwargs.expressions:
            try:
                command, args = self.__extractExpr(expression)
                event = getattr(self, "command_%s" % (command))(event, *args)
            except Exception as err:
                self.logging.error("Failed to process expression '%s'. Reason: %s Skipped." % (expression, err))

        self.submit(event, self.pool.queue.outbox)

    def command_add_item(self, event, item, key):

        event.get(key).append(item)
        return event

    def command_copy(self, event, source, destination, default_value):

        try:
            event.copy(source, destination)
        except KeyError:
            event.set(default_value, destination)
        return event

    def command_del_item(self, event, item, key):

        event.get(key).remove(item)

        return event

    def command_delete(self, event, key):

        event.delete(key)
        return event

    def command_extract(self, event, destination, regex, source):

        matches = re.match(regex, event.get(source))
        event.set(matches.groupdict(), destination)
        return event

    def command_lowercase(self, event, key):

        event.set(event.get(key).lower(), key)
        return event

    def command_set(self, event, value, key):

        event.set(deepcopy(value), key)
        return event

    def command_template(self, event, destination, template, key):

        result = template.format(**event.get(key))
        event.set(result, destination)
        return event

    def command_time(self, event, destination_key, f):

        result = arrow.get(event.get("@timestamp")).format(f)
        event.set(result, destination_key)
        return event

    def command_uppercase(self, event, key):

        event.set(event.get(key).upper(), key)
        return event

    def __extractExpr(self, e):

        assert isinstance(e, dict), "The expression should be a dict."
        assert len(e.keys()) == 1, "The expression should only contain 1 value"

        c = e.keys()[0]
        assert c in VALID_EXPRESSIONS, "'%s' is an invalid expression." % c

        assert isinstance(e[c], list), "The expression value must be a list."
        return c, e[c]
