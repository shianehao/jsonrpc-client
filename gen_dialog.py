import os
import subprocess

__author__ = "Roger Huang"
__copyright__ = "Copyright 2024, The JSONRPC Client Project"
__license__ = "Proprietary"
__version__ = "2.0.1"
__maintainer__ = "Roger Huang"
__email__ = "rogerhuang7@gmail.com"
__status__ = "Package"


def gen_dialog():
    build_ui = [
            'pyside6-uic ui/main_window.ui -o jsonrpc_client/dlg/main_window.py',
            ]

    try:
        os.mkdir('jsonrpc_client/dlg')
    except FileExistsError:
        pass
    for x in build_ui:
        print(f'Run \'{x}\'')
        subprocess.run(x, shell=True)

if __name__ == '__main__':
    gen_dialog()
