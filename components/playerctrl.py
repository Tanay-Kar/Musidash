from PySide6 import QtWidgets, QtCore


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
        self.playButton = QtWidgets.QPushButton("▶")
        self.playButton.setFixedSize(button_size, button_size)

        # Previous button
        self.prevButton = QtWidgets.QPushButton("⏮")
        self.prevButton.setFixedSize(button_size, button_size)

        # Next button
        self.nextButton = QtWidgets.QPushButton("⏭")
        self.nextButton.setFixedSize(button_size, button_size)

        # Add buttons to layout
        layout.addWidget(self.prevButton)
        layout.addWidget(self.playButton)
        layout.addWidget(self.nextButton)

        # Set layout
        self.setLayout(layout)


# Example usage
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    playerControl = PlayerControlWidget()
    playerControl.show()
    app.exec()
