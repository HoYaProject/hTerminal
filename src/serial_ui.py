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


class Serial_UI(QWidget):
    def __init__(self):
        super().__init__()

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

        baudrate_label = QLabel("Baudrate")
        baudrate_label.setFixedWidth(70)

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
