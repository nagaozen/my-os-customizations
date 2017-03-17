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

import gobject
import gtk

class Entry(gtk.EventBox):

	__gsignals__ = {
		'execute' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, () )
 	}

	def __init__(self, view, label):
		gtk.EventBox.__init__(self)
		self._view = view

		hbox = gtk.HBox(False, 3)
		hbox.show()
		hbox.set_border_width(3)

		self._entry = gtk.Entry()
		self._entry.modify_font(self._view.style.font_desc)
		self._entry.set_has_frame(False)
		self._entry.set_name("command-bar")
		self._entry.modify_text(gtk.STATE_NORMAL, self._view.style.text[gtk.STATE_NORMAL])
		self._entry.set_app_paintable(True)

		self._entry.connect("realize", self.on_realize)
		self._entry.connect("expose-event", self.on_entry_expose)

		self._entry.show()

		self._prompt_label = gtk.Label()
		self._prompt_label = gtk.Label("<b>%s</b>" % label)
		self._prompt_label.set_use_markup(True)
		self._prompt_label.modify_font(self._view.style.font_desc)
		self._prompt_label.show()
		self._prompt_label.modify_fg(gtk.STATE_NORMAL, self._view.style.text[gtk.STATE_NORMAL])

		self.modify_bg(gtk.STATE_NORMAL, self.background_gdk())
		self._entry.modify_base(gtk.STATE_NORMAL, self.background_gdk())

		self._entry.connect("focus-out-event", self.on_entry_focus_out)
		self._entry.connect("key-press-event", self.on_entry_key_press)

		self.connect_after("size-allocate", self.on_size_allocate)
		self.connect_after("expose-event", self.on_expose)
		self.connect_after("realize", self.on_realize)

		hbox.pack_start(self._prompt_label, False, False, 0)
		hbox.pack_start(self._entry, True, True, 0)

		self.add(hbox)
		self.attach()

		self._entry.grab_focus()
		self._wait_timeout = 0

		self.connect("destroy", self.on_destroy)

		self._handlers = [
			[None, gtk.keysyms.Return  , self.on_execute],
			[None, gtk.keysyms.KP_Enter, self.on_execute]
		]

	def destroy(self):
		self.hide()
		gtk.EventBox.destroy(self)

	def attach(self):
		# Attach ourselves in the text view, and position just above the text window
		self._view.set_border_window_size(gtk.TEXT_WINDOW_BOTTOM, 1)
		alloc = self._view.allocation

		self.show()

		self._view.add_child_in_window(self, gtk.TEXT_WINDOW_BOTTOM, 0, 0)
		self.set_size_request(alloc.width, -1)

	def background_gdk(self):
		bg = self.background_color()
		bg = map(lambda x: int(x * 65535), bg)
		return gtk.gdk.Color(bg[0], bg[1], bg[2])

	def background_color(self):
		bg = self._view.get_style().base[self._view.state]
		return [bg.red / 65535.0 * 1.1, bg.green / 65535.0 * 1.1, bg.blue / 65535.0 * 0.9, 0.8]

	def view(self):
		return self._view

	def read_label(self):
		return self._prompt_label.get_text()

	def update_label(self, label = ''):
		self._prompt_label.set_markup("<b>%s</b>" % label)

	def read_input(self):
		return self._entry.get_text()

	def clear_input(self):
		self._entry.set_text('')

	def on_realize(self, widget):
		widget.window.set_back_pixmap(None, False)

	def on_entry_expose(self, widget, event):
		ct = event.window.cairo_create()
		ct.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)

		bg = self.background_color()
		ct.set_source_rgb(bg[0], bg[1], bg[1])
		ct.fill()

		return False

	def on_entry_focus_out(self, widget, event):
		if self._entry.flags() & gtk.SENSITIVE:
			self.destroy()

	def on_entry_key_press(self, widget, event):
		state = event.state & gtk.accelerator_get_default_mod_mask()
		text = self._entry.get_text()

		if event.keyval == gtk.keysyms.Escape:
			if text:
				self._entry.set_text('')
			else:
				self._view.grab_focus()
				self.destroy()
			return True

		for handler in self._handlers:
			if (handler[0] == None or handler[0] == state) and event.keyval == handler[1] and handler[2](state):
				return True

		return False

	def on_size_allocate(self, widget, alloc):
		vwwnd = self._view.get_window(gtk.TEXT_WINDOW_BOTTOM).get_parent()
		size = vwwnd.get_size()
		position = vwwnd.get_position()

		self._view.set_border_window_size(gtk.TEXT_WINDOW_BOTTOM, alloc.height)

	def on_expose(self, widget, event):
		ct = event.window.cairo_create()
		color = self.background_color()

		ct.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
		ct.clip()

		# Draw separator line
		ct.move_to(0, 0)
		ct.set_line_width(1)
		ct.line_to(self.allocation.width, 0)

		ct.set_source_rgb(1 - color[0], 1 - color[1], 1 - color[2])
		ct.stroke()
		return False

	def on_destroy(self, widget):
		self._view.set_border_window_size(gtk.TEXT_WINDOW_BOTTOM, 0)

	def on_execute(self, modifier):
		self.emit("execute")
		return True

