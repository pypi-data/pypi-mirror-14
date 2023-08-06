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

import inspect
import zmq

from recone.nodes.client import Client
from recone import messages as m


class Servant(Client):
    """Create a servant.

    This class extends the class ``Client`` and implements the functionality
    needed to run a servant.

    Arguments:
        name (str): Name of the servant. Should be a unique name in the
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
        super(Servant, self).__init__(name, zmq_ctx, host, port_in,
                                      port_out, response_wait, log)

        # subscribe to relevant topics
        self.zmq_receiver.setsockopt(zmq.SUBSCRIBE, '.servant'.encode())

        # define the role of the client
        self.role = 'servant'

        # dictionary holding all commands which the servant provides
        self.commands = dict()

    def add_command(self, command, handler, description=None):
        """Add a command which can be called by the masters.

        Arguments:
            command (str): Name of the function.
            handler (method or function): Function or method handler.
            description (str): Optional description for the function. Defaults
                to None.

        Returns:
            bool: True if function or method is valid and could be added, False
            otherwise.
        """

        check = inspect.isfunction(handler) or inspect.ismethod(handler)

        if check:
            try:
                inspect.signature(handler)
            except (ValueError, TypeError):
                check = False

        check = check and type(command) is str

        if check:
            with self.lock:
                self.commands[command] = (handler, description)
            return True
        else:
            return False

    def send_update(self, update):
        """Send update to all masters.

        Arguments:
            update (object): Update to send. Must be serializable by msgpack.

        Returns:
            bool: True if broker has received the message, False otherwise.
        """
        return self._send_request('update', '.master', update)

    def _process_message(self, msg):
        """Further process incoming messages (specific to ``Servant``).

        This function is called by the receiver thread.
        """
        (msg_type, sender, addressee, msg_id, content) = msg

        if msg_type == 'list-commands':
            # return a dict with information about the available commands
            cmd_list = dict()
            for cmd in self.commands:
                try:
                    sig = inspect.signature(self.commands[cmd][0])
                    sig = str(sig)
                    if len(sig) == 2:
                        sig = None
                except (ValueError, TypeError):
                    # ValueError: raised if no signature can be provided
                    # TypeError: raised if that type of object is not supported
                    sig = None
                info = self.commands[cmd][1]
                cmd_list[cmd] = (sig, info)

            self._send_msg('ok', sender, msg_id, cmd_list)

            return True

        elif msg_type == 'run-command':
            # run the command
            failed = False

            # content should be a list or tuple
            if type(content) is list or type(content) is tuple:
                pass
            else:
                content = [content]

            # get command, break if no command is given or the command is not
            # valid
            cmd = content[0]

            if cmd is None:
                resp = m.command_empty
                failed = True
                self.log.warn(
                    '{name}: No command name is given.'.format(name=self.name))

            elif type(cmd) is not str:
                resp = m.command_not_string
                failed = True
                self.log.warn(
                    '{name}: Command name is not a string.'.format(
                        name=self.name))

            else:
                with self.lock:
                    if cmd not in self.commands:
                        resp = m.command_unknown
                        failed = True
                        self.log.warn(
                            '{name}: Command name is not known.'.format(
                                name=self.name))

                    else:
                        # get arguments
                        if len(content) > 1:
                            args = content[1:]
                        else:
                            args = ()

                        # run command and send back returned value
                        try:
                            func = self.commands[cmd][0]
                            if len(args) is 0:
                                resp = func()
                            else:
                                resp = func(*args)

                        except TypeError:
                            resp = m.command_failed
                            failed = True
                            self.log.warn(
                                '{name}: Command failed to run.'.format(
                                    name=self.name))

            if not failed:
                self._send_msg('ok', sender, msg_id, resp)
                return True
            else:
                self._send_msg('fail', sender, msg_id, resp)
                return False

        else:
            # messages of other type are not valid, drop it
            self.log.warn(
                '{name}: Drop message {id} from {sender}, invalid message '
                'type.'.format(
                    name=self.name, id=msg_id, sender=sender))
