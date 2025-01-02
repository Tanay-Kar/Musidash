from PySide6 import QtWidgets, QtCore, QtGui
from components.elide import ElidingLabel


class TitleBar(QtWidgets.QWidget):
    def __init__(self, parent, title):
        super(TitleBar, self).__init__()

        self.setFixedHeight(20)  # Set fixed height for the title bar

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
        self.parent = parent

        # Create layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title label
        self.titleLabel = ElidingLabel(title)
        self.titleLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.titleLabel.setFont(QtGui.QFont("Roboto", 7, QtGui.QFont.Bold))
        # Add title label to layout and make it expand
        layout.addWidget(self.titleLabel, 1)

        # Window control buttons
        button_size = 20  # Size for square buttons
        self.minimizeButton = QtWidgets.QPushButton("-")
        self.minimizeButton.setFixedSize(button_size, button_size)
        self.maximizeButton = QtWidgets.QPushButton("[]")
        self.maximizeButton.setFixedSize(button_size, button_size)
        self.closeButton = QtWidgets.QPushButton("x")
        self.closeButton.setFixedSize(button_size, button_size)
        self.closeButton.clicked.connect(
            self.parent.close
        )  # Close window when close button is clicked

        # Add buttons to layout
        layout.addWidget(self.minimizeButton)
        layout.addWidget(self.maximizeButton)
        layout.addWidget(self.closeButton)

        # Set layout
        self.setLayout(layout)

    def setSource(self, source):
        self.titleLabel.setText(source)


# Example usage
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    titleBar = TitleBar("My Application")
    titleBar.show()
    app.exec()
