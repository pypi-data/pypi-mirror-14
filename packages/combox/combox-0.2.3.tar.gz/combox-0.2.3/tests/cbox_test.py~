# -*- coding: utf-8 -*-
#
#    Copyright (C) 2015 Combox contributor(s). See CONTRIBUTORS.rst.
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

import os
import time
import yaml

from filecmp import cmp
from glob import glob
from os import path, remove
from shutil import copyfile
from threading import Lock, Thread

from nose.tools import *
from watchdog.observers import Observer

from combox import cbox
from combox.cbox import run_cb
from combox.config import get_nodedirs

from combox.silo import ComboxSilo
from tests.utils import (get_config, shardedp, dirp, renamedp,
                         path_deletedp, rm_nodedirs, rm_configdir,
                         purge_nodedirs, purge)



class TestCbox(object):
    """
    Class that tests the combox.cbox module.
    """

    @classmethod
    def setup_class(self):
        """Set things up for testing combox.cbox module"""
        self.config = get_config()


    def exec_runcb(self):
        run_cb(self.config)


    def untest_runcb(self):
        """Tests run_cb function"""

        # start a new thread that run the run_cb function.
        #t_runcb = Thread(target=self.exec_runcb)
        #t_runcb.start()
        self.exec_runcb()
        #t_runcb.join()
        #raise KeyboardInterrupt, "Zark it"


    def teardown(self):
        """Cleans up things after each test in this class"""
        purge_nodedirs(self.config)

    @classmethod
    def teardown_class(self):
        """Purge the mess created by this test"""
        rm_nodedirs(self.config)
        rm_configdir()
