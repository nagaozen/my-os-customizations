# -*- coding: utf-8 -*-

# pluma QuickJump plugin
# Copyright (C) 2017 Fabio Zendhi Nagao
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pluma
from plugin import Jumper

class QuickJumpWindowHelper:

	def __init__(self, plugin, window):
		self._window = window
		self._plugin = plugin
		self._jumper = Jumper(self._plugin, self._window)

	def deactivate(self):
		self._jumper.deactivate()
		self._jumper = None
		self._window = None
		self._plugin = None

	def update_ui(self):
		pass

class QuickJumpPlugin(pluma.Plugin):

	WINDOW_DATA_KEY = "QuickJumpPluginWindowData"

	def __init__(self):
		pluma.Plugin.__init__(self)

	def activate(self, window):
		helper = QuickJumpWindowHelper(self, window)
		window.set_data(self.WINDOW_DATA_KEY, helper)

	def deactivate(self, window):
		window.get_data(self.WINDOW_DATA_KEY).deactivate()
		window.set_data(self.WINDOW_DATA_KEY, None)

	def update_ui(self, window):
		window.get_data(self.WINDOW_DATA_KEY).update_ui()

