import sys

from application import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow


class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        self.app = Ui_MainWindow()
        self.app.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())
