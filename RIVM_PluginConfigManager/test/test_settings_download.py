# coding=utf-8
"""Dialog test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'marnix.de.ridder@rivm.nl'
__date__ = '2017-08-21'
__copyright__ = 'Copyright 2017, RIVM'

import unittest

from networkaccessmanager import NetworkAccessManager, RequestsException


class SettingsDownloadTest(unittest.TestCase):
    """Test if settings/ini files are downloadable."""

    def setUp(self):
        """Runs before each test."""
        self.settings_url = 'http://repo.svc.cal-net.nl/repo/rivm/qgis/'
        self.nam = NetworkAccessManager()

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_dev_ok(self):
        """Test if we can download dev settings."""
        try:
            url = self.settings_url + 'dev.rivm.ini'
            (response, content) = self.nam.request(url)
            if response.status == 200:
                self.assertEqual(200, response.status)
            else:
                self.fail("test_dev_ok: NON-200 response: {} {}".format(response.status, response.content))
        except RequestsException, e:
            # Handle exception
            self.fail("test_dev_ok, throws exception: " + e.message)

    def test_acc_ok(self):
        """Test if we can download acc settings."""
        try:
            url = self.settings_url + 'acc.rivm.ini'
            (response, content) = self.nam.request(url)
            if response.status == 200:
                self.assertEqual(200, response.status)
            else:
                self.fail("test_acc_ok: NON-200 response: {} {}".format(response.status, response.content))
        except RequestsException, e:
            # Handle exception
            self.fail("test_acc_ok, throws exception: " + e.message)

    def test_prd_ok(self):
        """Test if we can download prd settings."""
        try:
            url = self.settings_url + 'prd.rivm.ini'
            (response, content) = self.nam.request(url)
            if response.status == 200:
                self.assertEqual(200, response.status)
            else:
                self.fail("test_prd_ok: NON-200 response: {} {}".format(response.status, response.content))
        except RequestsException, e:
            # Handle exception
            self.fail("test_prd_ok, throws exception: " + e.message)

if __name__ == "__main__":
    suite = unittest.makeSuite(SettingsDownloadTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

