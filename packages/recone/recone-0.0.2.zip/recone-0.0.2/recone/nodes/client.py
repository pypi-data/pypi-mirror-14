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

import datetime
import queue
import threading
import zmq

from copy import deepcopy

from recone.nodes.base import Base
from recone import utils
from recone import messages as m


class Client(Base):
    """Base class for ``Servant`` and ``Master``.

    This class extends the base class ``Base`` and provides the basic
    functionality for the classes ``Servant`` and ``Master``.

    The arguments are described in the classes ``Servant`` and ``Master``.
    """

    def __init__(self, name, zmq_ctx, host, port_in, port_out,
                 response_wait, log):
        super(Client, self).__init__(name, zmq_ctx, host, port_in,
                                     port_out, log)

        # create, bind and setup the ZeroMQ sockets
        self.zmq_sender = self.zmq_ctx.socket(zmq.PUSH)
        self.zmq_sender.connect(self.broker_address_in)
        self.zmq_sender.setsockopt(zmq.LINGER, 10)
        self.zmq_receiver = self.zmq_ctx.socket(zmq.SUB)
        self.zmq_receiver.connect(self.broker_address_out)
        self.zmq_receiver.setsockopt(zmq.LINGER, 10)
        self.zmq_poller.register(self.zmq_receiver, zmq.POLLIN)

        # subscribe to relevant topics
        self.zmq_receiver.setsockopt(zmq.SUBSCRIBE, self.name.encode())
        self.zmq_receiver.setsockopt(zmq.SUBSCRIBE, '.heartbeat'.encode())

        # role of client (servant or master), is set by subclass
        self.role = None

        # connection status
        self.connected = False

        # message id, is incremented for each sent message
        self.msg_id = 0

        # dictionaries to handle outgoing messages for which a response is
        # expected
        self._responses = dict()
        self._responses_event = dict()
        self._responses_wait = response_wait

        # dictionary containing information about the broker
        self.broker = None

    def reset_sender_socket(self):
        """Reset the outgoing ZeroMQ socket.

        Close and recreate the ZeroMQ socket for outgoing messages. The
        function is called when the connection to the broker gets lost. This
        ensures that all pending messages get flushed and are not sent
        unintentionally as soon as the broker shows up again.
        """
        if self.zmq_receiver is not None:
            self.log.info(
                '{name}: Reset sender socket.'.format(name=self.name))
            self.zmq_sender.close()
            self.zmq_sender = self.zmq_ctx.socket(zmq.PUSH)
            self.zmq_sender.connect(self.broker_address_in)
            self.zmq_sender.setsockopt(zmq.LINGER, 10)

    def is_connected(self):
        """Check if node is connected to the broker.

        Returns:
            bool: True if a heartbeat was recently (enough) received, False
            otherwise.
        """
        with self.lock:
            connected = deepcopy(self.connected)

        return connected

    def _send_msg(self, msg_type, addressee, msg_id, content=None):
        """Put a message into the input queue of the sender thread.

        The content of the message can be any object which is serializable by
        msgpack.

        Arguments:
            msg_type (str): Typ of the message.
            addressee (str): Name of the node which should receive the message.
            msg_id (int): Message id.
            content (object): Message content. Must be serializable by
                msgpack.

        Returns:
            bool: True if successful, False otherwise (e.g. the broker cannot
            be seen.
        """
        if self.is_connected():
            msg = (msg_type, self.name, addressee, msg_id, content)
            self.queue_sender.put(msg)
            return True
        else:
            return False

    def _send_request(self, msg_type, addressee, content):
        """Send a message which expects a request.

        This function puts a message in the input queue of the sender thread.
        Afterwards the function waits on an event, this event is set by the
        receiver thread when the expected response has arrived.

        The content of the message can be any object which is serializable by
        msgpack.

        The function returns a tuple containing the success status and the
        response. The success status (first value) is True if a message of
        type ``ok`` is returned, False otherwise. The success status is also
        False if the message could not be sent or waiting on the response
        timed out. The response is either a str containing the error message
        if the success status is False or the response otherwise.

        Arguments:
            msg_type (str): Typ of the message.
            addressee (str): Name of the node which should receive the message.
            content (object): Message content. Must be serializable by
                msgpack.

        Returns:
            success, response (bool, object): A tuple containing the success
            status and the response (for more information see introduction
            above).
        """
        event = threading.Event()

        with self.lock:
            msg_id = deepcopy(self.msg_id)
            self.msg_id += 1
            self._responses[msg_id] = None
            self._responses_event[msg_id] = event

        # send message and wait for response
        ret = self._send_msg(msg_type, addressee, msg_id, content)
        if not ret:
            return False, m.broker_not_available

        ret = event.wait(self._responses_wait)
        if ret is False:
            with self.lock:
                self._responses.pop(msg_id)
            return False, m.response_timeout

        with self.lock:
            self._responses_event.pop(msg_id)
            resp = self._responses.pop(msg_id)

        if resp[0] == 'ok':
            success = True
        else:
            success = False

        return success, resp[1]

    def _worker_sender(self):
        """Send messages.

        This function is responsible for sending messages over ZeroMQ. It waits
        on the input queue for new messages and simply forwards them over
        ZeroMQ.

        This function is run as a thread on startup.
        """
        while True:
            msg = self.queue_sender.get()
            if msg == self.exit_sender_msg:
                break
            else:
                msg_enc = utils.msg_encode(msg)
                self.zmq_sender.send(msg_enc)
                self.log.debug(
                    '{name}: Sent {msg}'.format(name=self.name, msg=msg))

    def _worker_heartbeat(self):
        """Reply to heartbeats.

        This function replies to heartbeats from the broker. The receiver
        thread puts heartbeat messages into the heartbeat input queue. In the
        initial state, the function infinitely waits for a heartbeat. After
        the first heartbeat is received, the function only waits for twice the
        heartbeat interval (which is received in the heartbeat message from
        the server). For each timeout the function is set in its initial state,
        which also includes resetting the ZeroMQ sender socket.

        This function is run as a thread on startup
        """
        timeout = None

        while True:
            try:
                ret = self.queue_heartbeat.get(block=True, timeout=timeout)
                if ret == self.exit_heartbeat_msg:
                    break
            except queue.Empty:
                with self.lock:
                    self.log.info(
                        '{name}: No heartbeat message from broker {'
                        'broker_name}, disconnect.'.format(
                            name=self.name, broker_name=self.broker['name']))
                    self.connected = False
                    self.broker = None
                    self.reset_sender_socket()
                timeout = None
                continue

            broker_name, heartbeat_id, time_broker, heartbeat_interval = ret

            time_current = datetime.datetime.now()
            with self.lock:
                if not self.connected:
                    self.broker = dict()
                    self.connected = True
                    self.log.info(
                        '{name}: Got new heartbeat message from broker {'
                        'broker_name}, connect.'.format(
                            name=self.name, broker_name=broker_name))

                self.broker['name'] = broker_name
                self.broker['interval'] = heartbeat_interval
                self.broker['last_seen'] = time_current

            content = (self.role, time_broker, str(time_current))
            self._send_msg('heartbeat', broker_name, heartbeat_id, content)

            timeout = 2 * heartbeat_interval

    def _worker_receiver(self):
        """Receive and process messages.

        This function is responsible for receiving messages over ZeroMQ. It
        processes all messages of type ``heartbeat``, ``ok`` and ``fail``
        which `
        are common to ``Servant`` and ``Master``.

        This function is run as a thread on startup.
        """
        while not self.exit_receiver_event.is_set():
            # get message by polling poller
            socks = dict(self.zmq_poller.poll(self.poller_timeout))
            if self.zmq_receiver in socks:
                (addressee, msg_enc) = self.zmq_receiver.recv_multipart()
                msg = utils.msg_decode(msg_enc)
                self.log.debug(
                    '{name}: Received: {msg}'.format(name=self.name, msg=msg))
            else:
                continue

            (msg_type, sender, addressee, msg_id, content) = msg

            if msg_type == 'heartbeat':
                # forward heartbeat messages to the heartbeat thread
                time_broker, heartbeat_interval = content
                data = (sender, msg_id, time_broker, heartbeat_interval)
                self.queue_heartbeat.put(data)

            elif msg_type in ['ok', 'fail']:
                # set the event if a message of type ``ok`` or ``fail`` is
                # received, so the response function can terminate
                try:
                    with self.lock:
                        if msg_id in self._responses:
                            self._responses[msg_id] = (msg_type, content)
                            self._responses_event[msg_id].set()
                        else:
                            self.log.warn(
                                '{name}: Drop message {id} from {sender}, '
                                'invalid response (old or unexpected).'.format(
                                    name=self.name, id=msg_id, sender=sender))
                except KeyError:
                    pass

            else:
                # further process the message
                self._process_message(msg)

    def _process_message(self, msg):
        """Process messages which are specific to ``Servant`` or ``Master``.

        This function must be implemented by a subclass.
        """
        raise NotImplementedError(
            'This function must be implemented by the subclass.')
        pass
