import sys


from PyQt5.QtWidgets import (

    QApplication

)

from kitchenhelper_client.MainWindow import MainWindow

class App:
    def run(self):
        self.app = QApplication(sys.argv)
        self.win = MainWindow()
        self.win.showMaximized()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    sys._excepthook = sys.excepthook 
    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback) 
        sys.exit(1) 

    sys.excepthook = exception_hook 
    app = App()
    app.run()