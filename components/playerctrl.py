from PySide6 import QtWidgets
from PySide6.QtGui import QIcon
from themes import theme_manager  # noqa: F401


class PlayerControlWidget(QtWidgets.QWidget):
    def __init__(self):
        super(PlayerControlWidget, self).__init__()

        self.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
                color: #999;
                text-align: center;
            }

            QPushButton:hover {
                color: #EEE;
            }
            """
        )

        # Create layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)  # Fixed spacing between buttons

        # Button size
        button_size = 30  # Size for square buttons

        # Play button
        self.playButton = QtWidgets.QPushButton()
        self.playButton.setIcon(QIcon(":/icons/play.png"))
        self.playButton.setFixedSize(button_size, button_size)

        # Previous button
        self.prevButton = QtWidgets.QPushButton()
        self.prevButton.setIcon(QIcon(":/icons/prev.png"))
        self.prevButton.setFixedSize(button_size, button_size)

        # Next button
        self.nextButton = QtWidgets.QPushButton()
        self.nextButton.setIcon(QIcon(":/icons/next.png"))
        self.nextButton.setFixedSize(button_size, button_size)

        # Add buttons to layout
        layout.addWidget(self.prevButton)
        layout.addWidget(self.playButton)
        layout.addWidget(self.nextButton)

        # Set layout
        self.setLayout(layout)

    def setPlayPauseStatus(self, status):
        if status == "Playing":
            self.playButton.setIcon(QIcon(":/icons/pause.png"))
        elif status == "Paused":
            self.playButton.setIcon(QIcon(":/icons/play.png"))


# Example usage
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    playerControl = PlayerControlWidget()
    playerControl.show()
    app.exec()
