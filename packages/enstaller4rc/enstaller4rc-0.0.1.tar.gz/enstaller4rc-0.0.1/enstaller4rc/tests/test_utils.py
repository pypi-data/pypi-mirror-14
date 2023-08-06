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
import contextlib
import mock
import os.path
import sys
import textwrap
import unittest

from six import StringIO

from ..errors import InvalidSyntax
from ..utils import parse_assignments, real_prefix, under_venv


class TestParseAssignments(unittest.TestCase):
    def test_parse_simple(self):
        # Given
        r_data = {
            "IndexedRepos": ["http://acme.com/{SUBDIR}"],
            "webservice_entry_point": "http://acme.com/eggs/{PLATFORM}/"
        }

        s = textwrap.dedent("""\
        IndexedRepos = [
            "http://acme.com/{SUBDIR}",
        ]
        webservice_entry_point = "http://acme.com/eggs/{PLATFORM}/"
        """)

        # When
        data = parse_assignments(StringIO(s))

        # Then
        self.assertEqual(data, r_data)

    def test_parse_simple_invalid_file(self):
        with self.assertRaises(InvalidSyntax):
            parse_assignments(StringIO("EPD_auth += 2"))

        with self.assertRaises(InvalidSyntax):
            parse_assignments(StringIO("1 + 2"))


class TestVenv(unittest.TestCase):
    @contextlib.contextmanager
    def _patch_prefix(self, attr_name, prefix_value):
        # attr_name can be None to remove all venv prefixes
        prefix_names = ("real_prefix", "base_prefix")
        orig_attrs = {}
        for prefix_name in prefix_names:
            if hasattr(sys, prefix_name):
                orig_attrs[prefix_name] = getattr(sys, prefix_name)
                delattr(sys, prefix_name)

        try:
            if attr_name is not None:
                with mock.patch.object(sys, attr_name, prefix_value,
                                       create=True):
                    yield
            else:
                yield
        finally:
            for prefix_name, prefix_value in orig_attrs.items():
                setattr(sys, prefix_name, prefix_value)

    def _mock_under_non_venv(self):
        return self._patch_prefix(None, None)

    def _mock_under_venv(self):
        return self._patch_prefix("base_prefix",
                                  os.path.join(sys.prefix, 'venv'))

    def _mock_under_virtualenv(self):
        return self._patch_prefix("real_prefix",
                                  os.path.join(sys.prefix, 'venv'))

    def _mock_under_base_venv(self):
        return self._patch_prefix("base_prefix", sys.prefix)

    def _mock_under_virtualenv_under_base_venv(self):
        with self._patch_prefix("base_prefix", sys.prefix):
            return self._mock_under_virtualenv()

    def test_under_venv(self):
        def _check(mock_method, is_under_venv, prefix_name):
            with mock_method():
                self.assertEqual(under_venv(), is_under_venv)
                self.assertEqual(real_prefix(), getattr(sys, prefix_name))

        _check(self._mock_under_non_venv, False, "prefix")

        _check(self._mock_under_venv, True, "base_prefix")

        _check(self._mock_under_virtualenv, True, "real_prefix")

        _check(self._mock_under_base_venv, False, "prefix")

        _check(self._mock_under_virtualenv_under_base_venv,
               True, "real_prefix")
