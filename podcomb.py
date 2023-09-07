import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib
from FileSelectWindow import FileSelectWindow

class PodCombApplication(Gtk.Application):
    imagePath=""
    audioPath=""
    def __init__(self):
        super().__init__(application_id="eu.ottop.PodComb")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        win = FileSelectWindow(app)
        win.set_visible(True)

if __name__ == "__main__":
    app = PodCombApplication()
    app.run(None)