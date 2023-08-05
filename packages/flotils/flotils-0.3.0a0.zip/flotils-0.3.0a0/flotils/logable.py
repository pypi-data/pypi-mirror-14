# -*- coding: UTF-8 -*-
"""
Logging utilities
"""

__author__ = "the01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2013-16, Florian JUNG"
__license__ = "MIT"
__version__ = "0.1.4"
__date__ = "2016-03-02"
# Created: 2013-03-03 24:00

import logging
import inspect

try:
    import colorlog
except ImportError:
    colorlog = None


TIMEFORMAT_DEFAULT = "%Y-%m-%d %H:%M:%S"


class FunctionFilter(logging.Filter):
    """
    Add an extra 'function' if not already present
    """

    def filter(self, record):
        if not hasattr(record, "function"):
            record.function = ""
        else:
            fct = record.function

            if fct and not fct.startswith("."):
                record.function = u"." + fct
        return True


class Logable(object):
    """
    Class to facilitate clean logging with class/function/id information
    """

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings for instance (default: None)
        :type settings: dict | None
        :rtype: None
        """
        if settings is None:
            settings = {}
        super(Logable, self).__init__()
        self._id = settings.get('id', None)
        """ instance id """
        self._logger = logging.getLogger(self.name)

    @property
    def name(self):
        """
        Get the module name

        :return: Module name
        :rtype: str
        """
        res = type(self).__name__
        if self._id:
            res += u".{}".format(self._id)
        return res

    def _get_function_name(self):
        """
        Get function name of calling method

        :return: The name of the calling function
            (expected to be called in self.error/debug/..)
        :rtype: str
        """
        fname = inspect.getframeinfo(inspect.stack()[2][0]).function
        if fname == "<module>":
            return u""
        else:
            return fname

    def log(self, level, msg, *args, **kargs):
        self._logger.log(
            level, msg,
            extra={'function': self._get_function_name()},
            *args, **kargs
        )

    def logException(self, e):
        # deprecated
        import warnings
        warnings.warn(
            "This method is no longer in use"
            " - Please use .exception() instead",
            DeprecationWarning
        )
        self._logger.exception(e)

    def exception(self, msg, *args, **kwargs):
        self._logger.exception(
            msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(
            msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )

    def info(self, msg, *args, **kwargs):
        self._logger.info(
            msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )

    def warn(self, msg, *args, **kwargs):
        # deprecated
        import warnings
        warnings.warn(
            "This method is no longer in use - Please use .warning() instead",
            DeprecationWarning
        )
        self._logger.warning(
            msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(
            msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )

    def error(self, msg, *args, **kwargs):
        self._logger.error(
            msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )

    def critical(self, msg, *args, **kwargs):
        self._logger.critical(
            msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )

    def fatal(self, msg, *args, **kwargs):
        self._logger.fatal(
            msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )


class ModuleLogable(Logable):
    """ Class to log on module level """

    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        super(ModuleLogable, self).__init__(settings)

    @property
    def name(self):
        return type(self).__module__


default_logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "threaded": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d "
                      "%(thread)d %(message)s"
        },
        "verbose": {
            "format": "%(asctime)s %(levelname)-8s [%(name)s%(function)s] "
                      "%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format":
                "%(blue,bold)s%(asctime)s%(reset)s "
                "%(log_color)s%(levelname)-8s%(reset)s"
                "%(blue)s[%(name)s%(function)s]%(reset)s "
                  "%(message_log_color)s%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "white,bg_yellow",
                "ERROR": "yellow,bg_red",
                "CRITICAL": "yellow,bg_red"
            },
            "secondary_log_colors": {
                "message": {
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white"
                }
            }
        },
        "simple": {
            "format": "%(levelname)s %(message)s"
        }
    },
    "filters": {
        "my": {
            "()": "flotils.logable.FunctionFilter"
        }
    },
    "handlers": {
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
            "filters": ["my"]
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "filters": ["my"]
        }
    },
    "loggers": {
        "": {
            "handlers": [
                "console"
            ],
            "propagate": True,
            "level": "INFO"
        }
    }
}

# try to use colorlog as default -> if not installed, fallback solution
if colorlog is None:
    del default_logging_config['formatters']['colored']
    default_logging_config['handlers']['console']['formatter'] = "verbose"
