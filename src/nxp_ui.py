from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QPushButton


from color import (
    COLOR_BG,
    COLOR_BLACK,
    COLOR_LIGHT_BLACK,
    COLOR_WHITE,
)


class NXP_UI(QWidget):
    def __init__(self, serial):
        super().__init__()

        # Serial
        self._serial = serial
        self._serial.connectSignal.connect(self.enable_ui)

        # Control
        self.ctrl_reset_btn = QPushButton("Reset")
        self.ctrl_form_btn = QPushButton("Format")
        self.ctrl_steer_btn = QPushButton("Permit")

        self.init_ui()
        self.enable_ui(False)

    def init_ui(self):
        # Wiget ---------------------------------------------------------------#
        # Control
        self.ctrl_reset_btn.clicked.connect(self.ctrl_reset)
        self.ctrl_reset_btn.setFixedWidth(80)
        self.ctrl_reset_btn.setStyleSheet(
            f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
        )

        self.ctrl_form_btn.clicked.connect(self.ctrl_form)
        self.ctrl_form_btn.setFixedWidth(80)
        self.ctrl_form_btn.setStyleSheet(
            f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
        )

        self.ctrl_steer_btn.clicked.connect(self.ctrl_steer)
        self.ctrl_steer_btn.setFixedWidth(80)
        self.ctrl_steer_btn.setStyleSheet(
            f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
        )

        # Layout --------------------------------------------------------------#
        ctrl_hlayout = QHBoxLayout()
        ctrl_hlayout.addWidget(self.ctrl_reset_btn)
        ctrl_hlayout.addWidget(self.ctrl_form_btn)
        ctrl_hlayout.addWidget(self.ctrl_steer_btn)

        ctrl_group = QGroupBox("Network Control")
        ctrl_group.setLayout(ctrl_hlayout)

        vlayout = QVBoxLayout()
        vlayout.addWidget(ctrl_group)
        vlayout.addStretch(1)

        self.setLayout(vlayout)

    # Control ##################################################################
    def ctrl_reset(self):
        self._serial.write("factory reset\n")

    def ctrl_form(self):
        self._serial.write("form\n")

    def ctrl_steer(self):
        self._serial.write("steer\n")

    # Utility ##################################################################
    def enable_ui(self, en: bool):
        self.ctrl_reset_btn.setEnabled(en)
        if en is False:
            self.ctrl_reset_btn.setStyleSheet(
                f"color: {COLOR_WHITE}; background-color: {COLOR_BLACK}; font: bold;"
            )
            self.ctrl_form_btn.setStyleSheet(
                f"color: {COLOR_WHITE}; background-color: {COLOR_BLACK}; font: bold;"
            )
            self.ctrl_steer_btn.setStyleSheet(
                f"color: {COLOR_WHITE}; background-color: {COLOR_BLACK}; font: bold;"
            )
        else:
            self.ctrl_reset_btn.setStyleSheet(
                f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
            )
            self.ctrl_form_btn.setStyleSheet(
                f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
            )
            self.ctrl_steer_btn.setStyleSheet(
                f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
            )
