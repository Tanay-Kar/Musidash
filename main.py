# coding:utf-8
import sys

from PySide6.QtCore import QTimer, Qt, QThreadPool
from PySide6.QtWidgets import QApplication
from PySide6 import QtGui  # noqa: F401

from qframelesswindow import FramelessWindow
from layoutA import LayoutA

from worker import MetadataWorker, Metadata, ActionsWorker


class Window(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.current_theme = "light"
        self.load_theme()

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
        self.timer.start(500)  # Update every 0.1 seconds

    def handle_menu_click(self, button_group, button_number):
        print(f"Button {button_group} {button_number} clicked!")
        if button_group == "quick":
            if button_number == 1:
                self.switch_theme()

    def load_theme(self):
        if self.current_theme == "dark":
            import components.assets.dark_theme_rc  # noqa: F401

            qss_file = "components/assets/dark.qss"
        else:
            import components.assets.light_theme_rc  # noqa: F401

            qss_file = "components/assets/light.qss"

        with open(qss_file, "r") as f:
            self.setStyleSheet(f.read())

    def switch_theme(self):
        if self.current_theme == "dark":
            self.current_theme = "light"
        else:
            self.current_theme = "dark"
        self.load_theme()

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


if __name__ == "__main__":
    # run app
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec())
