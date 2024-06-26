# coding=utf-8
"""Resources test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'yanialva2009@gmail.com, maxigaspero@gmail.com, valetobares11@gmail.com'
__date__ = '2024-06-26'
__copyright__ = 'Copyright 2024, Alvarez Yanina, Gaspero Maximiliano, Tobares Valentin'

import unittest

from qgis.PyQt.QtGui import QIcon



class EmergencyDispatcherDialogTest(unittest.TestCase):
    """Test rerources work."""

    def setUp(self):
        """Runs before each test."""
        pass

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_icon_png(self):
        """Test we can click OK."""
        path = ':/plugins/EmergencyDispatcher/icon.png'
        icon = QIcon(path)
        self.assertFalse(icon.isNull())

if __name__ == "__main__":
    suite = unittest.makeSuite(EmergencyDispatcherResourcesTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)



