from PyQt5.QtCore import QIODevice
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


MAX_PORT: int = 200


class Serial_UI(QWidget):
    def __init__(self):
        super().__init__()

        self.serial = QSerialPort()

        # Settings
        self.port_cmb = QComboBox()
        self.baudrate_cmb = QComboBox()
        self.connect_btn = QPushButton("Connect")

        # Logging
        self.log_te = QTextEdit()

        # Tx
        self.tx_le = QLineEdit()
        self.tx_btn = QPushButton("Send")

        self.init_ui()

    def init_ui(self):
        # Wiget ################################################################
        # Settings
        port_label = QLabel("Port")
        port_label.setFixedWidth(70)
        self.scan_port()

        baudrate_label = QLabel("Baudrate")
        baudrate_label.setFixedWidth(70)
        self.scan_baudrate()

        self.connect_btn.setCheckable(True)
        self.connect_btn.clicked.connect(self.connect)
        self.connect_btn.setFixedWidth(80)
        self.connect_btn.setFixedHeight(50)

        # Logging
        self.log_te.setReadOnly(True)

        # Layout ###############################################################
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

        tx_hlayout = QHBoxLayout()
        tx_hlayout.addWidget(self.tx_le)
        tx_hlayout.addWidget(self.tx_btn)

        tx_group = QGroupBox("TX")
        tx_group.setLayout(tx_hlayout)

        vlayout = QVBoxLayout()
        vlayout.addWidget(settings_group)
        vlayout.addWidget(self.log_te)
        vlayout.addWidget(tx_group)

        self.setLayout(vlayout)

    def scan_port(self):
        for i in range(MAX_PORT):
            port_name: str = f"COM{i + 1}"
            self.serial.setPortName(port_name)
            if self.serial.open(QIODevice.ReadWrite):
                self.port_cmb.addItem(port_name)
                self.serial.close()

    def scan_baudrate(self):
        baudrates: list(str) = ["9600", "115200"]
        self.baudrate_cmb.addItems(baudrates)
        self.baudrate_cmb.setCurrentIndex(1)

    def connect(self):
        if self.connect_btn.isChecked():
            print("Connect")
            self.serial.setPortName(self.port_cmb.currentText())
            self.serial.setBaudRate(int(self.baudrate_cmb.currentText()))
            self.serial.open(QIODevice.ReadWrite)
            self.connect_btn.setText("Disconnect")
        else:
            self.serial.close()
            self.connect_btn.setText("Connect")
