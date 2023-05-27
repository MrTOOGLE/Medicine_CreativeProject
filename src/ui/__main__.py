import sys

from application import Ui_MainWindow
from PyQt5.Qt import *
from textwrap import fill


class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        self.app = Ui_MainWindow()
        self.app.setupUi(self)
        self.configure()

    def configure(self):
        self.app.btnSearch.clicked.connect(self.search)

    def search(self):
        searching_text = fill(self.app.textEdit.toPlainText(), 65)
        self.app.tableWidget.setItem(0, 1, QTableWidgetItem(searching_text))

        item = QTableWidgetItem()
        self.app.tableWidget.setItem(0, 0, item)
        item.setIcon(QIcon("D:/_Python/Programs/Medicine/src/ui/test.jpeg"))
        self.app.tableWidget.setIconSize(QSize(200, 200))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())
