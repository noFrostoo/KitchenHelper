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
    app = App()
    app.run()