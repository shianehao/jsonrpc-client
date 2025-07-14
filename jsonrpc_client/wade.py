import json

from PySide6 import QtCore
from PySide6.QtCore import Qt

__author__ = "Roger Huang"
__copyright__ = "Copyright 2025, The JSONRPC Client Project"
__license__ = "Proprietary"
__version__ = "2.0.1"
__maintainer__ = "Roger Huang"
__email__ = "rogerhuang7@gmail.com"
__status__ = "Package"


class WadeModel(QtCore.QAbstractListModel):
    def __init__(self, wades=None, icons=None):
        super().__init__()
        self.wades = wades or []
        self.icons = icons or []
        self.last_wade = None

    def wade(self, dir: str, reg_type: str, reg: str, val: str) -> dict:
        tran_type = {
            "BIT":"BIT",
            "UINT":"WORD",
            "INT":"WORD",
            "STR":"STR"
            }.get(reg_type)
        if tran_type != "STR":
            val = int(val)

        self.last_wade = {"type":dir, tran_type:{reg:val}}
        self.wades.append((0, self.last_wade))
        self.layoutChanged.emit()

        return self.last_wade

    def handle_result(self, status: int, key: str, msg: str) -> bool:
        if self.last_wade:
            if self.last_wade.get(key):
                # incase of timeout of wading
                _, prev = self.wades[-2]
                prev[key] = msg
                self.wades[-2] = (status, prev)
            else:
                self.last_wade[key] = msg
                self.wades[-1] = (status, self.last_wade)
            self.layoutChanged.emit()

            return True
        else:
            return False

    def data(self, index, role):
        if role == Qt.DisplayRole:
            _, obj = self.wades[index.row()]
            return json.dumps(obj)

        if role == Qt.DecorationRole:
            status, _ = self.wades[index.row()]
            if 0 > status > 2:
                status = 0
            return self.icons[status]

    def rowCount(self, index):
        return len(self.wades)