# -*- coding: UTF-8 -*-
"""
Module for loading/scraping data from the web
"""

__author__ = "the01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2013-16, Florian JUNG"
__license__ = "MIT"
__version__ = "0.1.6"
__date__ = "2016-01-07"
# Created: 2014-04-02 11:23

import logging
import os
import re
import datetime
import threading
import hashlib
import socket

from dateutil.tz import tzutc
import codecs
from bs4 import BeautifulSoup
import html2text
import requests
from requests import HTTPError
from requests.exceptions import SSLError, Timeout, ConnectionError

try:
    import portalocker as porta
except ImportError as e:
    # not using portalocker
    porta = None

from .loadable import Loadable
from .default_user_agents import default_user_agents
from .logable import ModuleLogable


class Logger(ModuleLogable):
    pass


logger = Logger()
UTC = tzutc()
_cache = {}
""" temp cache """
_cache_lock = threading.RLock()

if porta is None:
    logger.warning("Not using portalocker")


class WEBParameterException(Exception):
    """ Parameter Exception """
    pass


class WEBFileException(IOError):
    """ File Exception """
    pass


class WEBConnectException(Exception):
    """ Error with web connection """
    pass


class WebScraper(Loadable):
    """ Class for cached, session get/post/.. with optional scraping """

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings for instance (default: None)
        :type settings: dict | None
        :rtype: None
        """
        if settings is None:
            settings = {}
        super(WebScraper, self).__init__(settings)

        self._url = settings.get('url', None)
        self._scheme = settings.get('scheme', None)
        self._timeout = settings.get('timeout', None)
        self._cacheDir = settings.get('cache_directory', None)
        self._cacheIndex = None
        with _cache_lock:
            self._cacheIndex = _cache

        self._cacheTime = datetime.timedelta(
            seconds=settings.get('cache_time', 7 * 60)
        )
        self._cacheUseAdvanced = settings.get('cache_use_advanced', True)

        self._authMethod = settings.get('auth_method', None)
        self._authUsername = settings.get('auth_username', None)
        self._authPassword = settings.get('auth_password', None)

        # TODO: needs to be done outside?
        if self._cacheDir:
            self._cacheDir = self.joinPathPrefix(self._cacheDir)

        self._br = None
        """ object to do http actions
            :type _br: request.Session """
        self._brHandleRedirect = settings.get('handle_redirect', True)

        agentBrowser = default_user_agents['browser']['keith']
        agentOS = default_user_agents['os']['linux_i686']
        agent = settings.get('user_agent', None)

        if "default_user_agents_browser" in settings:
            brow = settings['default_user_agents_browser']
            agentBrowser = default_user_agents['browser'].get(brow, None)
        if "default_user_agents_os" in settings:
            os = settings['default_user_agents_os']
            agentOS = default_user_agents['os'].get(os, None)
        if "user_agent_browser" in settings:
            agentBrowser = settings['user_agent_browser']
        if "user_agent_os" in settings:
            agentOS = settings['user_agent_os']

        if not agent:
            if agentBrowser and agentOS:
                agent = agentBrowser.format(agentOS)
        self._brUserAgent = agent
        self._text_maker = None
        """ object to translate html to markdown (html2text)
            :type _text_maker: None | html2text.HTML2Text """
        if settings.get('html2text'):
            self._set_html2text(settings['html2text'])
        self._html_parser = settings.get('html_parser', "html.parser")
        """ what html parser to use (default: html.parser - built in)
            :type _html_parser: str """

    def _browser_init(self):
        """
        Init the browsing instance if not setup

        :rtype: None
        """
        if self._br:
            return

        self._br = requests.Session()
        headers = {}

        if self._brUserAgent:
            headers['User-agent'] = self._brUserAgent
        self._br.headers.update(headers)

        if self._authMethod in [None, "", "HTTPBasicAuth"]:
            if self._authUsername is not None:
                self._br.auth = (self._authUsername, self._authPassword)

    def _set_html2text(self, settings):
        """
        Load settings for html2text (https://github.com/Alir3z4/html2text)

        Warning: does not check options/values

        :param settings: Settings for the object
            (see:https://github.com/Alir3z4/html2text/blob/master/docs/usage.md)
        :type settings: dict
        :rtype: None
        """
        self._text_maker = html2text.HTML2Text()
        for param in settings:
            if not hasattr(self._text_maker, param):
                raise WEBParameterException(
                    u"Setting html2text failed - "
                    u"unknown parameter {}".format(param)
                )
            setattr(self._text_maker, param, settings[param])

    def loadScrap(self, path):
        """
        Load scraper settings from file

        :param path: Path to file
        :type path: str
        :rtype: None
        :raises WEBFileException: Failed to load settings
        :raises WEBParameterException: Missing parameters in file
        """
        try:
            conf = self._loadJSONFile(path)
        except Exception:
            # should only be IOError
            self.exception("Failed to load file")
            raise WEBFileException(u"Failed to load from {}".format(path))

        if "scheme" not in conf:
            raise WEBParameterException("Missing scheme definition")
        if "url" not in conf:
            raise WEBParameterException("Missing url definition")
        version = conf.get('version', None)
        if version != "1.0":
            raise WEBParameterException(
                u"Unsupported version {}".format(version)
            )
        self._scheme = conf['scheme']
        self._url = conf['url']
        self._timeout = conf.get('timeout', self._timeout)
        if "cache_directory" in conf:
            self._cacheDir = conf['cache_directory']
        if "cache_time" in conf:
            self._cacheTime = conf['cache_time']
        if self._cacheTime and not isinstance(
                self._cacheTime, datetime.timedelta):
            self._cacheTime = datetime.timedelta(seconds=self._cacheTime)
        if conf.get('html2text'):
            self._set_html2text(conf['html2text'])

    def _getCached(self, url, ignoreAccessTime=False):
        """
        Try to retrieve url from cache if available

        :param url: Url to retrieve
        :type url: str
        :param ignoreAccessTime: Should ignore the access time
        :type ignoreAccessTime: bool
        :return: (data, Accessed Time, ETag)
            None, None, None -> not found in cache
            None, Accessed Time, ETag -> found, but is expired
            data, Accessed Time, ETag -> found in cache
        :rtype: (None | str, None | datetime.datetime, None | str)
        """
        if not self._cacheDir:
            self.debug(u"From inet {}".format(url))
            return None, None, None

        if not self._cacheIndex:
            try:
                with open(
                        os.path.join(self._cacheDir, "cache_index.tmp"),
                        'rb'
                ) as f:
                    if porta:
                        porta.lock(f, porta.LOCK_EX)
                    self._cacheIndex = self._loadJSONFile(
                        os.path.join(self._cacheDir, "cache_index.tmp")
                    )
            except IOError as e:
                if str(e) != "Decoding json failed":
                    self.exception("Failed to load cache file")
            except:
                self.exception("Failed to load cache file")

        if not self._cacheIndex:
            self._cacheIndex = {'version': "1.0"}

        key = hashlib.md5(url).hexdigest()
        with _cache_lock:
            _cache.update(self._cacheIndex)
            accessed = _cache.get(key, None)
        eTag = None

        if not accessed:
            # not previously cached
            self.debug(u"From inet {}".format(url))
            return None, None, None

        if isinstance(accessed, dict):
            eTag = accessed['ETag']
            accessed = accessed['accessTime']
        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        if now - accessed > self._cacheTime and not ignoreAccessTime:
            # cached expired -> remove
            # del self._cacheIndex[key]
            # try:
            #    os.remove(os.path.join(self._cacheDir, key + ".tmp"))
            # except Exception:
            #    pass
            self.debug(u"From inet (expired) {}".format(url))
            return None, accessed, eTag

        res = None

        try:
            with codecs.open(
                    os.path.join(self._cacheDir, key + ".tmp"),
                    "rb", "utf-8") as f:
                if porta:
                    porta.lock(f, porta.LOCK_EX)
                res = f.read()
        except:
            self.exception("Failed to read cached file")
            self.debug(u"From inet (failure) {}".format(url))
            return None, None, None
        self.debug(u"From cache {}".format(url))
        return res, accessed, eTag

    def _updateCache(self, url, accessTime=None, eTag=None):
        """
        Update cache information for url

        :param url: Update for this url
        :type url: str
        :param accessTime: Time of last access (default: None)
            if None -> use current time
        :type accessTime: None | datetime.datetime
        :param eTag: ETag information (default: None)
        :type eTag: None | str
        :rtype: None
        """
        key = hashlib.md5(url).hexdigest()
        if not accessTime:
            accessTime = datetime.datetime.utcnow().replace(tzinfo=UTC)
        cache_dict = accessTime
        if eTag is not None:
            cache_dict = {
                'accessTime': accessTime,
                'ETag': eTag
            }
        self._cacheIndex[key] = cache_dict
        with _cache_lock:
            _cache[key] = cache_dict

    def _putCached(self, url, html, eTag=None):
        """
        Put response into cache

        :param url: Url to cache
        :type url: str
        :param html: HTML content of url
        :type html: str
        :param eTag: ETag information (default: None)
        :type eTag: None | str
        :rtype: None
        """
        if not self._cacheDir or not html:
            return
        key = hashlib.md5(url).hexdigest()

        try:
            with codecs.open(
                    os.path.join(self._cacheDir, key + ".tmp"),
                    "wb",
                    "utf-8") as f:
                if porta:
                    porta.lock(f, porta.LOCK_EX)
                f.write(html)
                # try flushing to make data available sooner
                # (try to get rid of erroneous reads)
                f.flush()
        except:
            self.exception("Failed to write cached file")
            return
        self._updateCache(url, eTag=eTag)

        # better in a close statement?
        try:
            with open(
                os.path.join(self._cacheDir, "cache_index.tmp"),
                "wb"
            ) as f, _cache_lock:
                if porta:
                    porta.lock(f, porta.LOCK_EX)
                self._saveJSONFile(
                    os.path.join(self._cacheDir, "cache_index.tmp"),
                    _cache
                )
                # try flushing to make data available sooner
                # (try to get rid of erroneous reads)
                f.flush()
        except:
            self.exception("Failed to save cache")

    def _request(
            self, method, url, timeout=None,
            headers=None, data=None, params=None
    ):
        """
        Make a request using the requests library

        :param method: Which http method to use (GET/POST)
        :type method: str
        :param url: Url to make request to
        :type url: str
        :param timeout: Timeout for request (default: None)
            None -> infinite timeout
        :type timeout: None | int | float
        :param headers: Headers to be passed along (default: None)
        :type headers: None | dict
        :param data: Data to be passed along (e.g. body in POST)
            (default: None)
        :type data: None | dict
        :param params: Parameters to be passed along (e.g. with url in GET)
            (default: None)
        :type params: None | dict
        :return: Response to the request
        :rtype: requests.Response
        :raises WEBConnectException: Loading failed
        """
        if headers is None:
            headers = {}
        if not self._br:
            self._browser_init()

        try:
            response = self._br.request(
                method,
                url,
                timeout=timeout,
                allow_redirects=self._brHandleRedirect,
                headers=headers,
                data=data,
                params=params
            )
        except SSLError as e:
            raise WEBConnectException(u"{}".format(e))
        except HTTPError:
            raise WEBConnectException(u"Unable to load {}".format(url))
        except (Timeout, socket.timeout):
            raise WEBConnectException(u"Timeout loading {}".format(url))
        except ConnectionError:
            raise WEBConnectException(u"Failed to load {}".format(url))
        except Exception:
            self.exception(u"Failed to load {}".format(url))
            raise WEBConnectException(
                u"Unknown failure loading {}".format(url)
            )
        return response

    def _get(self, url, **kwargs):
        """
        Make GET request

        :param url: Url to make the request to
        :type url: str
        :param kwargs: See _requests for parameters
        :type kwargs: dict
        :return: Response
        :rtype: requests.Response
        """
        return self._request("GET", url, **kwargs)

    def _post(self, url, **kwargs):
        """
        Make POST request

        :param url: Url to make the request to
        :type url: str
        :param kwargs: See _requests for parameters
        :type kwargs: dict
        :return: Response
        :rtype: requests.Response
        """
        return self._request("POST", url, **kwargs)

    def get(self, url, timeout=None, headers=None, params=None):
        """
        Make get request to url (might use cache)

        :param url: Url to make request to
        :type url: str
        :param timeout: Timeout for request (default: None)
            None -> infinite timeout
        :type timeout: None | int | float
        :param headers: Headers to be passed along (default: None)
        :type headers: None | dict
        :param params: Parameters to be passed along with url (default: None)
        :type params: None | dict
        :return: Html response
        :rtype: str
        :raises WEBConnectException: Loading failed
        """
        if headers is None:
            headers = {}
        cached, accessed_time, etag = self._getCached(url)

        if cached:
            # Using cached
            return cached
        # Not using cached

        if not self._br:
            self._browser_init()

        if self._cacheUseAdvanced:
            if accessed_time and "If-Modified-Since" not in headers.keys():
                headers['If-Modified-Since'] = accessed_time.strftime(
                    "%a, %d %b %Y %H:%M:%S GMT"
                )
            if etag and "If-None-Match" not in headers.keys():
                headers['If-None-Match'] = etag

        response = self._get(
            url,
            timeout=timeout,
            headers=headers,
            params=params
        )
        etag = response.headers.get('etag', etag)

        if response.history:
            # list of responses in redirects
            code = 0

            for resp in response.history + [None]:
                if resp is None:
                    resp = response
                if code in [requests.codes.found,
                            requests.codes.see_other,
                            requests.codes.temporary_redirect
                            ]:
                    self.info(
                        u"Temporary redirect to {}".format(resp.url)
                    )
                elif code in [requests.codes.moved_permanently,
                              requests.codes.permanent_redirect]:
                    self.warning(u"Moved to {}".format(resp.url))
                elif code != 0:
                    self.error(u"Code {} to {}".format(code, resp.url))
                code = resp.status_code

        if response.status_code == requests.codes.not_modified:
            self.info(u"Not modified {}".format(url))
            cached, _, _ = self._getCached(url, ignoreAccessTime=True)
            self._updateCache(url, eTag=etag)
            return cached

        try:
            response.raise_for_status()
        except HTTPError as e:
            raise WEBConnectException(u"{} - {}".format(e, url))

        try:
            html = response.text
            if html is None:
                self.warning("Response returned None")
                raise Exception()
        except Exception:
            raise WEBConnectException(u"Unable to load {}".format(url))

        self._putCached(url, html, eTag=etag)
        if url != response.url:
            if not response.history:
                self.warning(
                    u"Response url different despite no redirects "
                    u"{} - {}".format(url, response.url))
            self._putCached(response.url, html, eTag=etag)
        return html

    def _getTagMatch(self, ele, tree):
        """

        :param ele: 
        :type ele: 
        :param tree: 
        :type tree: 
        :return: 
        :rtype: None | list
        """
        # self.debug(u"ele={}".format(ele.name))

        if tree in [None, []]:
            return [ele]

        res = []
        t = tree[0]
        branch = tree[1:]
        attributes = {}

        for attr in t:
            if isinstance(t[attr], dict):
                if t[attr].get("type", None) == "reg":
                    t[attr] = re.compile(t[attr]['reg'])

        attributes.update(t)

        if "name" in attributes:
            del attributes['name']
        if "text" in attributes:
            del attributes['text']
        if "recursive" in attributes:
            del attributes['recursive']
        if "[]" in attributes:
            del attributes['[]']

        possibles = ele.find_all(
            t.get('name', None),
            text=t.get('text', None),
            attrs=attributes,
            recursive=t.get('recursive', True)
        )

        if not possibles:
            return None
        else:
            pass

        if "[]" in t:
            try:
                possibles = eval(u"possibles[{}]".format(t["[]"]))
            except:
                # no possibles
                return None

        if not isinstance(possibles, list):
            possibles = [possibles]

        for a in possibles:
            match = self._getTagMatch(a, branch)

            if match:
                res.extend(match)

        if not res:
            return None
        else:
            return res

    def _parseValue(self, eles, valueScheme):
        val = []
        valType = valueScheme.get('type', None)
        reg = valueScheme.get('reg', None)
        strip = valueScheme.get('strip', False)

        for match in eles:
            if valType == "text":
                val.append(unicode(match.getText()))
            elif valType == "content":
                val.append(unicode(match.getText()))
            elif valType == "attribute" and valueScheme.get("attribute", None):
                attr = valueScheme['attribute']

                if attr in match.attrs:
                    res = match[attr]

                    # multi-valued attributes will be joined in one string
                    if isinstance(res, list):
                        res = u" ".join(res)
                    val.append(res)
            elif valType == "html":
                val.append(unicode(match))
            else:
                # == html2text
                if self._text_maker is None:
                    val.append(html2text.html2text(unicode(match)))
                else:
                    val.append(self._text_maker.handle(unicode(match)))
            if strip:
                # TODO: github date field
                val[-1] = val[-1].strip()

        if reg:
            res = []

            for a in val:
                if isinstance(reg, dict):
                    if reg.get('type', None) == "reg":
                        reg = re.compile(reg['reg'])
                res.extend(reg.findall(a))
                # self.debug(u"'{}' - {}".format(a, res))
        else:
            res = val

        return res

    def _parseScheme(self, ele, scheme):
        res = {}

        for aKey in scheme:
            # self.debug(u"{}".format(aKey))
            entity = scheme[aKey]
            val = []
            matches = []
            res[aKey] = []

            if "tree" in entity:
                matches = self._getTagMatch(ele, entity['tree'])

                if not matches:
                    matches = []
                else:
                    pass
            else:
                # matches = [ele]
                pass

            if not matches and "value" == aKey:
                val.extend(self._parseValue([ele], entity))
                res[aKey].extend(val)

            if "value" == aKey:
                for a in matches:
                    # TODO: sure it's ele and not a?
                    val.extend(self._parseValue([ele], entity))
            if "children" in entity:
                for a in matches:
                    obj = {}
                    if "value" == aKey:
                        obj['value'] = val
                    child = self._parseScheme(a, entity['children'])

                    if child:
                        obj.update(child)
                    if obj:
                        res[aKey].append(obj)
        return res

    def scrap(self, url=None, scheme=None, timeout=None):
        """
        Scrap a url and parse the content according to scheme

        :param url: Url to parse (default: self._url)
        :type url: str
        :param scheme: Scheme to apply to html (default: self._scheme)
        :type scheme: dict
        :param timeout: Timeout for http operation (default: self._timout)
        :type timeout: float
        :return: Parsed data from url
        :rtype: dict
        :raises WEBConnectException: HTTP get failed
        :raises WEBParameterException: Missing scheme or url
        """
        if not url:
            url = self._url
        if not scheme:
            scheme = self._scheme
        if not timeout:
            timeout = self._timeout
        if not scheme:
            raise WEBParameterException("Missing scheme definition")
        if not url:
            raise WEBParameterException("Missing url definition")
        htmlSite = self.get(url, timeout)
        soup = BeautifulSoup(htmlSite, self._html_parser)
        res = self._parseScheme(soup, scheme)
        return res

    def shrinkList(self, shrink):
        if not isinstance(shrink, list):
            if isinstance(shrink, dict):
                return self.shrinkDict(shrink)
            return shrink

        res = []

        if len(shrink) == 1:
            return self.shrinkDict(shrink[0])
        else:
            for a in shrink:
                temp = self.shrinkDict(a)

                if temp:
                    res.append(temp)
        return res

    def shrinkDict(self, shrink):
        if not isinstance(shrink, dict):
            if isinstance(shrink, list):
                return self.shrinkList(shrink)
            return shrink

        res = {}

        if len(shrink.keys()) == 1 and "value" in shrink:
            return self.shrinkList(shrink['value'])
        else:
            for a in shrink:
                res[a] = self.shrinkList(shrink[a])

                if not res[a]:
                    del res[a]
        return res
