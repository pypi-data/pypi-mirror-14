#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  setup.py
#
#  Copyright 2014 Adam Fiebig <fiebig.adam@gmail.com>
#  Originally based on 'wishbone' project by smetj
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

from compysition.queue import QueuePool
from compysition.qlogger import QLogger
from compysition.errors import *
from restartlet import RestartPool
from compysition.event import CompysitionEvent
from gevent import sleep, socket
from gevent.event import Event
from gevent.local import local
from time import time
from copy import deepcopy
import traceback
import functools
import cPickle as pickle


class Actor(object):
    """
    The actor class is the abstract base class for all implementing compysition actors.
    In order to be a valid 'module' and connectable with the compysition event flow, a module must be an extension of this class.

    The Actor is responsible for putting events on outbox queues, and consuming incoming events on inbound queues.
    """

    DEFAULT_EVENT_SERVICE = "default"

    def __init__(self, name, size=0, frequency=1, generate_metrics=True, blocking_consume=False, rescue=False, *args, **kwargs):
        """
        **Base class for all compysition actors**

        Parameters:

        - name (str):               The instance name
        - size (int):               The max amount of events any outbound queue connected to this actor may contain. A value of 0 represents an infinite qsize  (Default: 100)
        - frequency (int):          The frequency that metrics are generated and broadcasted to the 'metrics' queue                                             (Default: 1)
        - generate_metrics (bool):  Whether or not to generate and broadcast metrics for this actor                                                             (Default: True)
        - blocking_consume (bool):  Define if this module should spawn a greenlet for every single 'consume' execution, or if
                                        it should execute 'consume' and block until that 'consume' is complete. This is usually
                                        only necessary if executing work on an event in the order that it was received is critical.                             (Default: False)

        """
        self.blockdiag_config = {"shape": "box"}
        self.name = name
        self.size = size
        self.frequency = frequency
        self.pool = QueuePool(size)
        self.logger = QLogger(name)
        self.__loop = True
        self.threads = RestartPool(logger=self.logger, sleep_interval=1)

        self.generate_metrics = generate_metrics

        self.__run = Event()
        self.__run.clear()
        self.__connections = {}
        self.__block = Event()
        self.__block.clear()
        self.__blocking_consume = blocking_consume
        self.__consumers = []
        self.rescue = rescue

        # This is the map to determine input processing and type checking of incoming data
        # TODO: "all" is here on the parent Actor temporarily until actors are all moved to utilize type checking
        self.input_types_processing_map = {str: self._process_str_input,
                                           "all": self._process_all_input}

    def block(self):
        self.__block.wait()

    def connect_error_queue(self, source_queue_name, destination, destination_queue_name, *args, **kwargs):
        self.connect_queue(source_queue_name, destination, destination_queue_name, error_queue=True, *args, **kwargs)

    def connect_queue(self, source_queue_name, destination, destination_queue_name, error_queue=False, check_existing=True):
        '''Connects the <source> queue to the <destination> queue.
        In fact, the source queue overwrites the destination queue.'''
        """TODO: Refactor and simplify this"""

        source_queue = self.pool.default_outbound_queues.get(source_queue_name, None)
        source_queue_scope = self.pool.default_outbound_queues
        if not source_queue:
            source_queue = self.pool.outbound_queues.get(source_queue_name, None)
            source_queue_scope = self.pool.outbound_queues

        destination_queue = destination.pool.inbound_queues.get(destination_queue_name, None)

        if check_existing:
            if source_queue:
                raise QueueConnected("Outbound queue {queue_name} on {source_name} is already connected".format(queue_name=source_queue_name,
                                                                                                                source_name=self.name))

            if destination_queue:
                raise QueueConnected("Inbound queue {queue_name} on {destination_name} is already connected".format(queue_name=destination_queue_name,
                                                                                                                    destination_name=destination.name))

        if not source_queue:
            if not destination_queue:
                if not error_queue:
                    source_queue = self.pool.add_outbound_queue(source_queue_name)
                else:
                    source_queue = self.pool.add_error_queue(source_queue_name)

                destination.register_consumer(destination_queue_name, source_queue)
            elif destination_queue:
                if not error_queue:
                    source_queue = self.pool.add_outbound_queue(source_queue_name, queue=destination_queue)
                else:
                    source_queue = self.pool.add_error_queue(source_queue_name, queue=destination_queue)

        else:
            if not destination_queue:
                destination.register_consumer(destination_queue_name, source_queue)
            else:
                self.pool.move_queue(source_queue, destination_queue, queue_scope=source_queue_scope)

        self.logger.info("Connected queue '{0}' to '{1}.{2}'".format(source_queue_name, destination.name, destination_queue_name))

    def loop(self):
        '''The global lock for this module'''

        return self.__loop

    def is_running(self):
        return self.__run.is_set()

    def register_consumer(self, queue_name, queue):
        '''
        Add the passed queue and queue name to
        '''
        self.pool.add_inbound_queue(queue_name, queue=queue)
        self.threads.spawn(self.__consumer, self.consume, queue)

    def start(self):
        '''Starts the module.'''
        self.logger.connect_logs_queue(self.pool.default_outbound_queues['logs'])
        if self.generate_metrics:
            self.threads.spawn(self.__metric_emitter)

        if hasattr(self, "pre_hook"):
            self.logger.debug("pre_hook() found, executing")
            self.pre_hook()

        self.__run.set()
        self.logger.debug("Started with max queue size of {size} events and metrics interval of {interval} seconds.".format(size=self.size,
                                                                                                                            interval=self.frequency))

    def stop(self):
        '''Stops the loop lock and waits until all registered consumers have exit.'''

        self.__loop = False
        self.__block.set()

        # This should do a self.threads.join() but currently it is blocking. This issue needs to be resolved
        # But in the meantime post_hook will execute

        if hasattr(self, "post_hook"):
            self.logger.debug("post_hook() found, executing")
            self.post_hook()

    def send_event(self, event, queue=None, queues=None):
        """
        Sends event to all registered outbox queues. If multiple queues are consuming the event,
        a deepcopy of the event is sent instead of raw event.

        If 'queue' is provided, it supercedes all others and submits ONLY to that queue
        """
        if queue is not None:
            self.__submit(queue, event=event)
        else:
            if queues:
                send_queues = queues
            else:
                send_queues = self.pool.outbound_queues.values()
            self.__loop_submit(event, send_queues)

    def send_error(self, event, queue=None, queues=None):
        """
        Calls 'send_event' with all error queues as the 'queues' parameter
        """
        if not queues:
            queues = self.pool.error_queues.values()

        if queues or queue:
            self.send_event(event, queue=queue, queues=queues)

    def __loop_submit(self, event, queues):
        """
        :param event:
        :param queues:
        :return:
        """
        if queues:
            map(functools.partial(self.__submit, event=event), queues)

    def __submit(self, queue, event=None):
        if event is not None:
            queue.put(deepcopy(event))
            sleep(0)

    def __consumer(self, function, queue):
        '''Greenthread which applies <function> to each element from <queue>
        '''

        self.__run.wait()

        while self.loop():
            queue.wait_until_content()
            try:
                event = queue.get(timeout=10)
                original_data = deepcopy(event.data)
            except QueueEmpty as err:
                pass
            else:
                if self.__blocking_consume:
                    self.__do_consume(function, event, queue, original_data)
                else:
                    self.threads.spawn(self.__do_consume, function, event, queue, original_data, restart=False)

        while True:
            if queue.qsize() > 0:
                try:
                    event = queue.get()
                    original_data = deepcopy(event.data)
                except QueueEmpty as err:
                    break
                else:
                    self.threads.spawn(self.__do_consume, function, event, queue, original_data, restart=False)
            else:
                break

    def __do_consume(self, function, event, queue, original_data):
        """
        A function designed to be spun up in a greenlet to maximize concurrency for the __consumer method
        This function actually calls the consume function for the actor
        """
        try:
            event.data = self.__validate_input(event.data)
            consume_local = local()
            consume_local.event = event
            function(event, origin=queue.name, origin_queue=queue)
        except QueueFull as err:
            event.data = original_data
            queue.rescue(event)
            err.wait_until_free()
        except InvalidInputException as error:
            self.logger.error("Invalid input detected: {0}".format(error))
        except Exception as err:
            print(traceback.format_exc())    # This is an unhappy path to get an exception at this point, so we want to print to STDOUT
                                             # In case this is a problem with the log_actor itself. At least for now
            if self.rescue:
                sleep(1)                    # To prevent spam loop for an unresolvable issue
                queue.put(event)
            else:
                if not event.get('errors', None):
                    event.errors = []

                event.errors.append(pickle.dumps(err))
                self.send_error(event)

    def __validate_input(self, data):
        """
        Validate event input using input_types_processing_map to find appropriate validation/processing function
        If the map is found and the reference is callable, transform event.data into the format returned by that function.
        If a type mapping is defined but the reference is NOT callable, the data will remain unchanged
        """
        process_input_function = self.input_types_processing_map.get(type(data),
                                                                     self.input_types_processing_map.get("all", None))
        if process_input_function is None:
            raise InvalidInputException("Invalid input type detected. Event data was of type '{type}'".format(type=type(data)))

        if hasattr(process_input_function, '__call__'):
            data = process_input_function(data)

        return data

    def __metric_emitter(self):
        '''A greenthread which collects the queue metrics at the defined interval.'''

        self.__run.wait()
        while self.loop():
            for queue_name, queue in self.pool.outbound_queues.iteritems():
                stats = queue.stats()
                for item in stats:
                    while self.loop():
                        try:
                            self.pool.queues.metrics.put({"header": {}, "data": (time(), "compysition", socket.gethostname(), "queue.%s.%s.%s" % (self.name, queue.name, item), stats[item], '', ())})
                            break
                        except QueueFull:
                            self.pool.queues.metrics.wait_until_empty()
            sleep(self.frequency)

    def create_event(self, *args, **kwargs):
        return CompysitionEvent(**kwargs)

    def consume(self, event, *args, **kwargs):
        """Raises error when user didn't define this function in his module.
        Due to the nature of *args and **kwargs in determining method definition, another check is put in place
        in 'router/default.py' to ensure that *args and **kwargs is defined"""

        raise SetupError("You must define a consume function as consume(self, event, *args, **kwargs)")

    def _process_str_input(self, data):
        """
        This is the default implementation - all current actors accept string input. This may change in the future.
        Override in implementing Actor to convert string input to desired value, or raise the appropriate exception
        """
        return data

    def _process_all_input(self, data):
        """
        This is here in the super class temporarily to allow for legacy support while actors are converted to use
        proper input type checking. The "all" keyword map should be used to allow for "all" types of event.data
        """
        return data