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
import sys
import unittest

from ..errors import Enstaller4rcError
from .._placeholders import ProxyConfiguration, UserPasswordAuth


class TestUserPasswordAuth(unittest.TestCase):
    def test_from_encoded_auth(self):
        # Given
        encoded_auth = "Zm9vOmJhcg=="
        r_auth = ("foo", "bar")

        # When
        auth = UserPasswordAuth.from_encoded_auth(encoded_auth)

        # Then
        self.assertEqual((auth.username, auth.password), r_auth)


class TestProxyConfigurationFromString(unittest.TestCase):
    def test_without_host(self):
        # Given
        s = ""

        # When/Then
        with self.assertRaises(Enstaller4rcError):
            ProxyConfiguration.from_string(s)

        # Given
        s = ":3128"

        # When/Then
        with self.assertRaises(Enstaller4rcError):
            ProxyConfiguration.from_string(s)

    @unittest.skipIf(sys.version_info < (2, 7),
                     "Bug in stdlib on 2.6")
    def test_without_scheme(self):
        # Given
        s = "acme.com:3129"

        # When
        info = ProxyConfiguration.from_string(s)

        # Then
        self.assertEqual(info.scheme, "http")
        self.assertEqual(info.host, "acme.com")
        self.assertEqual(info.user, "")
        self.assertEqual(info.password, "")
        self.assertEqual(info.port, 3129)

    def test_simple(self):
        # Given
        s = "http://acme.com"

        # When
        info = ProxyConfiguration.from_string(s)

        # Then
        self.assertEqual(info.scheme, "http")
        self.assertEqual(info.user, "")
        self.assertEqual(info.password, "")
        self.assertEqual(info.port, 3128)

    def test_simple_port(self):
        # Given
        s = "http://acme.com:3129"

        # When
        info = ProxyConfiguration.from_string(s)

        # Then
        self.assertEqual(info.scheme, "http")
        self.assertEqual(info.user, "")
        self.assertEqual(info.password, "")
        self.assertEqual(info.port, 3129)

    def test_simple_user(self):
        # Given
        s = "http://john:doe@acme.com"

        # When
        info = ProxyConfiguration.from_string(s)

        # Then
        self.assertEqual(info.scheme, "http")
        self.assertEqual(info.user, "john")
        self.assertEqual(info.password, "doe")
        self.assertEqual(info.port, 3128)

    def test_simple_user_wo_password(self):
        # Given
        s = "http://john@acme.com"

        # When
        info = ProxyConfiguration.from_string(s)

        # Then
        self.assertEqual(info.scheme, "http")
        self.assertEqual(info.user, "john")
        self.assertEqual(info.password, "")
        self.assertEqual(info.port, 3128)

    def test_scheme(self):
        # Given
        s = "https://john@acme.com"

        # When
        info = ProxyConfiguration.from_string(s)

        # Then
        self.assertEqual(info.scheme, "https")
        self.assertEqual(info.user, "john")
        self.assertEqual(info.password, "")
        self.assertEqual(info.port, 3128)


class TestProxyConfiguration(unittest.TestCase):
    def test_str_simple(self):
        # Given
        proxy_info = ProxyConfiguration.from_string("http://acme.com:3129")

        # When
        s = str(proxy_info)

        # Then
        self.assertEqual(s, "http://acme.com:3129")

    def test_str_full(self):
        # Given
        proxy_info = ProxyConfiguration.from_string("http://john:doe@acme.com:3129")

        # When
        s = str(proxy_info)

        # Then
        self.assertEqual(s, "http://john:doe@acme.com:3129")
