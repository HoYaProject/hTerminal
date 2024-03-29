from PyQt5.QtGui import QColor


DEBUG_LIST: list[str] = ["DBG"]


class HLogger:
    def __init__(self, log):
        self._log = log
        self._msg = ""

    def logging(self, msg):
        for char in msg:
            if char == "\n":
                if any(word in self._msg for word in DEBUG_LIST):
                    self._log.setTextColor(QColor(240, 198, 116))
                else:
                    self._log.setTextColor(QColor(197, 200, 198))
                self._log.append(self._msg)
                self._msg = ""
            elif char == "\r":
                continue
            else:
                self._msg += char
