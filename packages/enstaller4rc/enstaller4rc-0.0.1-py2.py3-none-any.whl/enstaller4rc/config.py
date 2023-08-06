#------------------------------------------------------------------------------
#
#  Copyright (c) 2016, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#------------------------------------------------------------------------------
import os
import os.path
import sys
import warnings

import six

from six.moves import urllib

from .errors import Enstaller4rcError, InvalidSyntax
from .utils import fill_template_path, fill_url, parse_assignments

from ._placeholders import APITokenAuth, ProxyConfiguration, UserPasswordAuth
from ._platform import CUSTOM_PLAT


STORE_KIND_LEGACY = "legacy"
STORE_KIND_BROOD = "brood"
_BROOD_PREFIX = "brood+"


class Configuration(object):
    @classmethod
    def from_file(cls, filename):
        """
        Create a new Configuration instance from the given file.

        Parameters
        ----------
        filename: str or file-like object
            If a string, is understood as a filename to open. Understood as a
            file-like object otherwise.
        """
        def _create(fp):
            ret = cls()

            def api_token_to_auth(api_token):
                _update(ret, auth=APITokenAuth(api_token))

            def epd_auth_to_auth(epd_auth):
                _update(ret, auth=UserPasswordAuth.from_encoded_auth(epd_auth))

            try:
                parsed = parse_assignments(fp)
            except (InvalidSyntax, SyntaxError) as e:
                msg = _create_error_message(fp, e)
                raise Enstaller4rcError(msg)

            # We need a custom translator to manage attributes in the
            # configuration file without polluting the config class
            translator = ret._name_to_setter.copy()
            translator.update({
                "EPD_auth": epd_auth_to_auth,
                "IndexedRepos": translator["indexed_repositories"],
                "api_token": api_token_to_auth,
            })

            if "EPD_auth" in parsed and "api_token" in parsed:
                msg = (
                    "Both 'EPD_auth' and 'api_token' set in configuration.\n"
                    "You should remove one of those for consistent behaviour."
                )
                warnings.warn(msg)

            for name, value in parsed.items():
                if name in translator:
                    translator[name](value)
                else:
                    warnings.warn("Unsupported configuration setting {0!r}, "
                                  "ignored".format(name))
            return ret

        if isinstance(filename, six.string_types):
            with open(filename, "r") as fp:
                ret = _create(fp)
                ret._filename = filename
                return ret
        else:
            return _create(filename)

    def __init__(self, **kw):
        """ Create a new configuration instance.

        Any argument passed to the constructor need to be a keyword argument,
        and is understood as an argument to the update method, e.g.::

            config = Configuration(store_url="http://acme.com")

            # equivalent to
            config = Configuration()
            config.update(store_url="http://acme.com")
        """
        self._auth = None
        self._autoupdate = True
        self._noapp = False
        self._proxy = None
        self._use_pypi = True
        self._use_webservice = True

        self._prefix = os.path.normpath(sys.prefix)
        self._indexed_repositories = tuple()
        self._store_url = "https://api.enthought.com"
        self._store_kind = STORE_KIND_LEGACY

        self._repository_cache = None

        self._filename = None
        self._platform = CUSTOM_PLAT

        self._max_retries = 0
        self._verify_ssl = True

        self._name_to_setter = {}
        simple_attributes = [
            ("autoupdate", "_autoupdate"),
            ("noapp", "_noapp"),
            ("verify_ssl", "_verify_ssl"),
            ("use_pypi", "_use_pypi"),
            ("use_webservice", "_use_webservice"),
        ]
        for name, private_attribute in simple_attributes:
            self._name_to_setter[name] = \
                self._simple_attribute_set_factory(private_attribute)

        self._name_to_setter.update({
            "auth": self._set_auth,
            "indexed_repositories": self._set_indexed_repositories,
            "max_retries": self._set_max_retries,
            "prefix": self._set_prefix,
            "proxy": self._set_proxy,
            "repository_cache": self._set_repository_cache,
            "store_url": self._set_store_url,
        })

        _update(self, **kw)

    # ----------
    # Properties
    # ----------
    @property
    def auth(self):
        """
        The auth object that may be passed to Session.authenticate

        :return: the auth instance, or None is configured.
        :rtype: IAuth or None
        """
        return self._auth

    @property
    def autoupdate(self):
        """
        Whether enpkg should attempt updating itself.
        """
        return self._autoupdate

    @property
    def filename(self):
        """
        The filename this configuration was created from. May be None if the
        configuration was not created from a file.
        """
        return self._filename

    @property
    def indexed_repositories(self):
        """
        List of (old-style) repositories. Only actually used when
        use_webservice is False.
        """
        return self._indexed_repositories

    @property
    def max_retries(self):
        """
        Max attempts to retry an http connection or re-fetching data whose
        checksum failed.
        """
        return self._max_retries

    @property
    def noapp(self):
        """
        Ignore appinst entries.
        """
        return self._noapp

    @property
    def prefix(self):
        """
        Prefix in which enpkg operates.
        """
        return self._prefix

    @property
    def proxy(self):
        """
        A ProxyConfiguration instance or None if no proxy is configured.
        """
        return self._proxy

    @property
    def proxy_dict(self):
        """
        A dictionary <scheme>:<proxy_string> that can be used as the proxies
        argument for requests.
        """
        if self._proxy:
            return {self._proxy.scheme: str(self._proxy)}
        else:
            return {}

    @property
    def repository_cache(self):
        """
        Absolute path where eggs will be cached.
        """
        if self._repository_cache is None:
            return os.path.join(self.prefix, "LOCAL-REPO")
        else:
            return self._repository_cache

    @property
    def store_kind(self):
        """
        Store kind (brood, legacy canopy, old-repo style).
        """
        return self._store_kind

    @property
    def store_url(self):
        """
        The store url to hit for indices and eggs.
        """
        return self._store_url

    @property
    def use_pypi(self):
        """
        Whether to load pypi repositories (in `webservice` mode).
        """
        return self._use_pypi

    @property
    def use_webservice(self):
        """
        Whether to use canopy legacy or not.
        """
        return self._use_webservice

    @property
    def verify_ssl(self):
        """
        Whether to verify SSL CA or not.
        """
        return self._verify_ssl

    # ---------------
    # Private methods
    # ---------------
    def _set_auth(self, auth):
        """ Set the internal authentication information.

        Parameters
        ----------
        auth : Auth-like
            The authentication information. Must be an *Auth subclass.
        """
        self._auth = auth

    def _set_indexed_repositories(self, urls):
        self._indexed_repositories = tuple(fill_url(url) for url in urls)

    def _set_max_retries(self, raw_max_retries):
        try:
            max_retries = int(raw_max_retries)
        except ValueError:
            msg = "Invalid type for 'max_retries': {0!r}"
            raise Enstaller4rcError(msg.format(raw_max_retries))
        else:
            self._max_retries = max_retries

    def _set_prefix(self, prefix):
        self._prefix = os.path.normpath(_abs_expanduser(prefix))

    def _set_proxy(self, proxy_string):
        self._proxy = ProxyConfiguration.from_string(proxy_string)

    def _set_store_url(self, url):
        p = urllib.parse.urlparse(url)
        if p.scheme.startswith(_BROOD_PREFIX):
            url = url[len(_BROOD_PREFIX):]
            self._store_kind = STORE_KIND_BROOD
        self._store_url = url

    def _set_repository_cache(self, value):
        normalized = fill_template_path(
            os.path.normpath(_abs_expanduser(value))
        )
        self._repository_cache = normalized

    def _simple_attribute_set_factory(self, attribute_name):
        return lambda value: setattr(self, attribute_name, value)

    def __str__(self):
        lines = [
            "use_webservice: {0}".format(self.use_webservice),
        ]
        if self.filename is not None:
            lines.append("config file:{0}".format(self.filename))
        lines.append("settings:")
        lines.append("    prefix = %s" % self.prefix)
        lines.append("    %s = %s" % ("repository_cache", self.repository_cache))
        lines.append("    %s = %r" % ("noapp", self.noapp))
        lines.append("    %s = %r" % ("proxy", self.proxy))

        if not self.use_webservice:
            lines.append("    IndexedRepos:")
            for repo in self.indexed_repositories:
                lines.append('        %r' % repo)

        if self.auth is None:
            lines.append(
                "No auth information in configuration"
            )
        elif isinstance(self.auth, UserPasswordAuth):
            lines.append("Authenticated as '{0}'".format(self.auth.username))
        elif isinstance(self.auth, APITokenAuth):
            lines.append("Authenticated with API token")
        else:
            raise RuntimeError(
                "Invalid auth type: {0}".format(type(self.auth))
            )

        return "\n".join(lines)


def _create_error_message(fp, exc):
    pos = fp.tell()
    try:
        fp.seek(0)
        lines = fp.readlines()
        line = lines[exc.lineno-1].rstrip()
        if isinstance(exc, SyntaxError):
            msg = "Could not parse configuration file " \
                  "(invalid python syntax at line {0!r}: expression {1!r})".\
                  format(exc.lineno, line)
        else:
            msg = "Could not parse configuration file " \
                  "(error at line {0!r}: expression {1!r} not " \
                  "supported)".format(exc.lineno, line)
        return msg
    finally:
        fp.seek(pos)


def _abs_expanduser(path):
    return os.path.abspath(os.path.expanduser(path))


def _update(config, **kw):
    """ Set configuration attributes given as keyword arguments."""
    for name, value in kw.items():
        setter = config._name_to_setter.get(name, None)
        if name is None:
            raise ValueError("Invalid setting name: {0!r}".format(name))
        else:
            setter(value)
