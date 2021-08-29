from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QGroupBox,
    QLabel,
    QPushButton,
)

from color import COLOR_BLACK, COLOR_WHITE


class MerlotLab_UI(QWidget):
    def __init__(self, serial):
        super().__init__()

        # Serial
        self._serial = serial
        self._serial.connectSignal.connect(self.enable_ui)

        # Control
        self.led1_chkbox = QCheckBox()
        self.led2_chkbox = QCheckBox()
        self.led3_chkbox = QCheckBox()
        self.led_btn = QPushButton("Send")

        self.init_ui()
        self.enable_ui(False)

    def init_ui(self):
        # Wiget ---------------------------------------------------------------#
        # Control
        led1_label = QLabel("LED1")
        led1_label.setFixedWidth(30)
        led1_label.setAlignment(Qt.AlignCenter)
        led2_label = QLabel("LED2")
        led2_label.setFixedWidth(30)
        led2_label.setAlignment(Qt.AlignCenter)
        led3_label = QLabel("LED3")
        led3_label.setFixedWidth(30)
        led3_label.setAlignment(Qt.AlignCenter)

        self.led1_chkbox.setFixedWidth(30)
        self.led1_chkbox.setStyleSheet("margin-left: 5px")
        self.led2_chkbox.setFixedWidth(30)
        self.led2_chkbox.setStyleSheet("margin-left: 5px")
        self.led3_chkbox.setFixedWidth(30)
        self.led3_chkbox.setStyleSheet("margin-left: 5px")

        self.led_btn.clicked.connect(self.send_led_cmd)
        self.led_btn.setFixedWidth(80)
        self.led_btn.setFixedHeight(30)
        self.led_btn.setStyleSheet(
            f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
        )
        self.led_btn.setToolTip("Send LED command")

        # Layout --------------------------------------------------------------#
        ctrl_hlayout1 = QHBoxLayout()
        ctrl_hlayout1.addWidget(led1_label)
        ctrl_hlayout1.addWidget(led2_label)
        ctrl_hlayout1.addWidget(led3_label)

        ctrl_hlayout2 = QHBoxLayout()
        ctrl_hlayout2.addWidget(self.led1_chkbox)
        ctrl_hlayout2.addWidget(self.led2_chkbox)
        ctrl_hlayout2.addWidget(self.led3_chkbox)

        ctrl_vlayout = QVBoxLayout()
        ctrl_vlayout.addLayout(ctrl_hlayout1)
        ctrl_vlayout.addLayout(ctrl_hlayout2)

        ctrl_hlayout3 = QHBoxLayout()
        ctrl_hlayout3.addLayout(ctrl_vlayout)
        ctrl_hlayout3.addWidget(self.led_btn)
        ctrl_hlayout3.addStretch(1)

        ctrl_group = QGroupBox("MerlotLab Mesh")
        ctrl_group.setLayout(ctrl_hlayout3)

        hlayout = QHBoxLayout()
        hlayout.addWidget(ctrl_group)

        self.setLayout(hlayout)

    # Control ##################################################################
    def send_led_cmd(self):
        self._serial.write(
            f"rgb(10, {int(self.led1_chkbox.isChecked())}, {int(self.led2_chkbox.isChecked())}, {int(self.led3_chkbox.isChecked())})\n"
        )

    # Utility ##################################################################
    def enable_ui(self, en: bool):
        self.led_btn.setEnabled(en)
        if en is False:
            self.led_btn.setStyleSheet(
                f"color: {COLOR_WHITE}; background-color: {COLOR_BLACK}; font: bold;"
            )
        else:
            self.led_btn.setStyleSheet(
                f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
            )
