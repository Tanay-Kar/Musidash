from PySide6 import QtWidgets, QtCore, QtGui
from components.elide import ElidingLabel


class SongInfoWidget(QtWidgets.QWidget):
    def __init__(self, title, author):
        super(SongInfoWidget, self).__init__()

        self.setFixedHeight(50)  # Set fixed height for the widget
        # self.setStyleSheet("color: #333333;")
        # Create layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title label
        self.title_label = ElidingLabel(title)
        self.title_label.setAlignment(QtCore.Qt.AlignLeft)
        self.title_label.setFont(QtGui.QFont("Poppins", 12, 700))

        # Author label
        self.authorLabel = ElidingLabel(author)
        self.authorLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.authorLabel.setFont(QtGui.QFont("Poppins", 8, 900))

        # Add labels to layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.authorLabel)

        # Set layout
        self.setLayout(layout)

    def setInfo(self, title, author):
        self.title_label.setText(title)
        self.authorLabel.setText(author)


# Example usage
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    songInfo = SongInfoWidget("Song Title", "Author Name")
    songInfo.show()
    app.exec()
