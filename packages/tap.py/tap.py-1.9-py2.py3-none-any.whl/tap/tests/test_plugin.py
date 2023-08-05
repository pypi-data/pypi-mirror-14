# Copyright (c) 2015, Matt Layman

import unittest

try:
    from unittest import mock
except ImportError:
    import mock
# There is some weird conflict with `TestLoader.discover` if `nose.case.Test`
# is imported directly. Importing `nose.case` works.
from nose import case
from nose.suite import ContextSuite

from tap.plugin import DummyStream, TAP
from tap.tests import TestCase


class FakeOptions(object):

    def __init__(self):
        self.tap_stream = False
        self.tap_outdir = None
        self.tap_combined = False
        self.tap_format = ''


class FakeTestCase(object):

    def __call__(self):
        pass


class TestPlugin(TestCase):

    @classmethod
    def _make_one(cls, options=None):
        plugin = TAP()
        plugin.enabled = True
        if options is None:
            options = FakeOptions()
        plugin.configure(options, None)
        return plugin

    def test_adds_error(self):
        plugin = self._make_one()
        plugin.addError(case.Test(FakeTestCase()), (None, None, None))
        line = plugin.tracker._test_cases['FakeTestCase'][0]
        self.assertFalse(line.ok)

    def test_adds_skip(self):
        # Since Python versions earlier than 2.7 don't support skipping tests,
        # this test has to hack around that limitation.
        try:
            plugin = self._make_one()
            plugin.addError(case.Test(
                FakeTestCase()), (unittest.SkipTest, 'a reason', None))
            line = plugin.tracker._test_cases['FakeTestCase'][0]
            self.assertEqual(line.directive.text, 'SKIP a reason')
        except AttributeError:
            self.assertTrue(
                True, 'Pass because this Python does not support SkipTest.')

    @mock.patch('sys.exit')
    def test_bad_format_string(self, fake_exit):
        """A bad format string exits the runner."""
        options = FakeOptions()
        options.tap_format = "Not gonna work {sort_desc}"
        plugin = self._make_one(options)
        test = mock.Mock()

        plugin._description(test)

        self.assertTrue(fake_exit.called)

    def test_get_name_from_context_suite(self):
        """When the test is actually a ContextSuite, get the name from context.

        setUpClass/tearDownClass provides a ContextSuite object to the plugin
        if they raise an exception. The test case is not available so its
        name must be pulled from a different location.
        """
        plugin = self._make_one()
        context = mock.Mock(__name__='FakeContext')
        test = ContextSuite(context=context)

        name = plugin._cls_name(test)

        self.assertEqual(name, 'FakeContext')

    def test_streaming_option_captures_stream(self):
        options = FakeOptions()
        options.tap_stream = True
        plugin = self._make_one(options)
        fake_stream = mock.Mock()

        plugin.setOutputStream(fake_stream)

        self.assertEqual(plugin.tracker.stream, fake_stream)

    def test_streaming_options_returns_dummy_stream(self):
        options = FakeOptions()
        options.tap_stream = True
        plugin = self._make_one(options)

        dummy_stream = plugin.setOutputStream(None)

        self.assertTrue(isinstance(dummy_stream, DummyStream))
