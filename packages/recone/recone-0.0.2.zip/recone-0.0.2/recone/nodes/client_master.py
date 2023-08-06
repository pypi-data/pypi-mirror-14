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

import zmq

from copy import deepcopy

from recone.nodes.client import Client
from recone import messages as m


class Master(Client):
    """Create a master.

    This class extends the class ``Client`` and implements the functionality
    needed to run a master.

    Arguments:
        name (str): Name of the master. Should be a unique name in the
            network.
        zmq_ctx (zmq.Context or None): ZeroMQ context to use. Defaults to None
            which creates a new one.
        host (str): Hostname or IP address of the broker. Defaults to
            127.0.0.1.
        port_in (int): Port on which the broker listens for incoming messages.
            Defaults to 6800.
        port_out (int): Port on which the broker listens for subscribers to
            send messages to. Defaults to 6801.
        response_wait (int or float): Time to wait for a response in
            seconds. Defaults to 3 seconds.
        log (logging.Logger or None): Logger. Defaults to None which gets one.
    """

    def __init__(self, name, zmq_ctx=None, host='127.0.0.1', port_in=6800,
                 port_out=6801, response_wait=3, log=None):
        super(Master, self).__init__(name, zmq_ctx, host, port_in, port_out,
                                     response_wait, log)

        # subscribe to relevant topics
        self.zmq_receiver.setsockopt(zmq.SUBSCRIBE, '.master'.encode())

        # define the role of the client
        self.role = 'master'

        # function which will be called when an update message is received
        self.update_function = None

    def set_update_func(self, func_handler):
        """Set function which will be called when an update message is
        received.

        Arguments:
            func_handler (method or function): Function or method handler.
        """
        self.update_function = func_handler

    def get_broker_status(self):
        """Get the status of the broker.

        The function returns a tuple containing the success status and the
        response. The success status (first value) is True if a message of
        type ``ok`` is returned, False otherwise. The success status is also
        False if the message could not be sent or waiting on the response
        timed out. The response is either a str containing the error message
        if the success status is False or a dict containing information about
        all clients which are known to the broker.

        Returns:
            success, response (bool, object): A tuple containing the success
            status and the response (for more information see introduction
            above).
        """
        with self.lock:
            if self.broker is None:
                return False, m.broker_not_available
            else:
                broker_name = deepcopy(self.broker['name'])

        return self._send_request('status', broker_name, None)

    def get_servants(self):
        """Get a list of all available servants.

        The function gets the list of servants from the broker status. First,
        the function calls ``get_broker_status`` and then scans the response
        for the all servants.

        The function returns a tuple containing the success status and the
        response. The success status (first value) is True if the broker
        returned a message of type ``ok`` (containing the status), False
        otherwise. The response is either the list containing all available
        servants (if success is True) or the error message received from the
        broker.

        Returns:
            success, servants (bool, object): A tuple containing the success
            status and the response (for more information see introduction
            above).
        """
        success, resp = self.get_broker_status()

        if success:
            servants = list()
            for client in resp:
                if resp[client]['role'] == 'servant':
                    servants.append(client)
            ret = (True, servants)
        else:
            ret = (success, resp)

        return ret

    def list_commands(self, addressee):
        """Get a list of commands which can be run on the servant.

        The function returns a tuple containing the success status and the
        response. The success status (first value) is True if a message of
        type ``ok`` is returned, False otherwise. The success status is also
        False if the message could not be sent or waiting on the response
        timed out. The response is either a str containing the error message
        if the success status is False or dict containing information about
        the available commands on the servant..

        Arguments:
            addressee (str): Name of the servant which should be called.

        Returns:
            success, response (bool, object): A tuple containing the success
            status and the response (for more information see introduction
            above).
        """
        return self._send_request('list-commands', addressee, None)

    def list_all_commands(self):
        """Get a list of commands from all available servants.

        The function gets the list of all available servants by calling
        ``get_servants()``. Then, the functions calls for each servant
        ``list_commands(servant)``.

        The function returns a tuple containing the success status and the
        response. The success status (first value) is True if the broker
        returned a message of type ``ok`` (containing the status), False
        otherwise. The response is either the list containing all available
        servants (if success is True) or the error message received from the
        broker.

        Returns:
            success, response (bool, object): A tuple containing the success
            status and the response (for more information see introduction
            above).
        """

        success1, resp1 = self.get_servants()

        if success1:
            servants = dict()
            for servant in resp1:
                success2, resp2 = self.list_commands(servant)
                if success2:
                    servants[servant] = resp2
                else:
                    servants[servant] = 'failed'
            ret = (True, servants)
        else:
            ret = (success1, resp1)

        return ret

    def run_command(self, addressee, cmd):
        """Run a command on the servant.

        The argument ``cmd`` is a list or tuple containing the command's name
        as sting at first position, followed by the arguments. The list or
        tuple (with its arguments) must be serializable by msgpack.

        The function returns a tuple containing the success status and the
        response. The success status (first value) is True if a message of
        type ``ok`` is returned, False otherwise. The success status is also
        False if the message could not be sent or waiting on the response
        timed out. The response is either a str containing the error message
        if the success status is False or the object returned by the remote
        function or method.

        Arguments:
            addressee (str): Name of the servant on which to run the command.
            cmd (list or tuple): List or tuple containing the command's name
                and the arguments (for more information see introduction
                above).

        Returns:
            success, response (bool, object): A tuple containing the success
            status and the response (for more information see introduction
            above).
        """
        return self._send_request('run-command', addressee, cmd)

    def _process_message(self, msg):
        """Further process incoming messages (specific to ``Master``).

        This function is called by the receiver thread.
        """
        (msg_type, sender, addressee, msg_id, content) = msg

        if msg_type == 'update':
            # run update function if one is set, do not send response to
            # servant
            if self.update_function is not None:
                try:
                    self.update_function(content)
                except (TypeError, EOFError):
                    self.log.warn(
                        '{name}: Invalid argument(s) for update '
                        'function'.format(
                            name=self.name, msg=msg))

        else:
            self.log.warn(
                '{name}: Drop message {id} from {sender}, invalid message '
                'type.'.format(
                    name=self.name, id=msg_id, sender=sender))
