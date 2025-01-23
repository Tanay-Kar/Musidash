# coding:utf-8
import sys

from PySide6.QtCore import QTimer, Qt, QThreadPool
from PySide6.QtWidgets import QApplication
from PySide6 import QtGui

from qframelesswindow import FramelessWindow
from layoutA import LayoutA

# import components
from worker import MetadataWorker, Metadata, ActionsWorker
from themes import theme_manager  # noqa: F401


class Window(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = LayoutA(self)

        self.thread_pool = QThreadPool()
        self.action_worker = ActionsWorker()

        self.titleBar.deleteLater()
        self.titleBar.hide()
        self.titleBar: LayoutA = layout
        self.titleBar.setParent(self)
        self.titleBar.assign_actions(self.action_worker)

        self.setFixedHeight(120)  # Set fixed height for the title bar
        self.setWindowTitle("Musidash")
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.titleBar.setSongInfo("Title", "Author")
        self.titleBar.setSource("Player")

        self.timer = QTimer(self)
        self.timer.timeout.connect(
            self.update_metadata
        )  # Trigger worker on each timeout
        self.timer.start(1000)  # Update every 1 second (1000 ms)

    def update_metadata(self):
        # Create a worker and connect the result signal to the UI update method
        worker = MetadataWorker()
        worker.signals.result.connect(self.display_metadata)

        # Run the worker in the QThreadPool
        self.thread_pool.start(worker)

    def display_metadata(self, metadata: Metadata):
        """Update the QLabel values with the fetched metadata"""
        self.titleBar.setSource(metadata.source)
        self.titleBar.setSongInfo(metadata.title, metadata.artist)
        self.titleBar.setCoverImage(metadata.cover)
        self.titleBar.setPlayPauseStatus(metadata.status)

    def switchTheme(self):
        if self.current_theme == "dark":
            self.current_theme = "light"
            # Unload dark theme and load light theme
            QApplication.instance().loadStyleSheet("")
        else:
            self.current_theme = "dark"
            # Unload light theme and load dark theme
            QApplication.instance().loadStyleSheet("")


if __name__ == "__main__":
    # run app
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec())
