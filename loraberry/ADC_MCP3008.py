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

from loraberry import ADC
from gpiozero import MCP3008

MIN_VALUE = 0
MAX_VALUE = 255

class ADC_MCP3008(ADC, MCP3008):
    def __init__(self, channel = 0):
      super().__init__(channel = channel)

    def get_min_value(self):
        return MIN_VALUE

    def get_max_value(self):
        return MAX_VALUE
    
    def get_value(self):
        return super().value * MAX_VALUE