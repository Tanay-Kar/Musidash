from PySide6 import QtWidgets, QtCore, QtGui


class ProgressBarWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ProgressBarWidget, self).__init__()

        self.setFixedHeight(50)  # Set fixed height for the widget

        # Create main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Slider
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 100)  # Set the range for the slider

        # Add slider to main layout
        main_layout.addWidget(self.slider)

        # Create label layout
        label_layout = QtWidgets.QHBoxLayout()
        label_layout.setContentsMargins(0, 0, 0, 0)

        # Current duration label
        self.current_duration = QtWidgets.QLabel("0:00")
        self.current_duration.setFont(QtGui.QFont("Roboto", 9, QtGui.QFont.Bold))
        self.current_duration.setAlignment(QtCore.Qt.AlignLeft)

        # Total duration label
        self.total_duration = QtWidgets.QLabel("3:00")
        self.total_duration.setFont(QtGui.QFont("Roboto", 9, QtGui.QFont.Bold))
        self.total_duration.setAlignment(QtCore.Qt.AlignRight)

        # Add labels and stretch to label layout
        label_layout.addWidget(self.current_duration)
        label_layout.addStretch()
        label_layout.addWidget(self.total_duration)

        # Add label layout to main layout
        main_layout.addLayout(label_layout)

        # Set main layout
        self.setLayout(main_layout)


# Example usage
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    progressBarWidget = ProgressBarWidget()
    progressBarWidget.show()
    app.exec()
