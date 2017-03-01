# -*- coding: utf-8 -*-

# Pluma Macros plugin
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
			<placeholder name="EditOps_4">
				<menuitem action="DuplicateLine" name="Duplicate line"/>
			</placeholder>
		</menu>
	</menubar>
</ui>
"""

class BetterDefaultsWindowHelper:
	def __init__(self, plugin, window):
		self._window = window
		self._plugin = plugin

		self.install_ui()

		for view in self._window.get_views():
			view.set_smart_home_end(True)

		self._tab_added_id = self._window.connect("tab_added", lambda w, t: t.get_view().set_smart_home_end(True))
		self._key_press_id = self._window.connect("key-press-event", self.on_key_press_event)

	def deactivate(self):
		self._window.disconnect(self._key_press_id)
		self._window.disconnect(self._tab_added_id)

		for view in self._window.get_views():
			view.set_smart_home_end(False)

		self.uninstall_ui()

		self._window = None
		self._plugin = None

	def update_ui(self):
		pass

	def install_ui(self):
		manager = self._window.get_ui_manager()

		self._action_group = gtk.ActionGroup("BetterDefaultsPluginActions")
		self._action_group.add_actions([
			( "DuplicateLine", None, _("Duplicate line"), "<Ctrl><Shift>d", _("Duplicate Line"), self.duplicate_line )
		])

		manager.insert_action_group(self._action_group, -1)
		self._ui_id = manager.add_ui_from_string(ui_str)

	def uninstall_ui(self):
		manager = self._window.get_ui_manager()

		manager.remove_ui(self._ui_id)
		manager.remove_action_group(self._action_group)

		manager.ensure_update()

	def duplicate_line(self, action):
		doc = self._window.get_active_document()
		doc.begin_user_action()
		liter = doc.get_iter_at_mark(doc.get_insert())
		liter.set_line_offset(0);
		riter = doc.get_iter_at_mark(doc.get_insert())
		f = riter.forward_line()
		line = doc.get_slice(liter, riter, True)
		if f:
			doc.insert(riter, line)
		else:
			doc.insert(riter, '\n' + line)
		doc.end_user_action()

	def enclose_selected(self, l, r):
		doc = self._window.get_active_document()
		(a, b) = doc.get_selection_bounds()
		doc.insert(b, r)
		(a, b) = doc.get_selection_bounds()
		doc.insert(a, l)

	def on_key_press_event(self, window, event):
		doc = self._window.get_active_document()
		bounds = doc.get_selection_bounds()
		if bounds:
			c = event.keyval
			if c == 123:
				self.enclose_selected('{', '}')
			elif c == 91:
				self.enclose_selected('[', ']')
			elif c == 40:
				self.enclose_selected('(', ')')
			elif c == 60:
				self.enclose_selected('<', '>')
			elif c == 65111:
				self.enclose_selected('"', '"')
			elif c == 65105:
				self.enclose_selected("'", "'")
			if c in [123, 91, 40, 60, 65111, 65105]:
				return True

class BetterDefaultsPlugin(pluma.Plugin):

	WINDOW_DATA_KEY = "BetterDefaultsPluginWindowData"

	def __init__(self):
		pluma.Plugin.__init__(self)

	def activate(self, window):
		helper = BetterDefaultsWindowHelper(self, window)
		window.set_data(self.WINDOW_DATA_KEY, helper)

	def deactivate(self, window):
		window.get_data(self.WINDOW_DATA_KEY).deactivate()
		window.set_data(self.WINDOW_DATA_KEY, None)

	def update_ui(self, window):
		window.get_data(self.WINDOW_DATA_KEY).update_ui()
