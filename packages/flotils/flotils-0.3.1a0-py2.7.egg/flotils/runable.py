# -*- coding: UTF-8 -*-
"""
Module for runable interfaces
"""

__author__ = "the01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2015-16, Florian JUNG"
__license__ = "All rights reserved"
__version__ = "0.1.1a0"
__date__ = "2016-03-31"
# Created: 2015-06-07 15:00

from abc import ABCMeta, abstractmethod
import time
import signal

from .logable import Logable


class StartException(Exception):
    pass


class Startable(object):
    """
    Abstract interface to add a start method
    """
    __metaclass__ = ABCMeta

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings to be passed for init (default: None)
        :type settings: dict | None
        :rtype: None
        """
        if settings is None:
            settings = {}
        super(Startable, self).__init__()

    @abstractmethod
    def start(self):
        """
        Start the interface

        :rtype: None
        """
        pass


class Stopable(object):
    """
    Abstract interface to add a stop method
    """
    __metaclass__ = ABCMeta

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings to be passed for init (default: None)
        :type settings: dict | None
        :rtype: None
        """
        if settings is None:
            settings = {}
        super(Stopable, self).__init__()

    @abstractmethod
    def stop(self):
        """
        Stop the interface

        :rtype: None
        """
        pass


class StartStopable(Startable, Stopable):
    """
    Abstract interface to add a start/stop method (e.g. for threading)
    """
    __metaclass__ = ABCMeta

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings to be passed for init (default: None)
        :type settings: dict | None
        :rtype: None
        """
        if settings is None:
            settings = {}
        super(StartStopable, self).__init__(settings)
        self._is_running = False
        """ Indicate whether this object is currently running
            :type _running: bool """
        self._start_block_timeout = settings.get('start_blocking_timeout', 1.0)
        """ Timeout used to sleep in blocking loop (in seconds) """

    def start(self, blocking=False):
        """
        Start the interface

        :param blocking: Should the call block until stop() is called
            (default: False)
        :type blocking: bool
        :rtype: None
        """
        super(StartStopable, self).start()
        self._is_running = True
        # blocking
        try:
            while blocking and self._is_running:
                time.sleep(self._start_block_timeout)
        except IOError as e:
            if not str(e).lower().startswith("[errno 4]"):
                raise

    def stop(self):
        """
        Stop the interface

        :rtype: None
        """
        self._is_running = False
        super(StartStopable, self).stop()


class SignalStopWrapper(Logable, Stopable):
    """
    Catch SIGINT and SIGTERM to smoothly stop running
    """
    __metaclass__ = ABCMeta

    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        super(SignalStopWrapper, self).__init__(settings)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        self.info("Catching SIGINT and SIGTERM")

    def _signal_handler(self, sig, frame):
        self.warning(u"Signal {} caught".format(sig))
        self.stop()
