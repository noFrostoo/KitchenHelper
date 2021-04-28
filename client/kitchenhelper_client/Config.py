import json
import os
import sys
from kitchenhelper_client.pythonUi.ServerDialog import ServerDialog
from PyQt5.QtWidgets import (
  QMessageBox
)

class Config:
    def __init__(self):
        if os.path.isfile('config.json'):
            self._readConfig()
        else:
            self._createConfig()
         
    def _createConfig(self):
        #TODO: think how to display server dialog and get data from it
        self.dialog = ServerDialog()
        if self.dialog.exec():
            addres = self.dialog.getServerAddress()
        else:
            QMessageBox.critical(
            self.dialog,
            "Error",
            "<p>Dialog did not exited correctly</p>"
            )
            sys.exit()
        self.config = {
            'serverAddress': addres,
            'uuid': self._generateUuid()
        }
        self.updateConfig()

    def _readConfig(self):
        with open('config.json') as f:
            self.config = json.load(f)
    
    def updateConfig(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f)

    def getserverAddress(self):
        return self.config['serverAddress']

    def getUuid(self):
        return self.config['uuid']

    def setserverAddress(self, newServer):
        self.config['serverAddress'] = newServer
    
    def _generateUuid(self):
        #TODO: real uuid generation
        return 'tempUuid'