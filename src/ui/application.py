from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(900, 510)
        MainWindow.setMinimumSize(QtCore.QSize(900, 510))
        MainWindow.setMaximumSize(QtCore.QSize(1200, 680))
        font = QtGui.QFont()
        font.setPointSize(30)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: rgb(40, 40, 60);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 20, 741, 38))
        font = QtGui.QFont()
        font.setFamily("Cascadia Mono Light")
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textEdit.setStyleSheet("QTextEdit {\n"
"    background-color: rgb(85, 85, 105);\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"}")
        self.textEdit.setObjectName("textEdit")
        self.btnSearch = QtWidgets.QPushButton(self.centralwidget)
        self.btnSearch.setGeometry(QtCore.QRect(780, 20, 100, 38))
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(12)
        self.btnSearch.setFont(font)
        self.btnSearch.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.btnSearch.setStyleSheet("QPushButton {\n"
"    background-color: rgb(13, 245, 227);\n"
"    border-radius: 10px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(13, 225, 200);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(13, 245, 227);\n"
"}")
        self.btnSearch.setObjectName("btnSearch")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 70, 861, 421))
        self.tableWidget.setStyleSheet("""
            background-color: rgb(85, 85, 105);
            color: white;
        """)
        self.tableWidget.setFont(font)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setColumnWidth(0, 225)
        self.tableWidget.setColumnWidth(1, 602)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(5)
        for i in range(0, 5):
            self.tableWidget.setRowHeight(i, 180)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Application"))
        self.btnSearch.setText(_translate("MainWindow", "Search"))