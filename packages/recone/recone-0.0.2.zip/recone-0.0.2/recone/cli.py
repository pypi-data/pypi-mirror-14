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

"""
Simple CLI.
"""

import pprint
import zmq

try:
    import readline
except ImportError:
    pass

from recone.nodes import Master


def print_help():
    """Print available commands.
    """
    print('Available commands:')
    print('  exit, quit or q           exit')
    print('  help, h or ?              print this help')
    print('  status                    get status from broker')
    print('  servants                  get list of servants')
    print('  list <servant>            get list of commands from servant')
    print('  run <servant> <command>   run command on addressee')
    print('        ... <argument(s)>')


def run(name=None, zmq_ctx=None, host='127.0.0.1', port_in=6800,
        port_out=6801):
    """Run command line interface.

    Runs a master node in background and provides and command line interface to
    interact with the servants.

    Args:
        name (str): Name of the node. Defaults to 'simpleCLI'.
        zmq_ctx (zmq.Context): ZeroMQ context to use. Defaults to None which
            creates a new one.
        host (str): Hostname or IP address of the broker. Defaults to
            127.0.0.1.
        port_in (int): Port on which the broker listens for incoming messages.
            Defaults to 6800.
        port_out (int): Port on which the broker listens for subscribers to
            send messages to. Defaults to 6801.
    """
    # set or create ZeroMQ context
    zmq_ctx = zmq_ctx or zmq.Context.instance()

    # pretty print
    pp = pprint.PrettyPrinter()

    # start a master
    name = name or 'masterCLI'
    master = Master(name=name, zmq_ctx=zmq_ctx, host=host, port_in=port_in,
                    port_out=port_out)
    master.start()

    try:
        while True:
            # read command from stdin
            cmd = input(">>> ")
            cmd = cmd.split()

            # the following commands are allowed:
            #
            # exit, quit or q: exit the CLI
            # help, h or ?: get help
            # status: get status from broker
            # servant: get list of servants
            # list: get list of commands from all servants
            # list <servant>: get list of commands from servant
            # run <servant> <command> <argument(s)>: run command on servant

            if len(cmd) is 1 and cmd[0] in ['exit', 'quit', 'q']:
                master.shutdown()
                return

            elif len(cmd) is 1 and cmd[0] in ['help', 'h', '?']:
                print_help()
                continue

            elif len(cmd) is 1 and cmd[0] == 'status':
                (status, resp) = master.get_broker_status()

            elif len(cmd) is 1 and cmd[0] == 'servants':
                (status, resp) = master.get_servants()

            elif len(cmd) is 1 and cmd[0] == 'list':
                (status, resp) = master.list_all_commands()

            elif len(cmd) is 2 and cmd[0] == 'list':
                (status, resp) = master.list_commands(cmd[1])

            elif len(cmd) > 2 and cmd[0] == 'run':
                (status, resp) = master.run_command(cmd[1], cmd[2:])

            else:
                print('Failed: invalid command or wrong number of arguments')
                continue

            # print out the response, use PrettyPrint for dicts
            if status is True:
                if isinstance(resp, dict):
                    pp.pprint(resp)
                else:
                    print(resp)
            else:
                print('Failed: {resp}'.format(resp=resp))

    except (KeyboardInterrupt, EOFError):
        master.shutdown()
        return
