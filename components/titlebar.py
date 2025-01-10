from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMenu,
    QToolButton,
    QWidget,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QWidgetAction,
)
from components.elide import ElidingLabel
from themes import theme_manager  # noqa: F401


class TitleBar(QtWidgets.QWidget):
    def __init__(self, parent, title):
        super(TitleBar, self).__init__()

        self.setFixedHeight(20)  # Set fixed height for the title bar

        self.setStyleSheet(
            """
            QPushButton {
                background-color: #020202;
                padding: 8px;
                border: none;
                color: #999;
                text-align: center;
            }

            QPushButton:hover {
                background-color: #222;
            }

            QToolButton {
                background-color: transparent;
                border: none;
                color: #999;
                text-align: center;
            }

            QToolButton:hover {
                background-color: #222;
            }
            QToolButton::menu-indicator {
                image: none;
            }
            """
        )
        self.parent = parent

        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title label
        self.titleLabel = ElidingLabel(title)
        self.titleLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.titleLabel.setFont(QtGui.QFont("Roboto", 7, QtGui.QFont.Bold))
        # Add title label to layout and make it expand
        layout.addWidget(self.titleLabel, 1)

        # Window control buttons
        button_size = 20  # Size for square buttons
        self.closeButton = QPushButton()
        self.closeButton.setIcon(QIcon(":/icons/close.png"))
        self.closeButton.setFixedSize(button_size, button_size)
        self.closeButton.clicked.connect(
            self.parent.close
        )  # Close window when close button is clicked

        self.menuButton = QToolButton(self)
        self.menuButton.setIcon(QIcon(":/icons/dots.png"))
        self.menuButton.setPopupMode(QToolButton.InstantPopup)

        # Create the menu
        self.menu = QMenu(self)

        # Create a widget to hold the buttons
        quick_button_widget = QWidget(self)
        button_grid = QHBoxLayout(quick_button_widget)

        buttons = []
        for i in range(3):
            button = QPushButton(f"Btn{i + 1}", quick_button_widget)
            buttons.append(button)
            # Add buttons to the hbox layout
            button_grid.addWidget(button)

        # Create a QWidgetAction to hold the button widget
        quick_action = QWidgetAction(self)
        quick_action.setDefaultWidget(quick_button_widget)

        # Add the QWidgetAction to the menu
        self.menu.addAction(quick_action)

        # Create a widget to hold the buttons
        layout_button_widget = QWidget(self)
        button_grid = QGridLayout(layout_button_widget)

        # Create 4 buttons for the 2x2 grid
        buttons = []
        layout_labels = ["Minimal", "Expanded", "Square", "Micro"]
        for i in range(4):
            button = QPushButton(layout_labels[i], layout_button_widget)
            buttons.append(button)
            # Add buttons to the grid layout
            button_grid.addWidget(button, i // 2, i % 2)

        # Create a QWidgetAction to hold the button widget
        layout_action = QWidgetAction(self)
        layout_action.setDefaultWidget(layout_button_widget)

        # Add the QWidgetAction to the menu
        self.menu.addAction(layout_action)

        # Associate the menu with the tool button
        self.menuButton.setMenu(self.menu)

        # Add buttons to layout
        layout.addWidget(self.menuButton)
        layout.addWidget(self.closeButton)

        # Set layout
        self.setLayout(layout)

    def setSource(self, source):
        self.titleLabel.setText(source)


# Example usage
if __name__ == "__main__":
    app = QApplication([])
    titleBar = TitleBar("My Application")
    titleBar.show()
    app.exec()
