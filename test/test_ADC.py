# LoraBerry.
# Copyright (C) Pietro Panizza.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest
from loraberry import ADC

class Test(unittest.TestCase):

    def test_get_min_value(self):
        adc = ADC()
        with self.assertRaises(NotImplementedError):
            adc.get_min_value()

    def test_get_max_value(self):
        adc = ADC()
        with self.assertRaises(NotImplementedError):
            adc.get_max_value()

    def test_get_value(self):
        adc = ADC()
        with self.assertRaises(NotImplementedError):
            adc.get_value()