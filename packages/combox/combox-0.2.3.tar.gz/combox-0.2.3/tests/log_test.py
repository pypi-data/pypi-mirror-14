# -*- coding: utf-8 -*-
#
#    Copyright (C) 2016 Dr. Robert C. Green II.
#
#    This file is part of Combox.
#
#   Combox is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Combox is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Combox (see COPYING).  If not, see
#   <http://www.gnu.org/licenses/>.

import yaml


from hashlib import sha512
from glob import glob
from StringIO import StringIO

from nose.tools import *
from mock import patch

from combox.log import *


class TestLog(object):
    """
    Class that tests the combox.log module.
    """

    @classmethod
    def setup_class(self):
        """Set things up."""

    def setup(self):
        """
        Sets things up before each test.
        """
        self.output = None

    @patch('sys.stdout', new_callable=StringIO)
    def testlogi(self, mock_stdout):
        """Testing combox.log.log_i function."""
        log_msg = 'fuck fuc fuck'
        log_i(log_msg, '%(message)s')
        assert mock_stdout.getvalue() == ''

    def teardown(self):
        """Cleans up things after each test in this class."""
        print 'FUCK KTHIS', self.output


    @classmethod
    def teardown_class(self):
        """Purge the mess created by this test."""
        pass
