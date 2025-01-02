# coding:utf-8
import sys

from PySide6.QtCore import QRect, QSize, QThread, QTimer, Qt, QThreadPool
from PySide6.QtGui import QColor, QPixmap, QIcon
from PySide6.QtWidgets import QApplication, QLabel

from qframelesswindow import FramelessWindow, StandardTitleBar
from layoutA import LayoutA
import components
from worker import MetadataWorker, Metadata


class Window(FramelessWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = LayoutA(self)

        self.thread_pool = QThreadPool()

        self.titleBar.deleteLater()
        self.titleBar.hide()
        self.titleBar: LayoutA = layout
        self.titleBar.setParent(self)
        self.titleBar.raise_()

        self.setFixedHeight(120)
        self.setWindowTitle("TuneBar")
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.titleBar.setSongInfo("Feelings", "Shy Martin")
        
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
        self.titleBar.setSongInfo(metadata.title, metadata.artist)
        self.titleBar.setCoverImage(metadata.cover)
    



if __name__ == "__main__":
    # run app
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec())
