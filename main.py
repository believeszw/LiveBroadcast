import sys

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.uic import loadUi
import client

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QDialog()
    ui = client.UiDialog()
    ui.setupUi(MainWindow)
    from LoginWeb import SeleniumHandler
    login_process = SeleniumHandler()
    login_process.GetUi(ui)
    #启动线程
    # login_process.start()
    MainWindow.show()
    sys.exit(app.exec())
