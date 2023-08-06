# -*- coding: UTF-8 -*-
"""
An utility package
"""

__author__ = "the01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2013-16, Florian JUNG"
__license__ = "MIT"
__version__ = "0.3.1a0"
__date__ = "2016-03-31"

import logging

from .loadable import Loadable, loadJSON, saveJSON, loadJSONFile, saveJSONFile
from .logable import Logable, ModuleLogable
from .runable import StartStopable, Startable, Stopable, StartException


logger = logging.getLogger(__name__)
__all__ = ["logable", "loadable", "runable"]
