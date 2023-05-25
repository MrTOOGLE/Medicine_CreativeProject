# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from src.ui.widgets.widgets import TableWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(600, 340)
        MainWindow.setMinimumSize(QtCore.QSize(600, 340))
        MainWindow.setMaximumSize(QtCore.QSize(600, 340))
        font = QtGui.QFont()
        font.setPointSize(30)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: rgb(40, 40, 60);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 20, 450, 38))
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

        self.searchResTable = TableWidget(self.centralwidget)
        self.searchResTable.setGeometry(QtCore.QRect(20, 70, 561, 251))
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(10)
        self.searchResTable.setFont(font)
        self.searchResTable.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.searchResTable.setStyleSheet("""
            background-color: rgb(85, 85, 105);
            color: white;
            border-radius: 10px;
        """)
        self.searchResTable.setObjectName("searchResTable")
        self.searchResTable.setColumnCount(2)
        self.searchResTable.setColumnWidth(0, 280)
        self.searchResTable.setColumnWidth(1, 280)


        self.btnSearch = QtWidgets.QPushButton(self.centralwidget)
        self.btnSearch.setGeometry(QtCore.QRect(480, 20, 100, 38))
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
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Application"))
        self.btnSearch.setText(_translate("MainWindow", "Search"))
