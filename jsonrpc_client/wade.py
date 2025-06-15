import json

from PySide6 import QtCore
from PySide6.QtCore import Qt

class WadeModel(QtCore.QAbstractListModel):
    def __init__(self, wades=None, icons=None):
        super().__init__()
        self.wades = wades or []
        self.icons = icons or []


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