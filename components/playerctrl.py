from PySide6 import QtWidgets
from PySide6.QtGui import QIcon
# from themes import theme_manager  # noqa: F401


class PlayerControlWidget(QtWidgets.QWidget):
    def __init__(self):
        super(PlayerControlWidget, self).__init__()

        # Create layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)  # Fixed spacing between buttons

        # Button size
        button_size = 30  # Size for square buttons

        # Play button
        self.play_button = QtWidgets.QPushButton()
        self.play_button.setIcon(QIcon(":/icons/play.png"))
        self.play_button.setFixedSize(button_size, button_size)

        # Previous button
        self.prev_button = QtWidgets.QPushButton()
        self.prev_button.setIcon(QIcon(":/icons/prev.png"))
        self.prev_button.setFixedSize(button_size, button_size)

        # Next button
        self.next_button = QtWidgets.QPushButton()
        self.next_button.setIcon(QIcon(":/icons/next.png"))
        self.next_button.setFixedSize(button_size, button_size)

        # Add buttons to layout
        layout.addWidget(self.prev_button)
        layout.addWidget(self.play_button)
        layout.addWidget(self.next_button)

        # Set layout
        self.setLayout(layout)

    def setPlayPauseStatus(self, status):
        if status == "Playing":
            self.play_button.setIcon(QIcon(":/icons/pause.png"))
        elif status == "Paused":
            self.play_button.setIcon(QIcon(":/icons/play.png"))


# Example usage
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    player_control = PlayerControlWidget()
    player_control.show()
    app.exec()
