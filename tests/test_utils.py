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

import unittest
from logging import NullHandler, DEBUG

from pssh import utils
from pssh.utils import find_eol

class ParallelSSHUtilsTest(unittest.TestCase):

    def test_enabling_host_logger(self):
        self.assertTrue(len([h for h in utils.host_logger.handlers
                             if isinstance(h, NullHandler)]) == 1)
        utils.enable_host_logger()
        # And again to test only one non-null handler is attached
        utils.enable_host_logger()
        self.assertTrue(len([h for h in utils.host_logger.handlers
                             if not isinstance(h, NullHandler)]) == 1)
        utils.host_logger.handlers = [NullHandler()]

    def test_enabling_pssh_logger(self):
        self.assertTrue(len([h for h in utils.logger.handlers
                             if isinstance(h, NullHandler)]) == 1)
        utils.enable_logger(utils.logger)
        utils.enable_logger(utils.logger)
        self.assertTrue(len([h for h in utils.logger.handlers
                             if not isinstance(h, NullHandler)]) == 1)
        utils.enable_debug_logger()
        self.assertEqual(utils.logger.level, DEBUG)
        utils.logger.handlers = [NullHandler()]

    # https://github.com/ParallelSSH/ssh2-python/blob/master/tests/test_utils.py

    def test_find_eol_no_lines(self):
        buf = b"a buffer"
        linepos, new_line_pos = find_eol(buf, 0)
        self.assertEqual(linepos, -1)
        self.assertEqual(new_line_pos, 0)

    def test_read_line(self):
        lines = [b'a line', b'another line', b'third']
        buf = b"\n".join(lines)
        pos = 0
        line_num = 0
        linesep, new_line_pos = find_eol(buf, 0)
        self.assertTrue(linesep > 0)
        self.assertTrue(linesep < len(buf))
        while pos < len(buf):
            if linesep < 0:
                break
            end_of_line = pos + linesep
            line = buf[pos:end_of_line]
            self.assertEqual(lines[line_num], line)
            pos += linesep + new_line_pos
            line_num += 1
            linesep, new_line_pos = find_eol(buf, pos)
        line = buf[pos:]
        self.assertEqual(lines[line_num], line)

    def test_read_line_crnl(self):
        lines = [b'a line', b'another line', b'third']
        buf = b"\r\n".join(lines)
        pos = 0
        line_num = 0
        linesep, new_line_pos = find_eol(buf, 0)
        self.assertTrue(linesep > 0)
        self.assertTrue(linesep < len(buf))
        while pos < len(buf):
            if linesep < 0:
                break
            end_of_line = pos + linesep
            line = buf[pos:end_of_line]
            self.assertEqual(lines[line_num], line)
            pos += linesep + new_line_pos
            line_num += 1
            linesep, new_line_pos = find_eol(buf, pos)
        line = buf[pos:]
        self.assertEqual(lines[line_num], line)

    def test_read_line_cr_only(self):
        lines = [b'a line', b'another line', b'third']
        buf = b"\r".join(lines)
        linesep, new_line_pos = find_eol(buf, 0)
        self.assertEqual(linesep, -1)

    def test_read_line_bad_data(self):
        linesep, new_line_pos = find_eol(b"", 0)
        self.assertEqual(linesep, -1)
        self.assertEqual(new_line_pos, 0)
        linesep, new_line_pos = find_eol(b'\n', 0)
        self.assertEqual(linesep, 0)
        self.assertEqual(new_line_pos, 1)
        linesep, new_line_pos = find_eol(b'\r\n', 0)
        self.assertEqual(linesep, 0)
        self.assertEqual(new_line_pos, 2)
        linesep, new_line_pos = find_eol(b'\r', 0)
        self.assertEqual(linesep, -1)
        self.assertEqual(new_line_pos, 0)

    # This fails in the c implementation
    def test_read_line_with_nulls(self):
        lines = [b'a l\0ine', b'anot\0her line', b'thi\0rd']
        buf = b"\n".join(lines)
        pos = 0
        line_num = 0
        linesep, new_line_pos = find_eol(buf, 0)
        self.assertTrue(linesep > 0)
        self.assertTrue(linesep < len(buf))
        while pos < len(buf):
            if linesep < 0:
                break
            end_of_line = pos + linesep
            line = buf[pos:end_of_line]
            self.assertEqual(lines[line_num], line)
            pos += linesep + new_line_pos
            line_num += 1
            linesep, new_line_pos = find_eol(buf, pos)
        line = buf[pos:]
        self.assertEqual(lines[line_num], line)

    # This is not supported in the c implementation
    def test_read_line_nlcr(self):
        lines = [b'a line', b'another line', b'third']
        buf = b"\n\r".join(lines)
        pos = 0
        line_num = 0
        linesep, new_line_pos = find_eol(buf, 0)
        self.assertTrue(linesep > 0)
        self.assertTrue(linesep < len(buf))
        while pos < len(buf):
            if linesep < 0:
                break
            end_of_line = pos + linesep
            line = buf[pos:end_of_line]
            self.assertEqual(lines[line_num], line)
            pos += linesep + new_line_pos
            line_num += 1
            linesep, new_line_pos = find_eol(buf, pos)
        line = buf[pos:]
        self.assertEqual(lines[line_num], line)
