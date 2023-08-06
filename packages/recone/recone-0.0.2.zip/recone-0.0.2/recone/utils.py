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

import msgpack


def msg_encode(msg):
    """Encode message with msgpack.

    Arguments:
        msg (str): Message to encode.

    Returns:
        bytes: Encoded message.
    """
    return msgpack.packb(msg, use_bin_type=True)


def msg_decode(msg):
    """Decode message with msgpack.

    Arguments:
        msg (str): Message to decode.

    Returns:
        bytes: Decoded message.
    """
    return msgpack.unpackb(msg, encoding='utf-8')
