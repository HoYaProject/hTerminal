from PyQt5.QtCore import QIODevice
from PyQt5.QtSerialPort import QSerialPort


MAX_PORT: int = 200


class HSerial(QSerialPort):
    def __init__(self):
        super().__init__()

        self.is_connect = False

    def scan_port(self) -> list[str]:
        port_list = []
        for i in range(MAX_PORT):
            port_name: str = f"COM{i + 1}"
            self.setPortName(port_name)
            if self.open(QIODevice.ReadWrite):
                port_list.append(port_name)
                self.close()
        return port_list

    def connect(self, port: str, baudrate: int) -> bool:
        self.setPortName(port)
        self.setBaudRate(baudrate)
        if self.open(QIODevice.ReadWrite):
            self.is_connect = True
        return self.is_connect

    def disconnect(self):
        self.is_connect = False
        self.close()

    def is_connect(self) -> bool:
        return self.is_connect
