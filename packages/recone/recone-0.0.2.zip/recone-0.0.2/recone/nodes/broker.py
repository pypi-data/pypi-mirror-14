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
import zmq

from copy import deepcopy

from recone.nodes.base import Base
from recone import utils
from recone import messages as m


class Broker(Base):
    """Create a broker.

    This class extends the base class ``Base`` and implements the functionality
    needed to run a broker.

    Arguments:
        name (str): Name of the broker. Defaults to '.broker'.
        zmq_ctx (zmq.Context or None): ZeroMQ context to use. Defaults to None
            which creates a new one.
        host (str): Hostname or IP address for the broker to listen on.
            Defaults to 127.0.0.1.
        port_in (int): Port on which the broker listens for incoming messages.
            Defaults to 6800.
        port_out (int): Port on which the broker listens for subscribers to
            send messages to. Defaults to 6801.
        heartbeat_interval (int or float): Interval between heartbeats in
            seconds. Defaults to 5.
        log (logging.Logger or None): Logger. Defaults to None which gets one.
    """

    def __init__(self, name='.broker', zmq_ctx=None, host='127.0.0.1',
                 port_in=6800, port_out=6801, heartbeat_interval=5, log=None):
        super(Broker, self).__init__(name, zmq_ctx, host, port_in, port_out,
                                     log)

        # create and bind the ZeroMQ sockets
        self.zmq_sender = self.zmq_ctx.socket(zmq.PUB)
        self.zmq_sender.bind(self.broker_address_out)
        self.zmq_receiver = self.zmq_ctx.socket(zmq.PULL)
        self.zmq_receiver.bind(self.broker_address_in)
        self.zmq_poller.register(self.zmq_receiver, zmq.POLLIN)

        # create dictionary containing all connected clients
        self.status = dict()

        # set the interval between sending to heartbeats
        self.heartbeat_interval = heartbeat_interval
        # heartbeat id, is incremented for each sent heartbeat
        self.heartbeat_id = 0

    def get_status(self):
        """Get status.

        This function returns the status dictionary. Entries of the type
        datetime are converted to strings.

        Returns:
            dict: Dictionary containing information about the connected
            clients.
        """
        with self.lock:
            status = deepcopy(self.status)

        for client in status:
            status[client]['last_seen'] = str(status[client]['last_seen'])
            status[client]['first_seen'] = str(status[client]['first_seen'])

        return status

    def _send_msg(self, msg_type, sender, addressee, msg_id, content=None):
        """Put a message into the input queue of the sender thread.

        The content of the message can be any object which is serializable by
        msgpack.

        Arguments:
            msg_type (str): Typ of the message.
            sender (str): Name of the node which sends the message.
            addressee (str): Name of the node which should receive the message.
            msg_id (int): Message id.
            content (object): Message content. Must be serializable by
                msgpack.
        """
        msg = (msg_type, sender, addressee, msg_id, content)
        self.queue_sender.put(msg)

    def _worker_sender(self):
        """Send messages.

        This function is responsible for sending messages over ZeroMQ. It waits
        on the input queue for new messages and simply forwards them over
        ZeroMQ. It differs to the function in ``Client`` because it has to send
        multipart messages to the subscribers.

        This function is run as a thread on startup.
        """
        while True:
            msg = self.queue_sender.get()
            if msg == self.exit_sender_msg:
                break
            else:
                msg_enc = utils.msg_encode(msg)
                self.zmq_sender.send_multipart([msg[2].encode(), msg_enc])
                self.log.debug(
                    '{name}: Sent {msg}'.format(name=self.name, msg=msg))

    def _worker_heartbeat(self):
        """Send heartbeats.

        This function continuously sends heartbeats to all clients. Before a
        heartbeat is broadcasted, the status of all connected clients is
        checked and old clients removed.

        This function is run as a thread on startup
        """
        while True:
            try:
                ret = self.queue_heartbeat.get(
                    block=True, timeout=self.heartbeat_interval)
            except queue.Empty:
                ret = None

            if ret == self.exit_heartbeat_msg:
                break

            dt_now = datetime.datetime.now()

            old_clients = list()
            with self.lock:
                for client in self.status:
                    dt_old = self.status[client]['last_seen']
                    dt_diff = dt_now - dt_old
                    if dt_diff.total_seconds() > 2 * self.heartbeat_interval:
                        old_clients.append(client)

                for client in old_clients:
                    self.log.info(
                        '{name}: No heartbeat response from client {client}, '
                        'drop it.'.format(
                            name=self.name, client=client))
                    self.status.pop(client)

                heartbeat_id = self.heartbeat_id
                self.heartbeat_id += 1

            content = (str(dt_now), self.heartbeat_interval)
            self._send_msg('heartbeat', self.name, '.heartbeat', heartbeat_id,
                           content)

    def _worker_receiver(self):
        """Receive and process messages.

        This function is responsible for receiving messages over ZeroMQ and
        processing them. It is run as a thread on startup.
        """
        while not self.exit_receiver_event.is_set():
            # get message by polling the poller
            socks = dict(self.zmq_poller.poll(self.poller_timeout))
            if self.zmq_receiver in socks:
                msg_enc = self.zmq_receiver.recv()
                msg = utils.msg_decode(msg_enc)
                self.log.debug(
                    '{name}: Received {msg}'.format(name=self.name, msg=msg))
            else:
                continue

            # extract and process message
            (msg_type, sender, addressee, msg_id, content) = msg

            if msg_type == 'heartbeat' and addressee == self.name:
                # update status of the client with the current time, create a
                # new entry if the client is not yet known
                (client_role, time_old, time_client) = content
                dt_now = datetime.datetime.now()
                with self.lock:
                    if sender in self.status:
                        self.status[sender]['last_seen'] = dt_now
                    else:
                        self.log.info(
                            '{name}: First heartbeat response from client {'
                            'client}, add it.'.format(
                                name=self.name, client=sender))
                        status = dict()
                        status['role'] = client_role
                        status['first_seen'] = dt_now
                        status['last_seen'] = dt_now
                        self.status[sender] = status

            elif msg_type == 'heartbeat':
                # Drop heartbeat response if 'addressee' is not the broker's
                # name.
                self.log.warn(
                    '{name}: Drop heartbeat message {id} from {sender}, '
                    'addressee is not broker.'.format(
                        name=self.name, id=msg_id, sender=sender))

            elif msg_type == 'status' and addressee == self.name:
                # simply return the status
                status = self.get_status()
                self._send_msg('ok', self.name, sender, msg_id, status)

            elif msg_type == 'status':
                # drop status request if 'addressee' is not the broker's name
                # and inform client
                self.log.warn(
                    '{name}: Drop status request {id} from {sender}, '
                    'addressee is not broker.'.format(
                        name=self.name, id=msg_id, sender=sender))
                self._send_msg('fail', self.name, sender, msg_id,
                               m.addressee_not_broker)

            elif msg_type == 'update':
                # confirm a received update message and forward it
                self._send_msg(msg_type, sender, addressee, msg_id, content)
                self._send_msg('ok', self.name, sender, msg_id,
                               m.update_received)

            elif msg_type in ['ok', 'fail']:
                # forward messages of type 'ok' and 'fail' if addressee is
                # known
                with self.lock:
                    known = addressee in self.status

                if known:
                    self._send_msg(msg_type, sender, addressee, msg_id,
                                   content)
                else:
                    self.log.warn(
                        '{name}: Drop message {id} from {sender}, '
                        'addressee not known.'.format(
                            name=self.name, id=msg_id, sender=sender))
                    self._send_msg('fail', self.name, sender, msg_id,
                                   m.addressee_unknown)

            elif msg_type in ['list-commands', 'run-command']:
                # forward messages of type 'list-commands' and 'run-command'
                # if addressee is a servant
                servant = False
                with self.lock:
                    known = addressee in self.status
                    if known:
                        servant = self.status[addressee]['role'] == 'servant'

                if not known:
                    self.log.warn(
                        '{name}: Drop message {id} from {sender}, '
                        'addressee not known.'.format(
                            name=self.name, id=msg_id, sender=sender))
                    self._send_msg('fail', self.name, sender, msg_id,
                                   m.addressee_unknown)

                elif not servant:
                    self._send_msg('fail', self.name, sender, msg_id,
                                   m.addressee_not_servant)

                else:
                    self._send_msg(msg_type, sender, addressee, msg_id,
                                   content)

            else:
                # messages of other type are not valid, drop it
                self.log.warn(
                    '{name}: Drop message {id} from {sender}, invalid message '
                    'type.'.format(
                        name=self.name, id=msg_id, sender=sender))
                self._send_msg('fail', self.name, sender, msg_id,
                               m.message_type_invalid)
