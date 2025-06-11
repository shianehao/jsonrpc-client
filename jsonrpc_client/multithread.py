import json

from PySide6.QtCore import (
    QThreadPool,
)
from PySide6.QtWidgets import (
    QMainWindow,
)

from jsonrpc_client.worker import Worker
from jsonrpc_client.ipc import TcpIpc

from jsonrpc_client.dlg.main_window import Ui_MainWindow

__author__ = "Roger Huang"
__copyright__ = "Copyright 2024, The JSONRPC Client Project"
__license__ = "Proprietary"
__version__ = "2.0.1"
__maintainer__ = "Roger Huang"
__email__ = "rogerhuang7@gmail.com"
__status__ = "Package"


class MainWindow(QMainWindow):
    def __init__(self, server_ip: str, port: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.lineEdit_registerName.textChanged.connect(self.enable_fire)
        self.ui.lineEdit_value.textChanged.connect(self.enable_fire)
        self.ui.pushButton_fire.clicked.connect(self.wade)

        self.threadpool = QThreadPool()
        thread_count = self.threadpool.maxThreadCount()
        print(f"Multithreading with maximum {thread_count} threads")

        self.worker = TcpIpc(server_ip=server_ip, port=port)
        worker = Worker(
            self.worker.run
        )  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)

    def enable_fire(self):
        reg = self.ui.lineEdit_registerName.text()
        val = self.ui.lineEdit_value.text()
        self.ui.pushButton_fire.setEnabled(
            True if reg and val else False)
        
    def wade(self):
        reg = self.ui.lineEdit_registerName.text()
        val = self.ui.lineEdit_value.text()
        sel = self.ui.comboBox_type.currentText()
        type = {
            "BIT":"BIT",
            "UINT":"WORD",
            "INT":"WORD",
            "STR":"STR"
            }.get(sel)
        
        if type != "STR":
            val = int(val)

        payload = {"type":"WRITE", type:{reg:val}}

        self.worker.write(json.dumps(payload))

    def progress_fn(self, msg:bytes):
        self.ui.plainText_eventView.appendPlainText(msg.decode())

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def recurring_timer(self):
        self.counter += 1
        self.label.setText(f"Counter: {self.counter}")

    def closeEvent(self, event):
        self.worker.close()
        self.threadpool.waitForDone()

        return super().closeEvent(event)
