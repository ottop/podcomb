import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gio
import threading
import subprocess

class ProgressWindow(Gtk.Window):
    
    def __init__(self, app):
        Gtk.Window.__init__(self, title="Video Processing")
        self.set_resizable(False)
        self.set_default_size(300, 100)

        self.app = app

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)

        self.vbox.set_margin_top(10)
        self.vbox.set_margin_bottom(10)
        self.vbox.set_margin_start(10)
        self.vbox.set_margin_end(10)

        self.label = Gtk.Label()
        self.label.set_text("Processing...")
        self.vbox.append(self.label)

        self.progress_bar = Gtk.ProgressBar()
        self.vbox.append(self.progress_bar)

        self.set_child(self.vbox)

    def process_video(self, image_path, audio_path, output_path):
        def worker_thread():

            # Get the total duration of the audio file using ffprobe
            ffprobe_cmd = [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                self.app.audio_path
            ]
            duration = float(subprocess.check_output(ffprobe_cmd).strip())

            # Set up the ffmpeg command
            ffmpeg_cmd = [
                'ffmpeg',
                '-loop', '1',
                '-i', self.app.image_path,
                '-i', self.app.audio_path,
                '-c:v', 'libx264',
                '-tune', 'stillimage',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-pix_fmt', 'yuv420p',
                '-shortest',
                '-y',  # Overwrite output file if it exists
                output_path
            ]

            # Create a subprocess and redirect stderr to a pipe
            process = subprocess.Popen(ffmpeg_cmd, stderr=subprocess.PIPE, universal_newlines=True)

            while True:
                line = process.stderr.readline()
                if not line:
                    break
                # Parse the ffmpeg output to get progress information
                if "time=" in line:
                    time_str = line.split("time=")[1].split()[0]
                    current_time = sum(x * float(t) for x, t in zip([3600, 60, 1], time_str.split(":")))
                    # Calculate the progress percentage
                    progress = current_time / duration
                    # Update the progress bar in the GTK main thread
                    GLib.idle_add(self.update_progress, progress)

            # Wait for the ffmpeg process to complete
            process.wait()

            # Actions on success
            affirmButton = Gtk.Button(label = "OK")

            affirmButton.connect("clicked", self.on_affirmButton_clicked)
            self.vbox.append(affirmButton)

            self.label.set_text("Finished!")
            
            print("Video created successfully!")

        self.thread = threading.Thread(target=worker_thread)
        self.thread.start()

    def on_affirmButton_clicked(self,widget):
        self.destroy()

    def update_progress(self, progress):
        self.progress_bar.set_fraction(progress)