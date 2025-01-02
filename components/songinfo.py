from PySide6 import QtWidgets, QtCore, QtGui
from components.elide import ElidingLabel


class SongInfoWidget(QtWidgets.QWidget):
    def __init__(self, title, author):
        super(SongInfoWidget, self).__init__()

        self.setFixedHeight(50)  # Set fixed height for the widget

        # Create layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title label
        self.titleLabel = ElidingLabel(title)
        self.titleLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.titleLabel.setFont(QtGui.QFont("Roboto", 12, QtGui.QFont.Bold))

        # Author label
        self.authorLabel = ElidingLabel(author)
        self.authorLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.authorLabel.setFont(QtGui.QFont("Roboto", 8, QtGui.QFont.Bold))

        # Add labels to layout
        layout.addWidget(self.titleLabel)
        layout.addWidget(self.authorLabel)

        # Set layout
        self.setLayout(layout)

    def setInfo(self, title, author):
        self.titleLabel.setText(title)
        self.authorLabel.setText(author)


# Example usage
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    songInfo = SongInfoWidget("Song Title", "Author Name")
    songInfo.show()
    app.exec()
