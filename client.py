#!/usr/bin/env python
import argparse
import logging

from PySide6.QtWidgets import QApplication

from jsonrpc_client.multithread import MainWindow

__author__ = "Roger Huang"
__copyright__ = "Copyright 2024, The JSONRPC Client Project"
__license__ = "Proprietary"
__version__ = "2.0.1"
__maintainer__ = "Roger Huang"
__email__ = "rogerhuang7@gmail.com"
__status__ = "Package"


def main():
    opts = argparse.ArgumentParser()
    opts.add_argument('serverip', help="server IP", type=str)
    opts.add_argument('port', help="Server service port", type=int)
    args = opts.parse_args()

    app = QApplication([])
    window = MainWindow(args.serverip, args.port)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()