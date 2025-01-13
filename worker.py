import subprocess
from PySide6.QtCore import Signal, QObject, QRunnable, Slot


# Worker class that will handle fetching the current date and time via CLI
class Metadata:
    def __init__(self, status="", title="", artist="", album="", cover="", position="", source=""):
        self.status = status
        self.title = title
        self.artist = artist
        self.album = album
        self.cover = cover
        self.position = position
        self.source = source.title()


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
            status = self.run_command(["playerctl", "status"])
            title = self.run_command(["playerctl", "metadata", "xesam:title"])
            artist = self.run_command(["playerctl", "metadata", "xesam:artist"])
            album = self.run_command(["playerctl", "metadata", "xesam:album"])
            cover = self.run_command(["playerctl", "metadata", "mpris:artUrl"])
            position = self.run_command(["playerctl", "position"])
            source = self.run_command(["sh", "-c", "busctl --user list | grep -f <(playerctl -l) | awk '{print $3}'"])

            # Create a Metadata object with the fetched data
            metadata = Metadata(status, title, artist, album, cover, position, source)
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
