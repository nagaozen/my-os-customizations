# -*- coding: utf-8 -*-

# Gedit Macros plugin
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

ui_str = """
<ui>
	<menubar name="MenuBar">
		<menu name="ToolsMenu" action="Tools">
			<placeholder name="ToolsOps_3">
				<menu name="Macro" action="MacroPluginOptions">
					<menuitem action="StartRecordingMacro" name="Start recording macro"/>
					<menuitem action="StopRecordingMacro" name="Stop recording macro"/>
					<menuitem action="PlaybackMacro" name="Playback macro"/>
				</menu>
			</placeholder>
		</menu>
	</menubar>
	<toolbar name="ToolBar">
		<separator/>
		<toolitem action="StartRecordingMacro"/>
		<toolitem action="StopRecordingMacro"/>
		<toolitem action="PlaybackMacro"/>
		<separator/>
	</toolbar>
</ui>
"""

class MacrosWindowHelper:
	def __init__(self, plugin, window):
		self._window = window
		self._plugin = plugin

		self.install_ui()
		self._action_group.get_action('StartRecordingMacro').set_sensitive(True)
		self._action_group.get_action('StopRecordingMacro').set_sensitive(False)
		self._action_group.get_action('PlaybackMacro').set_sensitive(False)

	def deactivate(self):
		self.uninstall_ui()

		self._window = None
		self._plugin = None

	def update_ui(self):
		pass

	def install_ui(self):
		manager = self._window.get_ui_manager()

		self._action_group = gtk.ActionGroup("GeditMacrosPluginActions")
		self._action_group.add_actions([
			( "MacroPluginOptions" , gtk.STOCK_INFO        , _("Macro")                  , None         , _("Record and playback any key secquence"), None ),
			( "StartRecordingMacro", gtk.STOCK_MEDIA_RECORD, _("Start Recording Macro")  , None         , _("Start recording macro")                , self.on_start_recording ),
			( "StopRecordingMacro" , gtk.STOCK_MEDIA_STOP  , _("Stop Recording Macro")   , None         , _("Stop Recording Macro")                 , self.on_stop_recording ),
			( "PlaybackMacro"      , gtk.STOCK_MEDIA_PLAY  , _("Playback Recorded Macro"), "<Ctrl>comma", _("Playback Recorded Macro")              , self.on_playback )
		])

		manager.insert_action_group(self._action_group, -1)
		self._ui_id = manager.add_ui_from_string(ui_str)

	def uninstall_ui(self):
		manager = self._window.get_ui_manager()

		manager.remove_ui(self._ui_id)
		manager.remove_action_group(self._action_group)

		manager.ensure_update()

	def on_start_recording(self, action):
		handlers = []
		handlers.append( self._window.get_active_view().connect("key-press-event", self.on_key_event) )
		handlers.append( self._window.get_active_view().connect("key-release-event", self.on_key_event) )
		handlers.append( self._window.get_active_view().connect("move-cursor", self.on_move_event) )
		self._window.set_data("MacrosPluginHandlers", handlers)

		self._macro = []
		self._action_group.get_action('StartRecordingMacro').set_sensitive(False)
		self._action_group.get_action('StopRecordingMacro').set_sensitive(True)
		self._action_group.get_action('PlaybackMacro').set_sensitive(False)

	def on_stop_recording(self, action):
		handlers = self._window.get_data("MacrosPluginHandlers")
		for handler_id in handlers:
			self._window.get_active_view().disconnect(handler_id)

		self._action_group.get_action('StartRecordingMacro').set_sensitive(True)
		self._action_group.get_action('StopRecordingMacro').set_sensitive(False)
		self._action_group.get_action('PlaybackMacro').set_sensitive(True)

	def on_playback(self, action):
		for event in self._macro:
			print(event)
			event.put()

	def on_key_event(self, widget, event):
		print(event)
		self._macro.append(event.copy())

	def on_move_event(self, textview, step_size, count, extend_selection):
		print(textview, step_size, count, extend_selection)

class MacrosPlugin(gedit.Plugin):

	WINDOW_DATA_KEY = "MacrosPluginWindowData"

	def __init__(self):
		gedit.Plugin.__init__(self)

	def activate(self, window):
		helper = MacrosWindowHelper(self, window)
		window.set_data(self.WINDOW_DATA_KEY, helper)

	def deactivate(self, window):
		window.get_data(self.WINDOW_DATA_KEY).deactivate()
		window.set_data(self.WINDOW_DATA_KEY, None)

	def update_ui(self, window):
		window.get_data(self.WINDOW_DATA_KEY).update_ui()
