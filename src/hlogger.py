from PyQt5.QtGui import QColor

GOOD_LIST: list[str] = ["success"]
DEBUG_LIST: list[str] = ["DBG"]
BAD_LIST: list[str] = ["error", "fail"]


class HLogger:
    def __init__(self, log):
        self._log = log
        self._msg = ""

    def logging(self, msg: str):
        for char in msg:
            if char == "\n":
                if any(word in self._msg for word in DEBUG_LIST):
                    self._log.setTextColor(QColor(240, 198, 116))
                elif any(word in self._msg.lower() for word in GOOD_LIST):
                    self._log.setTextColor(QColor(140, 148, 64))
                elif any(word in self._msg.lower() for word in BAD_LIST):
                    self._log.setTextColor(QColor(165, 66, 66))
                else:
                    self._log.setTextColor(QColor(197, 200, 198))
                self._log.append(self._msg)
                self._msg = ""
            elif char == "\r":
                continue
            else:
                self._msg += char
