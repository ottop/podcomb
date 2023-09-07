import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gio
from ProgressWindow import ProgressWindow
from datetime import datetime
from os.path import realpath, dirname

class FileSelectWindow(Gtk.ApplicationWindow):

    def __init__(self, app):

        # Set basic properties
        super().__init__(application=app)
        self.set_resizable(False)
        self.set_title("PodComb")
        self.set_default_size(300, 200)
        
        self.app = app

        self.app.imagePath=""
        self.app.audioPath=""

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        #Set up the options to launch an about dialog

        GLib.set_application_name("PodComb")

        self.aboutButton = Gtk.Button()
        self.aboutButton.set_icon_name("help-about")
        self.header.pack_start(self.aboutButton)
        
        self.aboutButton.connect("clicked", self.on_aboutButton_clicked)

        grid = Gtk.Grid()

        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)

        infoText = Gtk.Label()
        infoText.set_text("Welcome to PodComb.\n\nJust select your image file and audio file. Then click Combine.\n")
        infoText.set_justify(Gtk.Justification.CENTER)
        grid.attach(infoText, 0, 0, 3, 1)

        # Set up the buttons

        self.imageButton = Gtk.Button()
        imageButtonText = Gtk.Label(label="Select an image file")

        self.styleButton(self.imageButton, imageButtonText , "image-x-generic")

        self.imageButton.connect("clicked", self.on_imageButton_clicked)
        grid.attach(self.imageButton, 0, 1, 1, 1)

        self.audioButton = Gtk.Button()
        audioButtonText = Gtk.Label(label="Select an audio file")

        self.styleButton(self.audioButton, audioButtonText, "audio-x-generic")

        self.audioButton.connect("clicked", self.on_audioButton_clicked)
        grid.attach_next_to(self.audioButton, self.imageButton, Gtk.PositionType.BOTTOM, 1, 1)

        combineButton = Gtk.Button(label="Combine")

        combineButton.connect("clicked", self.on_combineButton_clicked)
        grid.attach_next_to(combineButton, self.imageButton, Gtk.PositionType.RIGHT, 2, 2)

        for button in {infoText, self.imageButton,self.audioButton,combineButton}:
            button.set_margin_top(5)
            button.set_margin_bottom(5)
            button.set_margin_start(5)
            button.set_margin_end(5)
  
        self.set_child(grid)
    
    def styleButton(self, button, buttonText, icon):

        hBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button.set_child(hBox)

        buttonImage = Gtk.Image()
        buttonImage.set_from_icon_name(icon)

        hBox.append(buttonImage)
        hBox.append(buttonText)

    #Set up button actions

    def on_imageButton_clicked(self, widget):
        self.file_chooser("image")

    def on_audioButton_clicked(self, widget):
        self.file_chooser("audio")

    def on_combineButton_clicked(self, widget):
        self.output_video_chooser()

    def on_aboutButton_clicked(self, widget):

        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self)  
        self.about.set_modal(self)  

        self.about.set_authors(["Otto Petäjä"])
        self.about.set_copyright("Copyright 2023 Otto Petäjä")
        self.about.set_license_type(Gtk.License.MIT_X11)
        self.about.set_website("https://ottop.eu")
        self.about.set_website_label("Check out my site")
        self.about.set_version("1.0")
        self.about.set_logo(Gtk.Image.new_from_file(realpath(dirname(__file__))+"/eu.ottop.PodComb.svg").get_paintable())

        self.about.set_visible(True)

    def file_chooser(self, fileType):

        self.openDialog = Gtk.FileDialog.new()
        self.openDialog.set_title("Select a File")

        typeFilter = Gtk.FileFilter()

        if fileType == "image":
            typeFilter.set_name("Image files")
            typeFilter.add_mime_type("image/*")

        elif fileType == "audio":
            typeFilter.set_name("Audio files")
            typeFilter.add_mime_type("audio/*")

        else:
            print("This shouldn't happen")
            typeFilter.set_name("All files")
            typeFilter.add_mime_type("*")

        filters = Gio.ListStore.new(Gtk.FileFilter) 
        filters.append(typeFilter)  

        self.openDialog.set_filters(filters) 
        self.openDialog.set_default_filter(typeFilter)
        self.openDialog.open(self, None, self.open_dialog_open_callback, fileType)
        
    #Function that runs after the user picks a file in the file chooser
    def open_dialog_open_callback(self, dialog, result, fileType):
        try:
            file = dialog.open_finish(result)

            if file is not None:

                print(f"File path: {file.get_path()}")

                if fileType == "image":
                    self.app.imagePath = file.get_path()
                    self.styleButton(self.imageButton, Gtk.Label(label=file.get_basename()), "image-x-generic")

                elif fileType == "audio":
                    self.app.audioPath = file.get_path()
                    self.styleButton(self.audioButton, Gtk.Label(label=file.get_basename()), "audio-x-generic")
                
                else:
                    print("This shouldn't happen")

        #Errors out when input file lacks read permissions or has some other problem. Will add a separate gui error dialog in a future release as it's not an urgent issue.
        except GLib.Error as error:
            print(f"Error opening file: {error.message}")
    
    def output_video_chooser(self):
        self.saveDialog = Gtk.FileDialog.new()
        
        typeFilter = Gtk.FileFilter()

        typeFilter.set_name("mp4")
        typeFilter.add_mime_type("video/mp4")

        filters = Gio.ListStore.new(Gtk.FileFilter) 
        filters.append(typeFilter)

        self.saveDialog.set_filters(filters) 
        self.saveDialog.set_default_filter(typeFilter)
        self.saveDialog.set_initial_name("CombinedVideo"+datetime.now().strftime("-%d.%m.%Y.-%H:%M:%S")+".mp4")
        self.saveDialog.save(self, None, self.open_dialog_save_callback)
        
    
    def open_dialog_save_callback(self, dialog, result):
        file = dialog.save_finish(result)
        if file is not None:

            print(f"File path: {file.get_path()}")

            filePath = file.get_path()

            loadingWindow = ProgressWindow()
            loadingWindow.set_transient_for(self)
            loadingWindow.set_modal(self)
            loadingWindow.set_visible(True)
            
            loadingWindow.process_video(self.app.imagePath, self.app.audioPath, filePath)
            self.__init__(self.app)
            
    
