import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gio
import threading
import subprocess
from ProgressWindow import ProgressWindow

class FileSelectWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        super().__init__(application=app)
        self.set_resizable(False)
        self.set_title("PodComb")
        self.set_default_size(300, 200)
        
        self.app = app

        grid = Gtk.Grid()

        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)

        infoText = Gtk.Label()
        infoText.set_text("Welcome to PodComb.\n\nJust select your image file and audio file. Then click Combine.\n")
        infoText.set_justify(Gtk.Justification.CENTER)
        grid.attach(infoText, 0, 0, 3, 1)

        self.button1 = Gtk.Button()
        button1text = Gtk.Label(label="Select an image file")

        self.styleButton(self.button1, button1text , "image-x-generic")

        self.button1.connect("clicked", self.on_button1_clicked)
        grid.attach(self.button1, 0, 1, 1, 1)

        self.button2 = Gtk.Button()
        button2text = Gtk.Label(label="Select an audio file")

        self.styleButton(self.button2, button2text, "audio-x-generic")

        self.button2.connect("clicked", self.on_button2_clicked)
        grid.attach_next_to(self.button2, self.button1, Gtk.PositionType.BOTTOM, 1, 1)

        button3 = Gtk.Button(label="Combine")

        button3.connect("clicked", self.on_button3_clicked)
        grid.attach_next_to(button3, self.button1, Gtk.PositionType.RIGHT, 2, 2)

        for button in {infoText, self.button1,self.button2,button3}:
            button.set_margin_top(5)
            button.set_margin_bottom(5)
            button.set_margin_start(5)
            button.set_margin_end(5)
  
        self.set_child(grid)
    
    def styleButton(self, button, buttontext, icon):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button.set_child(hbox)

        buttonimage = Gtk.Image()
        buttonimage.set_from_icon_name(icon)

        hbox.append(buttonimage)
        hbox.append(buttontext)

    def on_button1_clicked(self, widget):
        self.fileChooser("image")

    def on_button2_clicked(self, widget):
        self.fileChooser("audio")

    def on_button3_clicked(self, widget):
        loadingWindow = ProgressWindow(self.app)
        loadingWindow.set_visible(True)

        # Start video processing in the background
        loadingWindow.process_video(self.app.image_path, self.app.audio_path)

    def fileChooser(self, fileType):
        self.open_dialog = Gtk.FileDialog.new()
        self.open_dialog.set_title("Select a File")

        f = Gtk.FileFilter()

        if fileType == "image":
            f.set_name("Image files")
            f.add_mime_type("image/*")

        elif fileType == "audio":
            f.set_name("Audio files")
            f.add_mime_type("audio/*")

        else:
            print("This shouldn't happen")
            f.set_name("All files")
            f.add_mime_type("*")

        filters = Gio.ListStore.new(Gtk.FileFilter)  # Create a ListStore with the type Gtk.FileFilter
        filters.append(f)  # Add the file filter to the ListStore. You could add more.

        self.open_dialog.set_filters(filters)  # Set the filters for the open dialog
        self.open_dialog.set_default_filter(f)
        self.show_open_dialog(fileType)
        
    def show_open_dialog(self, fileType):
        self.open_dialog.open(self, None, self.open_dialog_open_callback, fileType)
        
    def open_dialog_open_callback(self, dialog, result, fileType):
        try:
            file = dialog.open_finish(result)

            if file is not None:

                print(f"File path is {file.get_path()}")

                if fileType == "image":
                    self.app.image_path = file.get_path()
                    self.styleButton(self.button1, Gtk.Label(label=file.get_basename()), "image-x-generic")

                elif fileType == "audio":
                    self.app.audio_path = file.get_path()
                    self.styleButton(self.button2, Gtk.Label(label=file.get_basename()), "audio-x-generic")
                
                else:
                    print("This shouldn't happen")

        except GLib.Error as error:
            print(f"Error opening file: {error.message}")