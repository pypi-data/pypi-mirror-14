#!/usr/bin/python
# -*- coding: utf-8 -*-

""""
Copyright (c) 2014, Matt Doiron. All rights reserved.

BTCnDash is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BTCnDash is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BTCnDash. If not, see <http://www.gnu.org/licenses/>.
"""

# System Imports
import threading
import atexit

# BTCnDash Imports
import page_cache
import logger


class Worker(object):
    """Creates the worker thread, which refreshes the page cache."""

    def __init__(self, config):
        self.config = config
        self.log = logger.setup_logging(self.config['log_level'], __name__)
        self.log.info('Launching worker...')
        self.worker_thread = threading.Thread()
        self.refresh_cache()

    def interrupt(self):
        self.worker_thread.cancel()

    def refresh_cache(self):
        # Call PageCache object to check cache freshness
        page_cache.PageCache(self.config)

        try:
            # Set the next thread to start in cache_time seconds
            self.worker_thread = threading.Timer(self.config['cache_time'], self.refresh_cache, ())
            self.worker_thread.daemon = True
            self.worker_thread.start()

            # When you kill the program (SIGTERM), clear the next timer
            atexit.register(self.interrupt)

        except (KeyboardInterrupt, SystemExit):
            self.interrupt()
