from PySide6 import QtWidgets, QtCore, QtGui
from components.titlebar import TitleBar
from components.songinfo import SongInfoWidget
from components.playerctrl import PlayerControlWidget
from qframelesswindow import TitleBarBase


class LayoutA(TitleBarBase):
    def __init__(self, parent):
        super(LayoutA, self).__init__(parent)
        self.parent = parent
        self.setFixedHeight(122)

        # Main layout
        # self.setAutoFillBackground(True)
        self.main_widget = QtWidgets.QWidget(self)
        self.main_widget.setStyleSheet("background-color:#020202; border-radius: 8px;")
        main_layout = QtWidgets.QHBoxLayout(self)
        # main_layout.setContentsMargins(10, 10, 10, 10)

        # Cover image label
        self.coverImageLabel = QtWidgets.QLabel()
        self.coverImageLabel.setFixedSize(80, 80)
        self.coverImageLabel.setStyleSheet(
            """
            background-color: #003333;
            border-radius: 4px;
            """
        )  # Placeholder for cover image

        # Right-side layout
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.setContentsMargins(5, 0, 0, 0)

        # TitleBar widget
        self.titleBar = TitleBar(self.parent, "Song Title")
        right_layout.addWidget(self.titleBar)

        self.minBtn = self.titleBar.minimizeButton
        self.maxBtn = self.titleBar.maximizeButton
        self.closeBtn = self.titleBar.closeButton

        # Info and control layout
        info_control_layout = QtWidgets.QHBoxLayout()
        info_control_layout.setContentsMargins(0, 0, 0, 0)

        # SongInfoWidget
        self.songInfoWidget = SongInfoWidget("Song Title", "Author Name")
        info_control_layout.addWidget(self.songInfoWidget)

        # PlayerControlWidget
        self.playerControlWidget = PlayerControlWidget()
        info_control_layout.addWidget(self.playerControlWidget)

        right_layout.addStretch()

        # Add info and control layout to right-side layout
        right_layout.addLayout(info_control_layout)

        # Add cover image and right-side layout to main layout
        main_layout.addWidget(self.coverImageLabel)
        main_layout.addLayout(right_layout)

        # Set main layout
        # self.setLayout(main_layout)
        self.main_widget.setLayout(main_layout)
        self.setLayout(QtWidgets.QHBoxLayout(self))
        self.layout().addWidget(self.main_widget)

    def setCoverImage(self, path):
        if path.startswith("file://"):
            path = path[len("file://") :]
        pixmap = QtGui.QPixmap(path)
        if not pixmap.isNull():
            # Scale the pixmap to fit the label while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                self.coverImageLabel.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation,
            )

            # Create a rounded mask
            mask = QtGui.QPixmap(scaled_pixmap.size())
            mask.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(mask)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            path = QtGui.QPainterPath()
            path.addRoundedRect(
                0, 0, scaled_pixmap.width(), scaled_pixmap.height(), 5, 5
            )  # Adjust the rounding radius as needed
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()

            # Set the resulting pixmap on the label
            self.coverImageLabel.setPixmap(mask)

    def setSongInfo(self, title, author):
        self.songInfoWidget.setInfo(title, author)

    def setSource(self, source):
        self.titleBar.setSource(source)


# Example usage
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mainWidget = LayoutA(QtWidgets.QWidget())
    mainWidget.show()
    app.exec()
