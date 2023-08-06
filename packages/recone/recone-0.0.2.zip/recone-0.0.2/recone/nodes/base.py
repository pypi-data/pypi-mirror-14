# coding: utf-8
#
# ReCoNe - Framework to remote control a network of clients.
# Copyright (c) 2016, Tobias Bleiker & Dumeni Manatschal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#
# Source on github:
#   https://github.com/tbleiker/recone
#

import logging
import threading
import queue
import zmq


class Base:
    """Base class for ``Broker`` and ``Client``.

    This class provides the basic functionality for the classes ``Broker` and
    `Client``.

    The broker opens a ZeroMQ PULL socket on ``port_in`` to receive messages `
    and a PUB socket on ``port_out`` to send messages.

    The arguments are described in the classes ``Broker``, ``Servant`` and
    ``Master``.
    """

    def __init__(self, name, zmq_ctx, host, port_in, port_out, log):
        # set or create a logger
        self.log = log or logging.getLogger(__name__)

        # set or create ZeroMQ context
        self.zmq_ctx = zmq_ctx or zmq.Context.instance()

        # sockets for sending and receiving messages
        self.zmq_sender = None
        self.zmq_receiver = None

        # create ZeroMQ poller
        self.zmq_poller = zmq.Poller()
        self.poller_timeout = 1000

        # threads handling heartbeats and incoming and outgoing messages
        self.thread_sender = None
        self.thread_receiver = None
        self.thread_heartbeat = None

        # create input queue for heartbeat and sender threads
        self.queue_heartbeat = queue.Queue()
        self.queue_sender = queue.Queue()

        # set exit message and exit event for the three threads
        self.exit_heartbeat_msg = 'STOP!'
        self.exit_sender_msg = 'STOP!'
        self.exit_receiver_event = threading.Event()

        # set name of the node
        self.name = name

        # create a lock for accessing internal class variables
        self.lock = threading.Lock()

        # set broker address
        self.broker_address_in = 'tcp://{host}:{port}'.format(
            host=host, port=port_in)
        self.broker_address_out = 'tcp://{host}:{port}'.format(
            host=host, port=port_out)

        self.log.info('{name}: Set broker address (in) to {address}.'.format(
            name=self.name, address=self.broker_address_in))
        self.log.info('{name}: Set broker address (out) to {address}.'.format(
            name=self.name, address=self.broker_address_out))

    def _send_msg(self, *args, **kwargs):
        """Put a message into the input queue of the sender thread.

        This function must be implemented by a subclass. The subclass also
        defines what arguments are needed.
        """
        raise NotImplementedError(
            'This function must be implemented by the subclass.')
        pass

    def _worker_sender(self):
        """Send messages.

        This function is responsible for sending messages over ZeroMQ. It is
        run as a thread on startup and must be implemented by a subclass.
        """
        raise NotImplementedError(
            'This function must be implemented by the subclass.')
        pass

    def _worker_heartbeat(self):
        """Send and/or handle heartbeats.

        This function is run as a thread on startup and must be implemented by
        a subclass.
        """
        raise NotImplementedError(
            'This function must be implemented by the subclass.')
        pass

    def _worker_receiver(self):
        """Receive and process messages.

        This function is responsible for receiving messages over ZeroMQ and
        processing them. It is run as a thread on startup and must be
        implemented by a subclasses.
        """
        raise NotImplementedError(
            'This function must be implemented by the subclass.')
        pass

    def is_alive(self):
        """Check if node is alive.

        Returns:
            bool: True if all three threads (heartbeat, sender and receiver)
            are up and running, False otherwise.
        """
        try:
            alive = self.thread_sender.is_alive() and \
                    self.thread_receiver.is_alive() and \
                    self.thread_heartbeat.is_alive()
        except AttributeError:
            alive = False

        return alive

    def is_stopped(self):
        """Check if node is stopped.

        Returns:
            bool: True if all three threads (heartbeat, sender and receiver)
            are stopped, False otherwise.
        """
        stopped = self.thread_sender is None and \
                  self.thread_receiver is None and \
                  self.thread_heartbeat is None

        return stopped

    def start(self):
        """Start node.

        Start all three threads. The sender thread is started first, so the
        node is ready to respond to messages when the receiver thread is
        started. The heartbeat thread is started afterwards.

        Returns:
            bool: True if successful, False otherwise.
        """
        if self.is_alive():
            return True

        elif not self.is_stopped():
            self.log.error(
                '{name}: Failed to start. Some threads are not properly '
                'stopped.'.format(
                    name=self.name))
            return False

        try:
            # start sender thread
            name = '{name}.sender'.format(name=self.name)
            self.thread_sender = threading.Thread(
                name=name, target=self._worker_sender)
            self.thread_sender.start()

            # start receiver thread
            name = '{name}.receiver'.format(name=self.name)
            self.exit_receiver_event.clear()
            self.thread_receiver = threading.Thread(
                name=name, target=self._worker_receiver)
            self.thread_receiver.start()

            # start heartbeat thread
            name = '{name}.heartbeat'.format(name=self.name)
            self.thread_heartbeat = threading.Thread(
                name=name, target=self._worker_heartbeat)
            self.thread_heartbeat.start()

        except:
            self.log.error(
                '{name}: Failed to start one or more threads'.format(
                    name=self.name))
            raise

        self.log.info(
            '{name}: Started heartbeat, sender and receiver threads.'.format(
                name=self.name))

        return True

    def join(self):
        """Join node.

        The node is joined by joining the sender thread. The sender thread is
        joined because it is started first and stopped last.

        Returns:
            bool: True if the threads stopped, False if the sender thread could
            not be joined.
        """
        if self.is_alive():
            try:
                self.thread_sender.join()
            except (KeyboardInterrupt, SystemExit):
                self.stop()
            finally:
                return True
        else:
            return False

    def stop(self):
        """Stop node.

        Stop all three threads. The heartbeat thread is stopped first. The
        sender thread is stopped after the receiver thread to make sure
        that all received messages are processed and responded to.
        the sender thread when all messages are sent.

        Returns:
            bool: True if successful, False otherwise.
        """

        if self.is_stopped():
            return True

        elif not self.is_alive():
            self.log.error(
                '{name}: Failed to stop. Some threads are not properly '
                'running.'.format(
                    name=self.name))
            return False

        try:
            # stop heartbeat thread
            self.queue_heartbeat.put(self.exit_heartbeat_msg)
            self.thread_heartbeat.join()
            del self.thread_heartbeat
            self.thread_heartbeat = None

            # stop receiver thread
            self.exit_receiver_event.set()
            self.thread_receiver.join()
            del self.thread_receiver
            self.thread_receiver = None

            # stop sender thread
            self.queue_sender.put(self.exit_sender_msg)
            self.thread_sender.join()
            del self.thread_sender
            self.thread_sender = None
        except:
            self.log.error(
                '{name}: Failed to stop one ore more threads.'.format(
                    name=self.name))
            raise

        self.log.info(
            '{name}: Stopped heartbeat, sender and receiver threads.'.format(
                name=self.name))

        return True

    def cleanup_sockets(self):
        """Clean up ZeroMQ sockets.

        Returns:
            bool: True if successful, False if threads are still running.
        """
        if not self.is_stopped():
            self.log.warn(
                "{name}: Cannot clean up ZeroMQ sockets when threads are "
                "still running.".format(
                    name=self.name))
            return False

        if self.zmq_receiver is not None:
            self.zmq_receiver.close()
            if self.zmq_poller is not None:
                self.zmq_poller.unregister(self.zmq_receiver)
            self.zmq_receiver = None
            self.log.info("{name}: Closed ZeroMQ receiver socket.".format(
                name=self.name))
        if self.zmq_sender is not None:
            self.zmq_sender.close()
            self.zmq_sender = None
            self.log.info("{name}: Closed ZeroMQ sender socket.".format(
                name=self.name))

    def shutdown(self):
        """Stop threads and cleanup sockets.
        """
        self.stop()
        self.cleanup_sockets()
