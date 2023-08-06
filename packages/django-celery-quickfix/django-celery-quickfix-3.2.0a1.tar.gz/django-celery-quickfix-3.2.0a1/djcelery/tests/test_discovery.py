from __future__ import absolute_import, unicode_literals

import warnings

import django
from django.conf import settings

from celery.registry import tasks

from djcelery.loaders import autodiscover
from djcelery.tests.utils import unittest


class TestDiscovery(unittest.TestCase):

    def assertDiscovery(self):
        apps = autodiscover()
        self.assertTrue(apps)
        self.assertIn('c.unittest.SomeAppTask', tasks)
        self.assertEqual(tasks['c.unittest.SomeAppTask'].run(), 42)

    def test_discovery(self):
        if 'someapp' in settings.INSTALLED_APPS:
            self.assertDiscovery()

    def test_discovery_with_broken(self):
        warnings.resetwarnings()
        if 'someapp' in settings.INSTALLED_APPS:
            if django.VERSION < (1, 7):
                # Django < 1.7
                installed_apps = list(settings.INSTALLED_APPS)
                settings.INSTALLED_APPS = installed_apps + ['xxxnot.aexist']
                try:
                    # we should get a warning when loading xxxnot.aexist
                    with warnings.catch_warnings(record=True) as log:
                        autodiscover()
                        self.assertTrue(log)
                finally:
                    settings.INSTALLED_APPS = installed_apps
            else:
                # Django 1.7
                with warnings.catch_warnings(record=True) as log:
                    # we should not get any warnings
                    autodiscover()
                    self.assertEqual(log, [])
