from setuptools import setup
from setuptools import Command

import subprocess
import os

class GenDialog(Command):
    description = 'Gen dialogs of the project'
    user_options = []
    
    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass

    def run(self):
        build_ui = [
            'pyside6-uic ui/main_window.ui -o jsonrpc_client/dlg/main_window.py',
            'pyside6-rcc ui/resources.qrc -o jsonrpc_client/dlg/resources.py',
            ]

        try:
            os.mkdir('jsonrpc_client/dlg')
        except FileExistsError:
            pass
        for x in build_ui:
            print(f'Run \'{x}\'')
        subprocess.run(x, shell=True)

setup(
    cmdclass={
        'gen_dialog' : GenDialog
    }
)
