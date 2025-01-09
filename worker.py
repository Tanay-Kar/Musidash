import subprocess
from PySide6.QtCore import Signal, QObject, QRunnable, Slot


# Worker class that will handle fetching the current date and time via CLI
class Metadata:
    def __init__(self, title="", artist="", album="", cover="", position=""):
        self.title = title
        self.artist = artist
        self.album = album
        self.cover = cover
        self.position = position


# Worker Signals to communicate between the worker and the main thread
class WorkerSignals(QObject):
    result = Signal(Metadata)  # Emit a Metadata object


# Worker class for fetching metadata asynchronously using QRunnable
class MetadataWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()  # Create the signal object

    @Slot()  # Indicate that this method can be run in a thread
    def run(self):
        """Main task for fetching metadata"""
        try:
            # Fetch metadata using playerctl commands
            title = self.run_command(["playerctl", "metadata", "xesam:title"])
            artist = self.run_command(["playerctl", "metadata", "xesam:artist"])
            album = self.run_command(["playerctl", "metadata", "xesam:album"])
            cover = self.run_command(["playerctl", "metadata", "mpris:artUrl"])
            position = self.run_command(["playerctl", "position"])

            # Create a Metadata object with the fetched data
            metadata = Metadata(
                title=title, artist=artist, album=album, cover=cover, position=position
            )
            # Emit the result to the main thread
            self.signals.result.emit(metadata)

        except Exception as e:
            print(f"Error fetching metadata: {e}")

    @staticmethod
    def run_command(command):
        """Runs a shell command and returns the output"""
        try:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            output, _ = process.communicate()
            return output.decode("utf-8").strip()  # Clean up the output
        except Exception as e:
            return f"Error: {str(e)}"
