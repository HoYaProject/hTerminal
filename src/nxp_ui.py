from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QTextEdit,
)

from color import COLOR_BG, COLOR_BLACK, COLOR_LIGHT_BLACK, COLOR_WHITE


class NXP_UI(QWidget):
    _rx_data = ""

    def __init__(self, serial):
        super().__init__()

        # Serial
        self._serial = serial
        self._serial.connectSignal.connect(self.enable_ui)
        self._serial.readSignal.connect(self.read_data)

        # Control
        self.ctrl_reset_btn = QPushButton("Reset")
        self.ctrl_form_btn = QPushButton("Form")
        self.ctrl_permit_btn = QPushButton("Permit")
        self.ctrl_child_btn = QPushButton("Child")

        # Node Information
        self.node_table = QTableWidget()

        # Notification
        self.noti_te = QTextEdit()

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
        self.ctrl_reset_btn.setToolTip("Reset to factory default")

        self.ctrl_form_btn.clicked.connect(self.ctrl_form)
        self.ctrl_form_btn.setFixedWidth(80)
        self.ctrl_form_btn.setStyleSheet(
            f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
        )
        self.ctrl_form_btn.setToolTip("Form a new network")

        self.ctrl_permit_btn.clicked.connect(self.ctrl_permit)
        self.ctrl_permit_btn.setFixedWidth(80)
        self.ctrl_permit_btn.setStyleSheet(
            f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
        )
        self.ctrl_permit_btn.setToolTip("Permit joining")

        self.ctrl_child_btn.clicked.connect(self.ctrl_get_children)
        self.ctrl_child_btn.setFixedWidth(80)
        self.ctrl_child_btn.setStyleSheet(
            f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
        )
        self.ctrl_child_btn.setToolTip("Get children")

        # Node Information
        self.node_table.setEnabled(False)
        self.node_table.setFixedHeight(146)
        self.node_table.setMinimumWidth(490)
        self.node_table.setColumnCount(5)
        self.node_table.setColumnWidth(0, 160)
        self.node_table.setColumnWidth(1, 80)
        self.node_table.setColumnWidth(2, 50)
        self.node_table.setColumnWidth(3, 110)
        self.node_table.setColumnWidth(4, 60)
        self.node_table.setHorizontalHeaderLabels(
            ["IEEE Addr", "Nwk Addr", "Type", "Description", "Version"]
        )
        self.node_table.horizontalHeader().setStretchLastSection(True)
        self.node_table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.node_table.setStyleSheet(
            f"color: {COLOR_WHITE}; background-color: {COLOR_BG}; gridline-color: {COLOR_LIGHT_BLACK};"
        )
        self.node_table.horizontalHeader().setStyleSheet(
            f"QHeaderView::section {{color: {COLOR_WHITE}; background-color: {COLOR_BLACK}; font: bold; border: 1px solid {COLOR_LIGHT_BLACK};}}"
        )
        self.node_table.verticalHeader().setStyleSheet(
            f"QHeaderView::section {{color: {COLOR_WHITE}; background-color: {COLOR_BLACK}; font: bold; border: 1px solid {COLOR_LIGHT_BLACK};}}"
        )

        # Notification
        time_label = QLabel("Time")
        time_label.setFixedWidth(120)
        time_label.setAlignment(Qt.AlignCenter)
        src_label = QLabel("Source")
        src_label.setFixedWidth(50)
        src_label.setAlignment(Qt.AlignCenter)
        msg_label = QLabel("     Message")

        self.noti_te.setReadOnly(True)
        self.noti_te.setFontFamily("consolas")
        self.noti_te.setFontPointSize(8)
        self.noti_te.setStyleSheet(f"border: 2px solid {COLOR_LIGHT_BLACK};")

        # Layout --------------------------------------------------------------#
        ctrl_hlayout = QHBoxLayout()
        ctrl_hlayout.addWidget(self.ctrl_reset_btn)
        ctrl_hlayout.addWidget(self.ctrl_form_btn)
        ctrl_hlayout.addWidget(self.ctrl_permit_btn)
        ctrl_hlayout.addWidget(self.ctrl_child_btn)
        ctrl_hlayout.addStretch(1)

        ctrl_group = QGroupBox("Network Control")
        ctrl_group.setLayout(ctrl_hlayout)

        node_hlayout = QHBoxLayout()
        node_hlayout.addWidget(self.node_table)

        node_group = QGroupBox("Node information")
        node_group.setLayout(node_hlayout)

        noti_hlayout = QHBoxLayout()
        noti_hlayout.addWidget(time_label)
        noti_hlayout.addWidget(src_label)
        noti_hlayout.addWidget(msg_label)

        noti_vlayout = QVBoxLayout()
        noti_vlayout.addLayout(noti_hlayout)
        noti_vlayout.addWidget(self.noti_te)

        noti_group = QGroupBox("Notification")
        noti_group.setLayout(noti_vlayout)

        vlayout = QVBoxLayout()
        vlayout.addWidget(ctrl_group)
        vlayout.addWidget(node_group)
        vlayout.addWidget(noti_group)
        vlayout.setStretchFactor(noti_group, 1)

        self.setLayout(vlayout)

    # Control ##################################################################
    def ctrl_reset(self):
        self._serial.write("factory reset\n")

    def ctrl_form(self):
        self._serial.write("form\n")

    def ctrl_permit(self):
        self._serial.write("permit\n")

    def ctrl_get_children(self):
        self._serial.write("child\n")

    # Node Information #########################################################
    def new_node(self, data: str):
        token = data.split()
        ieee_addr = token[3].upper()
        ieee_addr = ":".join(ieee_addr[i : i + 2] for i in range(0, len(ieee_addr), 2))
        nwk_addr = token[4].upper()
        type = int(token[5], 16)
        if type & 0x01:
            node_type = "ZC"
        elif type & 0x20:
            node_type = "ZR"
        else:
            node_type = "ZED"

        rows = self.node_table.rowCount()
        is_exist = False
        if rows > 0:
            for r in range(rows):
                if self.node_table.item(r, 0).text() == ieee_addr:
                    self.set_cell(r, 1, nwk_addr)
                    self.set_cell(r, 2, node_type)
                    is_exist = True
                    break
        if not is_exist:
            self.node_table.insertRow(rows)
            self.set_cell(rows, 0, ieee_addr)
            self.set_cell(rows, 1, nwk_addr)
            self.set_cell(rows, 2, node_type)

    def leave_indication(self, data: str):
        token = data.split()
        ieee_addr = token[3].upper()
        ieee_addr = ":".join(ieee_addr[i : i + 2] for i in range(0, len(ieee_addr), 2))

        rows = self.node_table.rowCount()
        if rows > 0:
            for r in range(rows):
                if self.node_table.item(r, 0).text() == ieee_addr:
                    self.node_table.removeRow(r)

    def zdp_mgmt_lqi_rsp(self, data: str):
        token = data.split()
        ieee_addr = token[2].upper()
        ieee_addr = ":".join(ieee_addr[i : i + 2] for i in range(0, len(ieee_addr), 2))
        nwk_addr = token[3].upper()
        type = int(token[4], 16)
        if type == 0:
            node_type = "ZC"
        elif type == 1:
            node_type = "ZR"
        else:
            node_type = "ZED"

        rows = self.node_table.rowCount()
        is_exist = False
        if rows > 0:
            for r in range(rows):
                if self.node_table.item(r, 0).text() == ieee_addr:
                    self.set_cell(r, 1, nwk_addr)
                    self.set_cell(r, 2, node_type)
                    is_exist = True
                    break
        if not is_exist:
            self.node_table.insertRow(rows)
            self.set_cell(rows, 0, ieee_addr)
            self.set_cell(rows, 1, nwk_addr)
            self.set_cell(rows, 2, node_type)

    def zcl_data(self, data: str):
        token = data.split()
        src_addr = token[4][:-1].upper()
        cluster_id = token[6][:-1].upper()
        attr_type = token[8][:-1].upper()

        if cluster_id == "0000":
            if attr_type == "0001":
                data = str(int(token[10], 16))
                rows = self.node_table.rowCount()
                if rows > 0:
                    for r in range(rows):
                        if self.node_table.item(r, 1).text() == src_addr:
                            self.set_cell(r, 4, data)
            elif attr_type == "0005":
                data_len = int(token[10][:-1])
                data = bytes.fromhex(token[12]).decode("ascii")
                if data_len == len(data):
                    rows = self.node_table.rowCount()
                    if rows > 0:
                        for r in range(rows):
                            if self.node_table.item(r, 1).text() == src_addr:
                                self.set_cell(r, 3, data)
        elif cluster_id == "0400":
            if attr_type == "0000":
                data = int(token[10], 16)
                self.notification(
                    src_addr, f"{data} ({round(pow(10, (data - 1) / 10000), 6)} lx)"
                )
        elif cluster_id == "FCC0":
            if attr_type == "0112":
                data = token[10]
                self.notification(src_addr, f"{data[:4]} {data[4:]}")

    # Notification #############################################################
    def notification(self, src_addr: str, msg: str):
        now = datetime.now()
        msg_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.noti_te.append(f"[{msg_time}] {src_addr}  :  {msg}")

    # Utility ##################################################################
    def read_data(self, data: str):
        for char in data:
            if char == "\n":
                if "New Node" in self._rx_data:
                    self.new_node(self._rx_data)
                elif "Leave Indication" in self._rx_data:
                    self.leave_indication(self._rx_data)
                elif "MgmtLqiRsp" in self._rx_data:
                    self.zdp_mgmt_lqi_rsp(self._rx_data)
                elif "ZCL Attribute Report" in self._rx_data:
                    self.zcl_data(self._rx_data)
                self._rx_data = ""
            elif char == "\r":
                continue
            else:
                self._rx_data += char

    def set_cell(self, row: int, col: int, data: str):
        item = QTableWidgetItem(data)
        item.setTextAlignment(Qt.AlignCenter)
        self.node_table.setItem(row, col, item)

    def enable_ui(self, en: bool):
        self.ctrl_reset_btn.setEnabled(en)
        self.ctrl_form_btn.setEnabled(en)
        self.ctrl_permit_btn.setEnabled(en)
        self.ctrl_child_btn.setEnabled(en)
        if en is False:
            self.ctrl_reset_btn.setStyleSheet(
                f"color: {COLOR_WHITE}; background-color: {COLOR_BLACK}; font: bold;"
            )
            self.ctrl_form_btn.setStyleSheet(
                f"color: {COLOR_WHITE}; background-color: {COLOR_BLACK}; font: bold;"
            )
            self.ctrl_permit_btn.setStyleSheet(
                f"color: {COLOR_WHITE}; background-color: {COLOR_BLACK}; font: bold;"
            )
            self.ctrl_child_btn.setStyleSheet(
                f"color: {COLOR_WHITE}; background-color: {COLOR_BLACK}; font: bold;"
            )
        else:
            self.ctrl_reset_btn.setStyleSheet(
                f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
            )
            self.ctrl_form_btn.setStyleSheet(
                f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
            )
            self.ctrl_permit_btn.setStyleSheet(
                f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
            )
            self.ctrl_child_btn.setStyleSheet(
                f"color: {COLOR_BLACK}; background-color: {COLOR_WHITE}; font: bold;"
            )
