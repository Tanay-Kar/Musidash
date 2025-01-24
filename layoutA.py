from PySide6 import QtWidgets, QtCore, QtGui
from components.titlebar import TitleBar
from components.songinfo import SongInfoWidget
from components.playerctrl import PlayerControlWidget
from qframelesswindow import TitleBarBase
import os
import requests
from urllib.parse import urlparse, unquote
import hashlib


class LayoutA(TitleBarBase):
    def __init__(self, parent):
        super(LayoutA, self).__init__(parent)
        self.parent = parent
        self.maxBtn.hide()
        self.closeBtn.hide()
        self.minBtn.hide()
        self.setFixedHeight(122)

        # Main layout
        # self.setAutoFillBackground(True)
        self.main_widget = QtWidgets.QWidget(self)
        self.main_widget.setStyleSheet("background-color:#020202; border-radius: 8px;")
        main_layout = QtWidgets.QHBoxLayout(self)
        # main_layout.setContentsMargins(10, 10, 10, 10)

        # Cover image label
        self.cover_image = QtWidgets.QLabel()
        self.cover_image.setFixedSize(80, 80)
        self.cover_image.setStyleSheet(
            """
            background-color: #333333;
            border-radius: 4px;
            """
        )  # Placeholder for cover image

        # Right-side layout
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.setContentsMargins(5, 5, 5, 5)

        # TitleBar widget
        self.main_layout = TitleBar(self.parent, "Song Title")
        right_layout.addWidget(self.main_layout)

        # Info and control layout
        info_control_layout = QtWidgets.QHBoxLayout()
        info_control_layout.setContentsMargins(0, 0, 0, 0)

        # SongInfoWidget
        self.song_info = SongInfoWidget("Song Title", "Author Name")
        info_control_layout.addWidget(self.song_info)

        # PlayerControlWidget
        self.player_control = PlayerControlWidget()
        info_control_layout.addWidget(self.player_control)

        right_layout.addStretch()

        # Add info and control layout to right-side layout
        right_layout.addLayout(info_control_layout)

        # Add cover image and right-side layout to main layout
        main_layout.addWidget(self.cover_image)
        main_layout.addLayout(right_layout)

        # Set main layout
        # self.setLayout(main_layout)
        self.main_widget.setLayout(main_layout)
        self.setLayout(QtWidgets.QHBoxLayout(self))
        self.layout().addWidget(self.main_widget)

    def assign_actions(self, action_worker):
        self.action_worker = action_worker
        self.player_control.play_button.clicked.connect(
            lambda: self.action_worker.playpause()
        )
        self.player_control.next_button.clicked.connect(
            lambda: self.action_worker.next()
        )
        self.player_control.prev_button.clicked.connect(
            lambda: self.action_worker.previous()
        )

    def get_coverimage_url(self, url, cache_dir="cache"):
        try:
            parsed_url = urlparse(url)

            # If it's already a file URL or local path
            if parsed_url.scheme == "file" or not parsed_url.scheme:
                path = unquote(parsed_url.path)
                if os.name == "nt" and path.startswith("/"):
                    path = path[1:]
                return path

            # For http/https URLs, download and cache
            elif parsed_url.scheme in ["http", "https"]:
                # Create cache directory if it doesn't exist
                os.makedirs(cache_dir, exist_ok=True)

                # Create a unique filename using URL hash
                url_hash = hashlib.md5(url.encode()).hexdigest()

                # Get file extension from URL or default to .jpg
                ext = os.path.splitext(parsed_url.path)[1]
                if not ext:
                    ext = ".jpg"

                cache_path = os.path.join(cache_dir, f"{url_hash}{ext}")

                # If not already cached, download the file
                if not os.path.exists(cache_path):
                    response = requests.get(url, stream=True)
                    response.raise_for_status()  # Raise exception for bad status codes

                    with open(cache_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                return cache_path

            else:
                raise ValueError(f"URL scheme '{parsed_url.scheme}' is not supported")

        except Exception as e:
            print(f"Error processing URL for cover image {url}: {str(e)}")
            return None

    def setCoverImage(self, path):
        path = self.get_coverimage_url(path)

        pixmap = QtGui.QPixmap(path)
        if not pixmap.isNull():
            label_size = self.cover_image.size()

            # Scale the pixmap to cover the label while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                label_size,
                QtCore.Qt.KeepAspectRatioByExpanding,
                QtCore.Qt.SmoothTransformation,
            )

            # Calculate the cropping rectangle
            x_offset = (scaled_pixmap.width() - label_size.width()) // 2
            y_offset = (scaled_pixmap.height() - label_size.height()) // 2
            rect = QtCore.QRect(
                x_offset, y_offset, label_size.width(), label_size.height()
            )

            # Crop the scaled pixmap to fit the label
            cropped_pixmap = scaled_pixmap.copy(rect)

            # Create a rounded mask
            mask = QtGui.QPixmap(cropped_pixmap.size())
            mask.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(mask)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            path = QtGui.QPainterPath()
            path.addRoundedRect(
                0, 0, cropped_pixmap.width(), cropped_pixmap.height(), 4, 4
            )
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, cropped_pixmap)
            painter.end()

            # Set the resulting pixmap on the label
            self.cover_image.setPixmap(mask)

    def setSongInfo(self, title, author):
        self.song_info.setInfo(title, author)

    def setSource(self, source):
        self.main_layout.setSource(source)

    def setPlayPauseStatus(self, status):
        self.player_control.setPlayPauseStatus(status)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mainWidget = LayoutA(QtWidgets.QWidget())
    mainWidget.show()
    app.exec()
