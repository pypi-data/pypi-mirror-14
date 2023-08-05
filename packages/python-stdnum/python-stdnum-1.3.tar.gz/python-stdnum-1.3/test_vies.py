#!/usr/bin/env python

# test_vies.py - functions for testing the European VAT VIES functions
# coding: utf-8
#
# Copyright (C) 2015 Arthur de Jong
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

# This is a separate test file because it should not be run regularly
# because it could negatively impact the VIES service.

import unittest

from stdnum.eu import vat


class TestVies(unittest.TestCase):

    def test_check_vies(self):
        r = vat.check_vies('BE555445')
        self.assertEqual(r['countryCode'], 'BE')
        self.assertEqual(r['vatNumber'], '555445')

    def test_check_vies_approx(self):
        r = vat.check_vies_approx('BE555445', 'BE555445')
        self.assertEqual(r['countryCode'], 'BE')
        self.assertEqual(r['vatNumber'], '555445')


if __name__ == '__main__':
    unittest.main()
