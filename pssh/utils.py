# This file is part of parallel-ssh.
#
# Copyright (C) 2014-2022 Panos Kittenis and contributors.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, version 2.1.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA


"""Module containing static utility functions for parallel-ssh."""

import logging

host_logger = logging.getLogger('pssh.host_logger')
logger = logging.getLogger('pssh')


def enable_logger(_logger, level=logging.INFO):
    """Enables logging to stdout for given logger"""
    _logger.setLevel(level)
    stream_handlers = [h for h in _logger.handlers
                       if isinstance(h, logging.StreamHandler)]
    if stream_handlers:
        logger.warning("Logger already has a StreamHandler attached")
        return
    handler = logging.StreamHandler()
    host_log_format = logging.Formatter('%(asctime)s %(levelname)-8s %(name)-15s %(message)s')
    handler.setFormatter(host_log_format)
    _logger.addHandler(handler)


def enable_host_logger():
    """Enable host logger for logging stdout from remote commands
    as it becomes available.
    """
    enable_logger(host_logger)


def enable_debug_logger():
    """Enable debug logging for the library to sdout."""
    return enable_logger(logger, level=logging.DEBUG)


# The c implementation in ssh2.utils doesn't handle strings with null characters correctly,
# also this one supports \n\r as line separators.
def find_eol(data, pos):
    """Find end-of-line in buffer from position and return end position of
    line and where next find_eol should start from.

    Eg - find_eol(b'line\nline2', 0) would return (5, 6), next call should be
    find_eol(b'line\nline2', 6) for next line where 6 was added to previous
    position.

    :param buf: Data buffer to parse for line.
    :type buf: bytes
    :param pos: Starting position to parse from
    :type pos: int

    :rtype: (int, int)"""

    newline = data.find(b'\n', pos)
    if newline == -1:
        return -1, 0

    if data[newline-1:newline] == b'\r':
        return newline - pos - 1, 2
    elif data[newline+1:newline+2] == b'\r':
        return newline - pos, 2

    return newline - pos, 1
