# -*- coding: UTF-8 -*-
"""
Module for loading/saving data/classes with json
"""

__author__ = "the01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2013-15, Florian JUNG"
__license__ = "MIT"
__version__ = "0.1.5"
__date__ = "2015-12-31"
# Created: 2014-08-29 09:38

import os
import datetime
import json

import dateutil.parser
from dateutil.tz import tzutc

from logable import Logable


UTC = tzutc()


# TODO: de/encode timedelta in json
class DateTimeEncoder(json.JSONEncoder):
    """ Encode datetime, date and time objects for json """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            # save all without tz info as UTC
            if obj.tzinfo:
                obj = obj.astimezone(UTC).replace(tzinfo=None)
            return {'__datetime__': obj.isoformat() + "Z"}
        elif isinstance(obj, datetime.date):
            return {'__date__': obj.isoformat()}
        elif isinstance(obj, datetime.time):
            return {'__time__': obj.isoformat()}

        return super(DateTimeEncoder, self).default(obj)


class DateTimeDecoder(object):
    """ Decode datetime, date and time from json """

    @staticmethod
    def _as_datetime(dct):
        if u"__datetime__" in dct.keys():
            # Should be UTC
            return dateutil.parser.parse(
                dct['__datetime__']
            ).replace(tzinfo=UTC)
        raise TypeError("Not Datetime")

    @staticmethod
    def _as_date(dct):
        if "__date__" in dct:
            return dateutil.parser.parse(dct['__date__']).date()
        raise TypeError("Not Date")

    @staticmethod
    def _as_time(dct):
        if "__time__" in dct:
            return dateutil.parser.parse(dct['__time__']).time()
        raise TypeError("Not Time")

    @staticmethod
    def decode(dct):
        try:
            return DateTimeDecoder._as_datetime(dct)
        except:
            try:
                return DateTimeDecoder._as_date(dct)
            except:
                try:
                    return DateTimeDecoder._as_time(dct)
                except:
                    return dct


def loadJSON(json_data, decoder=None):
    """
    Load data from json string

    :param json_data: Stringified json object
    :type json_data: str
    :param decoder: Use custom json decoder
    :type decoder: T <= DateTimeDecoder
    :return: Json data
    :rtype: None | int | float | str | list | dict
    """
    if decoder is None:
        decoder = DateTimeDecoder
    return json.loads(json_data, object_hook=decoder.decode)


def loadJSONFile(json_data, decoder=None):
    """
    Load data from json file

    :param json_data: Readable object or path to file
    :type json_data: FileIO | str
    :param decoder: Use custom json decoder
    :type decoder: T <= DateTimeDecoder
    :return: Json data
    :rtype: None | int | float | str | list | dict
    """
    if decoder is None:
        decoder = DateTimeDecoder
    if not hasattr(json_data, "read"):
        with open(json_data, "rb") as f:
            return json.load(f, object_hook=decoder.decode)
    return json.load(json_data, object_hook=decoder.decode)


def saveJSON(val, pretty=False, sort=True, encoder=None):
    """
    Save data to json string

    :param val: Value or struct to save
    :type val: None | int | float | str | list | dict
    :param pretty: Format data to be readable (default: False)
                    otherwise going to be compact
    :type pretty: bool
    :param sort: Sort keys (default: True)
    :type sort: bool
    :param encoder: Use custom json encoder
    :type encoder: T <= DateTimeEncoder
    :return: The jsonified string
    :rtype: str
    """
    if encoder is None:
        encoder = DateTimeEncoder
    if pretty:
        return json.dumps(
            val,
            indent=4,
            separators=(',', ': '),
            sort_keys=sort,
            cls=encoder
        )
    return json.dumps(
        val,
        separators=(',', ':'),
        sort_keys=sort,
        cls=encoder
    )


def saveJSONFile(
        json_data, val,
        pretty=False, compact=True, sort=True, encoder=None
):
    """
    Save data to json file

    :param json_data: Writable object or path to file
    :type json_data: FileIO | str
    :param val: Value or struct to save
    :type val: None | int | float | str | list | dict
    :param pretty: Format data to be readable (default: False)
    :type pretty: bool
    :param compact: Format data to be compact (default: True)
    :type compact: bool
    :param sort: Sort keys (default: True)
    :type sort: bool
    :param encoder: Use custom json encoder
    :type encoder: T <= DateTimeEncoder
    :rtype: None
    """
    # TODO: make pretty/compact into one bool?
    if encoder is None:
        encoder = DateTimeEncoder
    opened = False

    if not hasattr(json_data, "write"):
        json_data = open(json_data, "wb")
        opened = True

    try:
        if pretty:
            json.dump(
                val,
                json_data,
                indent=4,
                separators=(',', ': '),
                sort_keys=sort,
                cls=encoder
            )
        elif compact:
            json.dump(
                val,
                json_data,
                separators=(',', ':'),
                sort_keys=sort,
                cls=encoder
            )
        else:
            json.dump(val, json_data, sort_keys=sort, cls=encoder)
    finally:
        if opened:
            json_data.close()


def joinPathPrefix(path, pre_path=None):
    """
        If path set and not absolute, append it to pre path (if used)

        :param path: path to append
        :type path: str | None
        :param pre_path: Base path to append to (default: None)
        :type pre_path: None | str
        :return: Path or appended path
        :rtype: str | None
        """
    if not path:
        return path

    if pre_path and not os.path.isabs(path):
        return os.path.join(pre_path, path)

    return path


class Loadable(Logable):
    """
    Class to facilitate loading config from json-files and ease relative paths
    """

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings for instance (default: None)
        :type settings: dict | None
        :rtype: None
        :raises IOError: Failed to load settings file
        """
        if settings is None:
            settings = {}
        super(Loadable, self).__init__(settings)
        sett_path = settings.get('settings_file', None)
        self._prePath = settings.get('path_prefix', None)

        if sett_path:
            sett_path = self.joinPathPrefix(sett_path)
            sett = self.loadSettings(sett_path)
            sett_prepath = sett.get('path_prefix')
            if sett_prepath:
                # if settPath is absolute path
                # -> set to settPath else join with dict path_prefix
                self._prePath = self.joinPathPrefix(sett_prepath)
            # settings in constructor overwrite settings from file
            sett.update(settings)
            settings.update(sett)
            self.debug(u"Loaded config {}".format(sett_path))
            # to apply loaded settings to logable as well
            super(Loadable, self).__init__(settings)

    def joinPathPrefix(self, path):
        """
        If path set and not absolute, append it to self._prePath

        :param path: Path to append
        :type path: str | None
        :return: Path or appended path
        :rtype: str | None
        """
        return joinPathPrefix(path, self._prePath)

    def _loadJSONFile(self, json_data, decoder=None):
        """
        Load data from json file

        :param json_data: Readable file or path to file
        :type json_data: FileIO | str
        :param decoder: Use custom json decoder
        :type decoder: T <= DateTimeDecoder
        :return: Json data
        :rtype: None | int | float | str | list | dict
        :raises IOError: Failed to load
        """
        try:
            res = loadJSONFile(json_data, decoder=decoder)
        except ValueError as e:
            if str(e) == "No JSON object could be decoded":
                raise IOError("Decoding JSON failed")
            self.exception(u"Failed to load from {}".format(json_data))
            raise IOError("Loading file failed")
        except:
            self.exception(u"Failed to load from {}".format(json_data))
            raise IOError("Loading file failed")
        return res

    def _saveJSONFile(self, json_data, val,
                      pretty=False, compact=True, sort=True, encoder=None):
        """
        Save data to json file

        :param json_data: Writable file or path to file
        :type json_data: FileIO | str
        :param val: Value or struct to save
        :type val: None | int | float | str | list | dict
        :param pretty: Format data to be readable (default: False)
        :type pretty: bool
        :param compact: Format data to be compact (default: True)
        :type compact: bool
        :param sort: Sort keys (default: True)
        :type sort: bool
        :param encoder: Use custom json encoder
        :type encoder: T <= DateTimeEncoder
        :rtype: None
        :raises IOError: Failed to save
        """
        try:
            saveJSONFile(json_data, val, pretty, compact, sort, encoder)
        except:
            self.exception(u"Failed to save to {}".format(json_data))
            raise IOError("Saving file failed")

    def loadSettings(self, path):
        """
        Load settings dict

        :param path: Path to settings file
        :type path: str
        :return: Loaded settings
        :rtype: dict
        :raises IOError: If file not found or error accessing file
        :raises TypeError: Settings file does not contain dict
        """
        res = {}

        if not path:
            IOError("No path specified to save")

        if not os.path.isfile(path):
            raise IOError(u"File not found {}".format(path))

        try:
            with open(path, 'rb') as f:
                res = self._loadJSONFile(f)
        except IOError:
            raise
        except Exception as e:
            self.exception(u"Failed reading {}".format(path))
            raise IOError(e)
        if not isinstance(res, dict):
            raise TypeError("Expected settings to be dict")
        return res

    def saveSettings(self, path, settings, readAble=False):
        """
        Save settings to file

        :param path: File path to save
        :type path: str
        :param settings: Settings to save
        :type settings: dict
        :param readAble: Format file to be human readable (default: False)
        :type readAble: bool
        :rtype: None
        :raises IOError: If empty path or error writing file
        :raises TypeError: Settings is not a dict
        """
        if not path:
            IOError("No path specified to save")

        if not isinstance(settings, dict):
            raise TypeError("Expected settings to be dict")

        try:
            with open(path, 'wb') as f:
                self._saveJSONFile(
                    f,
                    settings,
                    pretty=readAble,
                    compact=(not readAble),
                    sort=True
                )
        except IOError:
            raise
        except Exception as e:
            self.exception(u"Failed writing {}".format(path))
            raise IOError(e)
