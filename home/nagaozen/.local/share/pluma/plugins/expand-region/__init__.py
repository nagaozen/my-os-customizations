# -*- coding: utf-8 -*-

# pluma ExpandRegion plugin
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
import gtk

ui_str = """
<ui>
	<menubar name="MenuBar">
		<menu name="EditMenu" action="Edit">
			<placeholder name='EditOps_3'>
				<menuitem name="ExpandRegion" action="ExpandRegion"/>
			</placeholder>
		</menu>
	</menubar>
</ui>
"""

class ExpandRegionWindowHelper:
	def __init__(self, plugin, window):
		self._window = window
		self._plugin = plugin

		manager = self._window.get_ui_manager()

		self._action_group = gtk.ActionGroup("ExpandRegionPluginActions")
		self._action_group.add_actions([(
			"ExpandRegion",
			None,
			_("Expand Region"),
			"<Ctrl>e",
			_("Expand region from the cursor"),
			self.expand_region_from_cursor
		)])

		manager.insert_action_group(self._action_group, -1)
		self._ui_id = manager.add_ui_from_string(ui_str)

	def deactivate(self):
		manager = self._window.get_ui_manager()
		manager.remove_ui(self._ui_id)
		manager.remove_action_group(self._action_group)
		manager.ensure_update()

		self._window = None
		self._plugin = None

	def update_ui(self):
		pass

	def expand_region_from_cursor(self, action):
		doc = self._window.get_active_document()
		bounds = doc.get_selection_bounds()

		if bounds:
			(liter, riter) = bounds
			liter.backward_char()
		else:
			liter = doc.get_iter_at_mark(doc.get_insert()).copy()
			riter = doc.get_iter_at_mark(doc.get_insert()).copy()

		self.expand_region(liter, riter)

	def expand_region(self, liter, riter):
		doc = self._window.get_active_document()

		lchars  = ['`', '"', "'", '[', '(', '{']
		rchars  = ['`', '"', "'", ']', ')', '}']

		iter_char = None
		match_char = None

		stack = []
		while liter.backward_char():
			iter_char = liter.get_char()
			if iter_char in lchars and len(stack) == 0:
				match_char = rchars[ lchars.index(iter_char) ]
				liter.forward_char()
				break
			elif len(stack) > 0 and stack[len(stack) -1] == iter_char:
				stack.pop()
			elif iter_char in rchars:
				stack.append( lchars[ rchars.index(iter_char) ] )

		stack = []
		while riter.forward_char():
			iter_char = riter.get_char()
			if iter_char == match_char and len(stack) == 0:
				break
			elif len(stack) > 0 and stack[len(stack) -1] == iter_char:
				stack.pop()
			elif iter_char in lchars:
				stack.append( rchars[ lchars.index(iter_char) ] )

		doc.select_range(liter, riter)

class ExpandRegionPlugin(pluma.Plugin):

	WINDOW_DATA_KEY = "ExpandRegionPluginWindowData"

	def __init__(self):
		pluma.Plugin.__init__(self)

	def activate(self, window):
		helper = ExpandRegionWindowHelper(self, window)
		window.set_data(self.WINDOW_DATA_KEY, helper)

	def deactivate(self, window):
		window.get_data(self.WINDOW_DATA_KEY).deactivate()
		window.set_data(self.WINDOW_DATA_KEY, None)

	def update_ui(self, window):
		window.get_data(self.WINDOW_DATA_KEY).update_ui()

