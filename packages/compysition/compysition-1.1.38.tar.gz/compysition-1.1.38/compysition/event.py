#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  default.py
#
#  Copyright 2014 Adam Fiebig <fiebig.adam@gmail.com>
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
from uuid import uuid4 as uuid
from ast import literal_eval
from lxml import etree
from .errors import InvalidEventDataException, InvalidModificationException

"""
Compysition event is created and passed by reference among actors
"""

DEFAULT_EVENT_SERVICE="default"

class CompysitionEvent(object):

    """
    Anatomy of an event:
        - event_id: The unique and functionally immutable ID for this new event
        - meta_id:  The ID associated with other unique event data flows. This ID is used in logging
        - service:  (default: default) Used for compatability with the ZeroMQ MajorDomo configuration. Scope this to specific types of interproces routing
        - data:     <The data passed and worked on from event to event. Mutable and variable>
        - kwargs:   All other kwargs passed upon CompysitionEvent instantiation will be added to the event dictionary

    """

    def __init__(self, meta_id=None, service=None, data=None, *args, **kwargs):
        self.event_id = uuid().get_hex()
        self.meta_id = meta_id or self.event_id
        self.service = service or DEFAULT_EVENT_SERVICE
        self.data = data
        self.__dict__.update(kwargs)

    def to_string(self):
        return str(self.__dict__)

    def set(self, key, value):
        try:
            setattr(self, key, value)
            return True
        except:
            return False

    def get(self, key, default=None):
        return getattr(self, key, default)

    @staticmethod
    def from_string(string_value):
        string_value = string_value.strip()
        value_dict = literal_eval(string_value)
        event = CompysitionEvent(**value_dict)

        if value_dict.get('event_id', None):
            event.event_id = value_dict.get('event_id')

        return event

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def event_id(self):
        return self._event_id

    @event_id.setter
    def event_id(self, event_id):
        if self.get("_event_id", None):
            raise InvalidModificationException("Cannot alter event_id once it has been set. A new event must be created")
        else:
            self._event_id = event_id

    def get_properties(self):
        """
        Gets a dictionary of all event properties except for event.data
        Useful when event data is too large to copy in a performant manner
        """
        return {k: v for k, v in self.__dict__.items() if k != "data"}


class XMLEvent(CompysitionEvent):

    @CompysitionEvent.data.setter
    def data(self, data):
        if isinstance(data, str):
            try:
                data = etree.fromstring(data)
                self._data = data
            except Exception as err:
                raise InvalidEventDataException("Event data was invalid for {cls}: {err}".format(cls=self.__class__, err=err))
        elif isinstance(data, (etree._Element, etree._ElementTree)):
            self._data = data
        else:
            raise InvalidEventDataException("Event data was invalid for {cls}".format(cls=self.__class__))


class JSONEvent(CompysitionEvent):

    @CompysitionEvent.data.setter
    def data(self, data):
        if isinstance(data, str):
            try:
                data = literal_eval(data)
                self._data = data
            except Exception as err:
                raise InvalidEventDataException("Event data was invalid for {cls}: {err}".format(cls=self.__class__, err=err))
        elif isinstance(data, (list, dict)):
            self._data = data
        else:
            raise InvalidEventDataException("Event data was invalid for {cls}".format(cls=self.__class__))
"""

class LogEvent(CompysitionEvent):

    @CompysitionEvent.data.setter
    def data(self, data):
        if isinstance(data, str):
            try:
                data = etree.fromstring(data)
                self._data = data
            except Exception as err:
                raise InvalidEventDataException("Event data was invalid for {cls}: {err}".format(cls=self.__class__, err=err))
        elif isinstance(data, [list, dict]):
            self._data = data
        else:
            raise InvalidEventDataException("Event data was invalid for {cls}".format(cls=self.__class__))
"""
