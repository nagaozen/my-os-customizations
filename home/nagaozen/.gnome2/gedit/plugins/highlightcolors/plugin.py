# -*- coding: utf-8 -*-

# gedit HighlightColors plugin
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

import re

class Highlighter:

	def __init__(self, plugin, window):
		self._re = re.compile("(#[0-9a-fA-F]{6})|(#[0-9a-fA-F]{3})")
		# TODO: Match rgb(255,255,255) too, check "background-gdk" and <http://www.pygtk.org/pygtk2reference/class-gdkcolor.html>
#		self._re = re.compile("(#[0-9a-fA-F]{8})|(#[0-9a-fA-F]{6})|(#[0-9a-fA-F]{4})|(#[0-9a-fA-F]{3})|(rgb\(\s*[.0-9]+\%?\s*,\s*[.0-9]+\%?\s*,\s*[.0-9]+\%?\s*\))|(rgba\(\s*[.0-9]+\%?\s*,\s*[.0-9]+\%?\s*,\s*[.0-9]+\%?\s*,\s*[.0-9]+\%?\s*\))")

	def deactivate(self):
		pass

	def add_tag(self, doc, tag):
		if doc.get_tag_table().lookup(tag) is None:
			doc.create_tag(tag, background=tag)

	def highlight(self, doc):
		if doc is not None:
			code = doc.get_text(*doc.get_bounds()).decode("utf-8")
			for match in self._re.finditer(code):
				color_id = match.group(0)
				a = doc.get_iter_at_offset( match.start() )
				b = doc.get_iter_at_offset( match.end() )

				self.add_tag(doc, color_id)
				doc.apply_tag_by_name(color_id, a, b)

