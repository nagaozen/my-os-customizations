# -*- coding: utf-8 -*-

# gedit QuickJump plugin
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

import gobject
import gtk
import re
import string
from entry import Entry
from itertools import combinations_with_replacement as cwr

SHORTCUT_LABELS = ["".join(combination) for combination in cwr(string.ascii_lowercase, 2)]

class Jumper(gobject.GObject):
	def __init__(self, plugin, window):
		gobject.GObject.__init__(self)

		self._window = window
		self._plugin = plugin

		self._entry = None
		self._accel = gtk.AccelGroup()
		self._accel.connect_group(gtk.keysyms.comma, gtk.gdk.CONTROL_MASK, 0, self.init_entry)
		self._window.add_accel_group(self._accel)

	def deactivate(self):
		self._window.remove_accel_group(self._accel)
		self._entry = None

		self._window = None
		self._plugin = None

	def init_entry(self, group, obj, keyval, mod):
		view = self._window.get_active_view()

		if not view:
			return False

		if not self._entry:
			self._entry = Entry(self._window.get_active_view(), "pattern:")
			self._entry.connect("execute", self.on_entry_execute)
			self._entry.connect("destroy", self.on_entry_destroy)

		self._entry.grab_focus()
		return True

	def on_entry_destroy(self, widget):
		self._entry = None
		if self.get_data("labels"):
			for k, v in self.get_data("labels").items():
				v[0].destroy()

	def on_entry_execute(self, widget):
		if self._entry.read_label() == "pattern:":
			return self.handle_pattern()
		else:
			return self.handle_shortcut()

	def handle_pattern(self):
		value = self._entry.read_input()
		regex = re.compile(value)
		view  = self._window.get_active_view()
		ha    = view.get_hadjustment()
		va    = view.get_vadjustment()
		doc   = view.get_buffer()
		if doc is not None:
			code = doc.get_text(*doc.get_bounds()).decode("utf-8")

			self.set_data("labels", {})
			i  = 0

			vp = va.get_value()
			hp = ha.get_value()

			for match in regex.finditer(code):
				iter = doc.get_iter_at_offset( match.start() )
				location = view.get_iter_location(iter)
				key  = SHORTCUT_LABELS[i]
				i    = i + 1

				label = gtk.Label()
				label.modify_font(view.style.font_desc)
				label.set_markup(key)

				eb = gtk.EventBox()
				eb.add(label)
				eb.show_all()

				self.get_data("labels")[key] = [eb, iter]
				view.add_child_in_window(eb, gtk.TEXT_WINDOW_TEXT, int(location.x - hp), int(location.y - vp))

			self._entry.update_label("jump to:")
			self._entry.clear_input()

	def handle_shortcut(self):
		view = self._window.get_active_view()
		key  = self._entry.read_input().strip()

		view.get_buffer().place_cursor( self.get_data("labels")[key][1] )
		view.grab_focus()
