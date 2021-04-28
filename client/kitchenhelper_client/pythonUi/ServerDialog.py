import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
  QDialog
)
from PyQt5.QtCore import Qt, QEvent

class ServerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("kitchenhelper_client/ui/ServerDialog.ui", self)
        self.text.editingFinished.connect(self.dialogAccept)

    def getServerAddress(self):
        return self.addres
    
    def dialogAccept(self):
        self.addres = self.text.text()
        self.accept()

      
    # self.text.installEventFilter(self)
    # def self.close

    # # def keyPressEvent(self, e):
    # #     if e.key() == Qt.Key_Enter:
    # #         self.close()
    # #     return super().keyPressEvent(e)

    # def eventFilter(self, source, event):
    #   if event.type() == QEvent.KeyPress and source is self.text:
    #     if event.key() == Qt.Key_Enter:
    #       self.close()
    #   return super().eventFilter(source, event)
        