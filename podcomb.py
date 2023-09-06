import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gio
import threading
import subprocess
from FileSelectWindow import FileSelectWindow

class PodCombApplication(Gtk.Application):

    image_path=""
    audio_path=""
    def __init__(self):
        super().__init__(application_id="eu.ottop.PodComb")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        win = FileSelectWindow(app)
        win.set_visible(True)

if __name__ == "__main__":
    app = PodCombApplication()
    app.run(None)