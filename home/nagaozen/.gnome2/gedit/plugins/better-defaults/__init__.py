# -*- coding: utf-8 -*-

# Gedit Better Defaults plugin
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

import gedit
import gtk
import re

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
			self.activate_view(view)

		for doc in self._window.get_documents():
			self.activate_doc(doc)

		self._tab_added_id = self._window.connect("tab_added", self.on_tab_added)
#		self._key_press_id = self._window.connect("key-press-event", self.on_key_press_event)

	def deactivate(self):
#		self._window.disconnect(self._key_press_id)
		self._window.disconnect(self._tab_added_id)

		for doc in self._window.get_documents():
			self.deactivate_doc(doc)

		for view in self._window.get_views():
			self.deactivate_view(view)

		self.uninstall_ui()

		self._window = None
		self._plugin = None

	def update_ui(self):
		pass
#		# TODO: Use key press and button press events instead of update_ui
#		doc = self._window.get_active_document()
#		if doc:
#			bounds = doc.get_selection_bounds()
#			if bounds:
#				content = doc.get_text(*bounds).decode("utf-8")
#				highlightable = re.compile(r"[\S\{\}\[\]\(\)]+", flags=re.UNICODE)
#				if highlightable.search(content):
#					doc.set_search_text(content, gedit.SEARCH_CASE_SENSITIVE)
#				else:
#					doc.set_search_text("", gedit.SEARCH_CASE_SENSITIVE)
#			else:
#				doc.set_search_text("", gedit.SEARCH_CASE_SENSITIVE)

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

	def activate_view(self, view):
		view.set_smart_home_end(True)

		view.set_data("vscrolling_helper", (0.0, 0.0))

		size_allocate_id = view.connect("size-allocate", self.on_size_allocate)
		view.set_data("on_size_allocate_id", size_allocate_id)

		va = view.get_vadjustment()
		value_change_id = va.connect("value_changed", self.on_value_changed)
		view.set_data("on_value_changed_id", value_change_id)

	def deactivate_view(self, view):
		va = view.get_vadjustment()
		va.disconnect( view.get_data("on_value_changed_id") )

		view.disconnect( view.get_data("on_size_allocate_id") )

		view.set_smart_home_end(False)

	def activate_doc(self, doc):
		save_id = doc.connect("save", self.on_document_save)
		doc.set_data("on_save_id", save_id)

	def deactivate_doc(self, doc):
		doc.disconnect( view.get_data("on_save_id") )

	def on_tab_added(self, w, t):
		self.activate_view(t.get_view())
		self.activate_doc(t.get_document())

	def on_document_save(self, doc):
		piter = doc.get_end_iter()
		if piter.starts_line():
			while piter.backward_char():
				if not piter.ends_line():
					piter.forward_to_line_end()
					break
			doc.delete(piter, doc.get_end_iter())

	def on_size_allocate(self, view, allocation):
		va = view.get_vadjustment()
		vsz = va.get_upper() + ( va.get_page_size() / 2 )
		if va.get_upper() > va.get_page_size():
			va.set_upper(vsz)

			if va.get_value() < view.get_data("vscrolling_helper")[1]:
				va.set_value(view.get_data("vscrolling_helper")[1])

			view.set_data("vscrolling_helper", (vsz, va.get_value()))

	def on_value_changed(self, adjustment):
		view = self._window.get_active_view()
		va   = view.get_vadjustment()
		if( va.get_upper() == view.get_data("vscrolling_helper")[0] ):
			view.set_data( "vscrolling_helper", ( view.get_data("vscrolling_helper")[0], va.get_value() ) )

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

class BetterDefaultsPlugin(gedit.Plugin):

	WINDOW_DATA_KEY = "BetterDefaultsPluginWindowData"

	def __init__(self):
		gedit.Plugin.__init__(self)

	def activate(self, window):
		helper = BetterDefaultsWindowHelper(self, window)
		window.set_data(self.WINDOW_DATA_KEY, helper)

	def deactivate(self, window):
		window.get_data(self.WINDOW_DATA_KEY).deactivate()
		window.set_data(self.WINDOW_DATA_KEY, None)

	def update_ui(self, window):
		window.get_data(self.WINDOW_DATA_KEY).update_ui()


