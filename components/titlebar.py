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


class TitleBar(QtWidgets.QWidget):
    def __init__(self, parent, title):
        super(TitleBar, self).__init__()

        self.setFixedHeight(20)  # Set fixed height for the title bar

        self.parent = parent

        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title label
        self.title_label = ElidingLabel(title)
        self.title_label.setAlignment(QtCore.Qt.AlignLeft)
        self.title_label.setFont(QtGui.QFont("Poppins", 8, 1000))
        # Add title label to layout and make it expand
        layout.addWidget(self.title_label, 1)

        # Window control buttons
        button_size = 20  # Size for square buttons
        self.close_button = QPushButton()
        self.close_button.setIcon(QIcon(":/icons/close.png"))
        self.close_button.setFixedSize(button_size, button_size)
        self.close_button.clicked.connect(
            self.parent.close
        )  # Close window when close button is clicked

        self.menu_button = QToolButton(self)
        self.menu_button.setIcon(QIcon(":/icons/dots.png"))
        self.menu_button.setPopupMode(QToolButton.InstantPopup)

        # Create the menu
        self.menu = QMenu(self)

        # Create a widget to hold the buttons
        quick_button_widget = QWidget(self)
        button_grid = QHBoxLayout(quick_button_widget)

        for i in range(3):
            button = QPushButton(f"Btn{i + 1}", quick_button_widget)
            button.setObjectName("quick-button")
            button.clicked.connect(
                lambda _, num=i + 1: self.parent.handle_menu_click("quick", num)
            )
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

        layout_labels = ["Minimal", "Expanded", "Square", "Micro"]
        for i in range(4):
            button = QPushButton(layout_labels[i], layout_button_widget)
            button.setObjectName("layout-button")

            button.clicked.connect(
                lambda _, num=i + 1: self.parent.handle_menu_click("layout", num)
            )
            # Add buttons to the grid layout
            button_grid.addWidget(button, i // 2, i % 2)

        # Create a QWidgetAction to hold the button widget
        layout_action = QWidgetAction(self)
        layout_action.setDefaultWidget(layout_button_widget)

        # Add the QWidgetAction to the menu
        self.menu.addSeparator()
        self.menu.addAction(layout_action)
        self.menu.setObjectName("menu")

        # Associate the menu with the tool button
        self.menu_button.setMenu(self.menu)

        # Add buttons to layout
        layout.addWidget(self.menu_button)
        layout.addWidget(self.close_button)

        # Set layout
        self.setLayout(layout)

    def setSource(self, source):
        self.title_label.setText(source)


# Example usage
if __name__ == "__main__":
    app = QApplication([])
    main_layout = TitleBar("My Application")
    main_layout.show()
    app.exec()
