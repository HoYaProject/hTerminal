from PyQt5.QtGui import QColor


class HLogger:
    def __init__(self, log):
        self._log = log

    def logging(self, msg):
        msg = msg.rstrip()
        if msg != "":
            for c in msg:
                print(f"{c}, {ord(c)}")
            self._log.append(msg)
