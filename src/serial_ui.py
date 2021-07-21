from PyQt5.QtCore import QSettings, QIODevice
from PyQt5.QtSerialPort import QSerialPort
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QComboBox,
    QPushButton,
    QTextEdit,
    QLineEdit,
)

from color import (
    COLOR_BG,
    COLOR_BLACK,
    COLOR_LIGHT_BLACK,
    COLOR_WHITE,
)
from hlogger import HLogger


MAX_PORT: int = 200
BAUDRATES: list[str] = ["9600", "115200"]


class Serial_UI(QWidget):
    def __init__(self):
        super().__init__()

        # Settings
        self.settings = QSettings("ChameleoN", "hTerminal")

        # Serial
        self.serial = QSerialPort()

        # Settings
        self.port_cmb = QComboBox()
        self.baudrate_cmb = QComboBox()
        self.connect_btn = QPushButton("Connect")

        # Logging
        self.log_te = QTextEdit()
        self.logger = HLogger(self.log_te)

        # Tx
        self.tx_le = QLineEdit()
        self.tx_btn = QPushButton("Send")

        self.init_ui()
        self.enable_ui(False)
        self.load_settings()

    def init_ui(self):
        # Wiget ---------------------------------------------------------------#
        # Serial
        self.serial.readyRead.connect(self.read_data)

        # Settings
        port_label = QLabel("Port")
        port_label.setFixedWidth(70)
        self.port_cmb.setStyleSheet(f"border: 2px solid {COLOR_LIGHT_BLACK};")
        self.scan_port()

        baudrate_label = QLabel("Baudrate")
        baudrate_label.setFixedWidth(70)
        self.baudrate_cmb.setStyleSheet(f"border: 2px solid {COLOR_LIGHT_BLACK};")
        self.scan_baudrate()

        self.connect_btn.setCheckable(True)
        self.connect_btn.clicked.connect(self.connect)
        self.connect_btn.setFixedWidth(80)
        self.connect_btn.setFixedHeight(50)
        self.connect_btn.setStyleSheet(
            f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
        )

        # Logging
        self.log_te.setReadOnly(True)
        self.log_te.setFontFamily("consolas")
        self.log_te.setFontPointSize(8)

        # Tx
        tx_mode_label = QLabel("Mode: String")
        self.tx_le.returnPressed.connect(self.send_data)
        # self.tx_le.returnPressed.connect(self.tx_btn.click)
        self.tx_le.setStyleSheet(f"border: 2px solid {COLOR_LIGHT_BLACK};")
        self.tx_btn.clicked.connect(self.send_data)
        self.tx_btn.setStyleSheet(
            f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
        )

        # Layout --------------------------------------------------------------#
        settings_vlayout_1 = QVBoxLayout()
        settings_vlayout_1.addWidget(port_label)
        settings_vlayout_1.addWidget(baudrate_label)

        settings_vlayout_2 = QVBoxLayout()
        settings_vlayout_2.addWidget(self.port_cmb)
        settings_vlayout_2.addWidget(self.baudrate_cmb)

        settings_hlayout = QHBoxLayout()
        settings_hlayout.addLayout(settings_vlayout_1)
        settings_hlayout.addLayout(settings_vlayout_2)
        settings_hlayout.addWidget(self.connect_btn)

        settings_group = QGroupBox("Settings")
        settings_group.setLayout(settings_hlayout)

        tx_hlayout_1 = QHBoxLayout()
        tx_hlayout_1.addWidget(tx_mode_label)

        tx_hlayout_2 = QHBoxLayout()
        tx_hlayout_2.addWidget(self.tx_le)
        tx_hlayout_2.addWidget(self.tx_btn)

        tx_vlayout = QVBoxLayout()
        tx_vlayout.addLayout(tx_hlayout_1)
        tx_vlayout.addLayout(tx_hlayout_2)

        tx_group = QGroupBox("TX")
        tx_group.setLayout(tx_vlayout)

        vlayout = QVBoxLayout()
        vlayout.addWidget(settings_group)
        vlayout.addWidget(self.log_te)
        vlayout.addWidget(tx_group)

        self.setLayout(vlayout)

    # Serial ###################################################################
    def scan_port(self):
        for i in range(MAX_PORT):
            port_name: str = f"COM{i + 1}"
            self.serial.setPortName(port_name)
            if self.serial.open(QIODevice.ReadWrite):
                self.port_cmb.addItem(port_name)
                self.serial.close()

    def scan_baudrate(self):
        self.baudrate_cmb.addItems(BAUDRATES)
        self.baudrate_cmb.setCurrentIndex(1)

    def connect(self):
        if self.connect_btn.isChecked():
            self.serial.setPortName(self.port_cmb.currentText())
            self.serial.setBaudRate(int(self.baudrate_cmb.currentText()))
            self.serial.open(QIODevice.ReadWrite)
            self.enable_ui(True)
            self.connect_btn.setText("Disconnect")
        else:
            self.serial.close()
            self.enable_ui(False)
            self.connect_btn.setText("Connect")

    def read_data(self):
        data = str(self.serial.readAll(), "utf-8")
        self.log(data)

    def send_data(self):
        self.write_data()

    def write_data(self):
        self.log("\n")
        data = self.tx_le.text() + "\n"
        self.serial.write(data.encode("utf-8"))

    # Logging ##################################################################
    def log(self, msg):
        self.logger.logging(msg)

    def log_clear(self):
        self.log_te.clear()

    # Utility ##################################################################
    def enable_ui(self, en: bool):
        self.tx_le.setEnabled(en)
        self.tx_btn.setEnabled(en)
        if en is False:
            self.tx_le.setStyleSheet(
                f"background-color: {COLOR_BLACK}; border: 2px solid {COLOR_LIGHT_BLACK};"
            )
            self.tx_btn.setStyleSheet(
                f"color: {COLOR_WHITE}; background-color: {COLOR_BLACK}; font: bold;"
            )
        else:
            self.tx_le.setStyleSheet(
                f"background-color: {COLOR_BG}; border: 2px solid {COLOR_LIGHT_BLACK};"
            )
            self.tx_btn.setStyleSheet(
                f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
            )

    def save_settings(self):
        self.settings.setValue("port_name", self.port_cmb.currentText())
        self.settings.setValue("baudrate", self.baudrate_cmb.currentText())

    def load_settings(self):
        if self.settings.contains("port_name"):
            self.port_cmb.setCurrentIndex(
                self.port_cmb.findText(self.settings.value("port_name"))
            )
        if self.settings.contains("baudrate"):
            self.baudrate_cmb.setCurrentIndex(
                self.baudrate_cmb.findText(self.settings.value("baudrate"))
            )
