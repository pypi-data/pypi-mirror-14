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
import os.path
import sys
import textwrap
import unittest
import warnings

import mock
import six

from ..config import Configuration
from ..errors import Enstaller4rcError
from .._placeholders import (
    APITokenAuth, ProxyConfiguration, UserPasswordAuth
)


def configuration_from_string(s):
    return Configuration.from_file(six.StringIO(s))


class TestConfigurationDefault(unittest.TestCase):
    def _assert_default_values(self, config):
        self.assertIsNone(config.auth)
        self.assertIs(config.autoupdate, True)
        self.assertIsNone(config.filename)
        self.assertEqual(config.indexed_repositories, ())
        self.assertEqual(config.max_retries, 0)
        self.assertIs(config.noapp, False)
        self.assertEqual(config.prefix, sys.prefix)
        self.assertIsNone(config.proxy)
        self.assertEqual(config.proxy_dict, {})
        self.assertEqual(
            config.repository_cache, os.path.join(config.prefix, "LOCAL-REPO")
        )
        self.assertEqual(config.store_kind, "legacy")
        self.assertEqual(config.store_url, "https://api.enthought.com")
        self.assertIs(config.use_pypi, True)
        self.assertIs(config.use_webservice, True)
        self.assertIs(config.verify_ssl, True)

    def test_default(self):
        # Given
        config = Configuration()

        # Then
        self._assert_default_values(config)

    def test_default_from_empty_string(self):
        # Given
        text = ""

        # When
        config = configuration_from_string(text)

        # Then
        self._assert_default_values(config)

    def test_default_str(self):
        # Given
        r_output = textwrap.dedent("""\
        use_webservice: True
        settings:
            prefix = {0}
            repository_cache = {1}
            noapp = False
            proxy = None
        No auth information in configuration""").format(
            sys.exec_prefix, os.path.join(sys.exec_prefix, "LOCAL-REPO")
        )

        # When
        config = configuration_from_string("")

        # Then
        self.assertMultiLineEqual(str(config), r_output)


class TestConfigurationMisc(unittest.TestCase):
    def test_syntax_error(self):
        # Given
        text = "a = [[]"
        r_msg = (
            "Could not parse configuration file \(invalid python "
            "syntax at line 1: expression 'a = \[\[\]'\)"
        )

        # When/Then
        with self.assertRaisesRegexp(Enstaller4rcError, r_msg) as exc:
            configuration_from_string(text)

    def test_unsupported_syntax(self):
        # Given
        text = "if True: repository_cache = None"

        r_msg = (
            "Could not parse configuration file \(error at line 1: "
            "expression 'if True: repository_cache = None' not supported\)"
        )

        # When/Then
        with self.assertRaisesRegexp(Enstaller4rcError, r_msg) as exc:
            configuration_from_string(text)

    def test_unsupported_settings(self):
        # Given
        text = "flipper = 'the dolphin'"

        r_msg = "Unsupported configuration setting 'flipper', ignored"

        # When/Then
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            configuration_from_string(text)

            self.assertEqual(len(w), 1)
            self.assertIsInstance(w[0], warnings.WarningMessage)
            self.assertMultiLineEqual(str(w[0].message), r_msg)


class TestConfigurationAuth(unittest.TestCase):
    def setUp(self):
        self.r_auth = UserPasswordAuth("foo", "bar")
        self.r_encoded_auth = "Zm9vOmJhcg=="

    def test_from_file(self):
        # Given
        text = textwrap.dedent("""\
        EPD_auth = "{0}"
        """.format(self.r_encoded_auth))

        # Then
        config = configuration_from_string(text)

        # Then
        self.assertEqual(config.auth, self.r_auth)

    def test_from_file_api_token(self):
        # Given
        text = textwrap.dedent("""\
        api_token = "some dummy value"
        """)

        # Then
        config = configuration_from_string(text)

        # Then
        self.assertEqual(config.auth, APITokenAuth("some dummy value"))

    def test_multi_auth(self):
        # Given
        text = textwrap.dedent("""\
        EPD_auth = "{0}"
        api_token = "somme dummy value"
        """).format(self.r_encoded_auth)

        r_msg = (
            "Both 'EPD_auth' and 'api_token' set in configuration.\n"
            "You should remove one of those for consistent behaviour."
        )

        # When/Then
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            configuration_from_string(text)

            self.assertEqual(len(w), 1)
            self.assertIsInstance(w[0], warnings.WarningMessage)
            self.assertMultiLineEqual(str(w[0].message), r_msg)


class TestConfigurationStoreURL(unittest.TestCase):
    def test_from_file(self):
        # Given
        text = textwrap.dedent("""\
        store_url = "https://packages.enthought.com"
        """)

        # Then
        config = configuration_from_string(text)

        # Then
        self.assertEqual(config.store_url, "https://packages.enthought.com")


class TestIndexedRepositories(unittest.TestCase):
    def test_webservice_true(self):
        # Given
        r_indexed_repositories = tuple()

        text = ""

        # When
        with mock.patch("enstaller4rc.config.CUSTOM_PLAT", "rh5-64"):
            config = configuration_from_string(text)

        # Then
        self.assertEqual(config.indexed_repositories, r_indexed_repositories)

    def test_webservice_false(self):
        # Given
        r_indexed_repositories = (
            'https://www.enthought.com/repo/ets/eggs/RedHat/RH5_amd64/',
            'https://store.enthought.com/repo/genia/phase1/eggs/RedHat/RH5_amd64/'
        )

        text = textwrap.dedent("""\
        IndexedRepos = [
          'https://www.enthought.com/repo/ets/eggs/{SUBDIR}/',
          'https://store.enthought.com/repo/genia/phase1/eggs/{SUBDIR}/',
        ]
        """)

        # When
        with mock.patch("enstaller4rc.config.CUSTOM_PLAT", "rh5-64"):
            config = configuration_from_string(text)

        # Then
        self.assertEqual(config.indexed_repositories, r_indexed_repositories)


class TestProxy(unittest.TestCase):
    def test_simple_proxy(self):
        # Given
        r_proxy = ProxyConfiguration("acme.com")

        text = "proxy = 'http://acme.com:3128'"

        # When
        config = configuration_from_string(text)

        # Then
        self.assertEqual(config.proxy, r_proxy)

    def test_proxy_with_auth(self):
        # Given
        r_proxy = ProxyConfiguration(
            "acme.com", "https", 8080, "nono", "le-petit-robot"
        )

        text = "proxy = 'https://nono:le-petit-robot@acme.com:8080'"

        # When
        config = configuration_from_string(text)

        # Then
        self.assertEqual(config.proxy, r_proxy)
