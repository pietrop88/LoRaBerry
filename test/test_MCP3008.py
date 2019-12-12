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
from gpiozero import Device
from gpiozero.pins.mock import MockFactory, MockSPIDevice
from mock import patch
from loraberry import MCP3008

DEFAULT_CHANNEL = 0
ADC_MIN_VALUE = 0
ADC_MAX_VALUE = 255
ADC_BITS = 10
ADC_VREF = 3.3

class Test(unittest.TestCase):
    def setup_method(self, method):
        self._save_factory = Device.pin_factory
        Device.pin_factory = MockFactory()
    
    def teardown_method(self, method):
        if Device.pin_factory is not None:
            Device.pin_factory.reset()
        Device.pin_factory = self._save_factory

    def test_get_min_value(self):
      adc = MCP3008(channel=DEFAULT_CHANNEL)
      self.assertEqual(adc.get_min_value(), ADC_MIN_VALUE)
        
    def test_get_max_value(self):
      adc = MCP3008(channel=DEFAULT_CHANNEL)
      self.assertEqual(adc.get_max_value(), ADC_MAX_VALUE)

    def test_get_value(self):
        with patch('gpiozero.pins.local.SpiDev', None):
            mock = MockMCP3008(11, 10, 9, 8)
            adc = MCP3008(channel=DEFAULT_CHANNEL)
            scale = 2 ** ADC_BITS
            tolerance = 1 / scale * ADC_MAX_VALUE
            
            mock.channels[DEFAULT_CHANNEL] = 0.0
            self.assertAlmostEqual(adc.get_value(), 0.0, delta=tolerance)
            
            mock.channels[DEFAULT_CHANNEL] = 0.5 * ADC_VREF
            self.assertAlmostEqual(adc.get_value(), 0.5 * ADC_MAX_VALUE, delta=tolerance)
            
            mock.channels[0] = ADC_VREF
            self.assertAlmostEqual(adc.get_value(), ADC_MAX_VALUE, delta=tolerance)

class MockMCP3008(MockSPIDevice):
    def __init__(self, clock_pin, mosi_pin, miso_pin, select_pin=None):
        super(MockMCP3008, self).__init__(clock_pin, mosi_pin, miso_pin, select_pin)
        self.vref = ADC_VREF
        self.channels = [0.0] * 8
        self.channel_bits = 3
        self.bits = ADC_BITS
        self.state = 'idle'

    def on_start(self):
        super(MockMCP3008, self).on_start()
        self.state = 'idle'

    def on_bit(self):
        if self.state == 'idle':
            if self.rx_buf[-1]:
                self.state = 'mode'
                self.rx_buf = []
        elif self.state == 'mode':
            if self.rx_buf[-1]:
                self.state = 'single'
            self.rx_buf = []
        elif self.state in ('single', 'diff'):
            if len(self.rx_buf) == self.channel_bits:
                self.on_result(self.state == 'diff', self.rx_word())
                self.state = 'result'
        elif self.state == 'result':
            if not self.tx_buf:
                self.state = 'idle'
                self.rx_buf = []

    def on_result(self, differential, channel):
        result = self._clamp(self.channels[channel], 0, self.vref)
        result = self._scale(result, self.vref, self.bits)
        self.tx_word(result, self.bits + 2)
    
    def _clamp(self, v, min_value, max_value):
        return min(max_value, max(min_value, v))

    def _scale(self, v, ref, bits):
        v /= ref
        vmin = -(2 ** bits)
        vmax = -vmin - 1
        vrange = vmax - vmin
        return int(((v + 1) / 2.0) * vrange + vmin)