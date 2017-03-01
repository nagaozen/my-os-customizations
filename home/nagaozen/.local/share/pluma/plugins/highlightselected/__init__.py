# -*- coding: utf-8 -*-

# Pluma HighlightSelected plugin
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

class HighlightSelectedWindowHelper:

	def __init__(self, plugin, window):
		self._window = window
		self._plugin = plugin

	def deactivate(self):
		self._window = None
		self._plugin = None

	def update_ui(self):
		# TODO: Use key press and button press events instead of update_ui
		doc = self._window.get_active_document()
		if doc:
			bounds = doc.get_selection_bounds()
			if bounds:
				(liter, riter) = bounds
				doc.set_search_text(doc.get_text(liter, riter), pluma.SEARCH_CASE_SENSITIVE)
			else:
				doc.set_search_text("", pluma.SEARCH_CASE_SENSITIVE)

class HighlightSelectedPlugin(pluma.Plugin):

	WINDOW_DATA_KEY = "HighlightSelectedPluginWindowData"

	def __init__(self):
		pluma.Plugin.__init__(self)

	def activate(self, window):
		helper = HighlightSelectedWindowHelper(self, window)
		window.set_data(self.WINDOW_DATA_KEY, helper)

	def deactivate(self, window):
		window.get_data(self.WINDOW_DATA_KEY).deactivate()
		window.set_data(self.WINDOW_DATA_KEY, None)

	def update_ui(self, window):
		window.get_data(self.WINDOW_DATA_KEY).update_ui()

