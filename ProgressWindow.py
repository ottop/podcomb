import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib
import threading
import subprocess
import os

class ProgressWindow(Gtk.Window):
    
    def __init__(self):

        # Set basic properties
        Gtk.Window.__init__(self, title="Video Processing")
        self.set_resizable(False)
        self.set_default_size(300, 100)

        # Set up a custom response to closing the progress window
        self.connect("close-request", self.on_close_button_clicked)

        self.vBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)

        self.vBox.set_margin_top(10)
        self.vBox.set_margin_bottom(10)
        self.vBox.set_margin_start(10)
        self.vBox.set_margin_end(10)

        self.progressText = Gtk.Label()
        self.progressText.set_text("Processing...")
        self.vBox.append(self.progressText)

        self.progressBar = Gtk.ProgressBar()
        self.vBox.append(self.progressBar)

        self.set_child(self.vBox)

    def process_video(self, imagePath, audioPath, outputPath):

        def process_thread():

            #Set the output path for the entire class so that it can be accessed in the window close response
            self.outputPath = outputPath

            self.processFinished = False

            # Use ffprobe to get audio duration for the progress bar
            try:
                ffprobeCommand = [
                    'ffprobe',
                    '-v', 'error',
                    '-show_entries', 'format=duration',
                    '-of', 'default=noprint_wrappers=1:nokey=1',
                    audioPath
                ]
                duration = float(subprocess.check_output(ffprobeCommand).strip())

                if imagePath == "":
                    raise subprocess.CalledProcessError("You are missing an image","")

            # If image or audio is missing
            except subprocess.CalledProcessError:
                self.progressBar.set_visible(False)
                self.progressText.set_text("Error: You are missing a file or there's an issue with the files")
                affirmButton = Gtk.Button(label = "OK")

                affirmButton.connect("clicked", self.on_affirmButton_clicked)
                self.vBox.append(affirmButton)
                raise PermissionError("Error: You are missing a file or there's an issue with the file types")

            ffmpegCommand = [
                'ffmpeg',
                '-loop', '1',
                '-i', imagePath,
                '-i', audioPath,
                '-c:v', 'libx264',
                '-tune', 'stillimage',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-pix_fmt', 'yuv420p',
                '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2',
                '-shortest',
                '-f', 'mp4',
                '-y',  
                outputPath
            ]

            # Create a subprocess and redirect stderr to a pipe
            self.process = subprocess.Popen(ffmpegCommand, stderr=subprocess.PIPE, universal_newlines=True)

            while True:
                line = self.process.stderr.readline()
                print(line)

                # In case you try to write to a directory without write access or there's some other error that is not covered previously
                if "No such file or directory" in line or "Permission denied" in line:
                    self.progressBar.set_visible(False)
                    self.progressText.set_text("Error: Unable to write to "+outputPath)
                    affirmButton = Gtk.Button(label = "OK")

                    affirmButton.connect("clicked", self.on_affirmButton_clicked)
                    self.vBox.append(affirmButton)
                    raise PermissionError("Cannot write to "+outputPath)

                if not line:
                    self.processFinished = True
                    break

                # Move the progress bar. Reads current time from ffmpeg output and calculates the progress by using the duration from earlier. 
                if "time=" in line:
                    timeString = line.split("time=")[1].split()[0]
                    convertedTime = sum(x * float(t) for x, t in zip([3600, 60, 1], timeString.split(":")))

                    progress = convertedTime / duration

                    GLib.idle_add(self.update_progress, progress)

            # Actions on success
            affirmButton = Gtk.Button(label = "OK")

            affirmButton.connect("clicked", self.on_affirmButton_clicked)
            self.vBox.append(affirmButton)

            self.progressText.set_text("Finished!")
            

        self.thread = threading.Thread(target=process_thread)
        self.thread.start()

    def on_affirmButton_clicked(self,widget):
        self.destroy()

    def update_progress(self, progress):
        self.progressBar.set_fraction(progress)
    
    def on_close_button_clicked(self, widget):

        self.process.kill()

        #Remove file if it isn't finished
        if not self.processFinished:
            if os.path.exists(self.outputPath):
                os.remove(self.outputPath)

        self.destroy()