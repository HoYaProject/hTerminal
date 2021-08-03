import sys
import os

from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QWidget,
)

from color import COLOR_BG, COLOR_FG
from hserial import HSerial
from serial_ui import Serial_UI
from nxp_ui import NXP_UI


MAJOR_VERSION = 1
MINOR_VERSION = 0
PATCH_VERSION = 0


class HTerminal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = QSettings("ChameleoN", "hTerminal")

        self.serial = HSerial()

        self.init_ui()
        self.load_settings()

    def init_ui(self):
        hlayout = QHBoxLayout()
        hlayout.addWidget(Serial_UI(self.serial))
        hlayout.addWidget(NXP_UI(self.serial))
        central_widget = QWidget()
        central_widget.setLayout(hlayout)
        self.setCentralWidget(central_widget)

        self.setWindowIcon(QIcon(self.resource_path("./resource/favicon.ico")))
        self.setWindowTitle(
            "hTerminal for NXP v{}.{}.{}".format(
                MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION
            )
        )
        self.setStyleSheet(f"color: {COLOR_FG}; background-color: {COLOR_BG};")
        self.show()

    # Utility ##################################################################
    def closeEvent(self, event):
        for child_widget in self.findChildren(QWidget) + [self]:
            if hasattr(child_widget, "save_settings") and callable(
                child_widget.save_settings
            ):
                child_widget.save_settings()
        self.serial.close()
        super().closeEvent(event)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def save_settings(self):
        self.settings.setValue("geometry", self.saveGeometry())

    def load_settings(self):
        if self.settings.contains("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))
        else:
            self.setGeometry(100, 100, 600, 800)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = HTerminal()
    sys.exit(app.exec())
