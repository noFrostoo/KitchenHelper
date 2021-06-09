import sys
import traceback
from urllib.request import build_opener, install_opener

from PyQt5.QtWidgets import QMessageBox
from kitchenhelper_client.App import App

def main():
    def exception_hook(exctype, value, tb):
        """
        This hook captures uncaught exceptions and displays a message
        box containing exception details.
        """

        traceback.print_exception(exctype, value, tb)
        QMessageBox.critical(
            None,
            'Error',
            value.message if hasattr(value, 'message') else str(value)
        )
        exit(1)

    sys.excepthook = exception_hook

    opener = build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')]
    install_opener(opener)

    print('Hello, World!')
    app = App()
    app.run()

if __name__ == "__main__":
    main()

