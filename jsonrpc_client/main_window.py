import json

from PySide6.QtCore import (
    QThreadPool,
    QTimer,
)
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
)
from PySide6 import QtGui

from jsonrpc_client.worker import Worker
from jsonrpc_client.ipc import TcpIpc
from jsonrpc_client.wade import WadeModel

from jsonrpc_client.dlg.main_window import Ui_MainWindow
import jsonrpc_client.dlg.resources # noqa: F401

__author__ = "Roger Huang"
__copyright__ = "Copyright 2025, The JSONRPC Client Project"
__license__ = "Proprietary"
__version__ = "2.0.1"
__maintainer__ = "Roger Huang"
__email__ = "rogerhuang7@gmail.com"
__status__ = "Package"


class MainWindow(QMainWindow):
    def __init__(self, server_ip: str, port: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        app_ico = QtGui.QIcon(':/icons/app.ico')
        self.setWindowIcon(app_ico)

        self.ui.lineEdit_registerName.textChanged.connect(self.enable_fire)
        self.ui.lineEdit_value.textChanged.connect(self.enable_fire)
        self.ui.pushButton_fire.clicked.connect(self.wade)

        self.threadpool = QThreadPool()
        thread_count = self.threadpool.maxThreadCount()
        print(f"Multithreading with maximum {thread_count} threads")

        icons = [QtGui.QIcon(name) for name in \
                 [':/icons/question.png', ':/icons/tick.png', ':/icons/cross.png']]
        self.wade_model = WadeModel(icons=icons)
        self.ui.listView_controlView.setModel(self.wade_model)
        self.last_wade = None

        self.worker = TcpIpc(server_ip=server_ip, port=port)
        worker = Worker(
            self.worker.run
        )  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(print)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)
        self.timer = QTimer()

    def enable_fire(self):
        self.ui.pushButton_fire.setEnabled(True)

    def wade(self):
        dir = self.ui.comboBox_directive.currentText()
        reg = self.ui.lineEdit_registerName.text()
        reg_type = self.ui.comboBox_type.currentText()
        val = self.ui.lineEdit_value.text()

        if not reg:
            QMessageBox.warning(self, "Input Error",
                                "Register name cannot be empty.")
            return
        if dir != 'QUERY' and not val:
            QMessageBox.warning(self, "Input Error",
                                "Value cannot be empty.")
            return

        self.ui.pushButton_fire.setEnabled(False)

        wade_obj = self.wade_model.wade(dir=dir, reg_type=reg_type, val=val, reg=reg)
        if wade_obj:
            self.worker.write(json.dumps(wade_obj))
            self.timer.singleShot(1000, self.enable_fire)

    def wade_result(self, status: int, key: str, msg: str):
        if self.wade_model.handle_result(status, key, msg) is False:
            self.ui.plainText_eventView.appendPlainText(f'{key} : {msg}')
        if status == 2:
            # enable fire button on error case.
            self.enable_fire()

    def wade_handler(self, msg: str):
        self.enable_fire()
        if msg in ['done']:
            self.wade_result(1, 'wade', msg)
        else:
            self.wade_result(2, 'wade', msg)

    def status_handler(self, msg: str | dict):
        if isinstance(msg, dict):
            handlers = {
                'wade': self.wade_handler,
            }
            for k, v in msg.items():
                handler = handlers.get(k)
                if handler:
                    handler(v)
                    break
            else:
                self.ui.plainText_eventView.appendPlainText(f'{k} : {v}')
        else:
            self.ui.statusbar.showMessage(msg)

    def progress_fn(self, msg: str):
        handles = {
            'status': self.status_handler,
            'error': lambda x : self.wade_result(2, 'error', x),
            'result': lambda x : self.wade_result(1, 'result', x)
        }
        if msg:
            try:
                msg_dict = json.loads(msg)
            except Exception as e:
                print(f'JSON: {msg} : {e}')
                return
            if isinstance(msg_dict, dict) is False:
                print(f'MSG: {msg}')
                return

            for key, handler in handles.items():
                result = msg_dict.get(key)
                if result:
                    handler(result)
                    break
            else:
                self.ui.plainText_eventView.appendPlainText(msg)

    def thread_complete(self):
        print("THREAD COMPLETE!")
        self.close()

    def closeEvent(self, event):
        self.worker.close()
        self.threadpool.waitForDone()

        return super().closeEvent(event)
