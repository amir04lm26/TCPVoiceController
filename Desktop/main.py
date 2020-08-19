# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(747, 453)
        MainWindow.setStyleSheet("QMainWindow{\n"
"    /*background-color: #f6f6f6;*/\n"
"}\n"
"QFrame {\n"
"background-color: rgba(255, 255, 255, 0);\n"
"border-color: rgb(85, 170, 255);\n"
"/*font: 75 italic 12pt \"Sitka\";*/\n"
"}\n"
"/*QPushButton {\n"
"     background-color: #00aaff;\n"
"     color: rgb(255, 255, 255);\n"
"     border-radius: 8px;\n"
"    font: 14pt \"B Nazanin\";\n"
"    padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"     background-color: #9ee35d; border: 1px solid rgb(255, 85, 127);\n"
"}\n"
"QPushButton:pressed {\n"
"    outline: none;\n"
"}\n"
"QPushButton:focus {\n"
"    outline: none;\n"
"}*/\n"
"QLineEdit{\n"
"    font: italic 12pt \"Arial\";\n"
"}\n"
"QTextBrowser{\n"
"    background-color: #242320;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_3.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 4, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(100, 0))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 3, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setInputMask("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.lineEditPort = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditPort.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEditPort.setInputMask("")
        self.lineEditPort.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditPort.setObjectName("lineEditPort")
        self.gridLayout_2.addWidget(self.lineEditPort, 0, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem2, 0, 5, 1, 1)
        self.lamp = QtWidgets.QLabel(self.centralwidget)
        self.lamp.setMinimumSize(QtCore.QSize(40, 40))
        self.lamp.setMaximumSize(QtCore.QSize(40, 40))
        self.lamp.setText("")
        self.lamp.setObjectName("lamp")
        self.gridLayout_6.addWidget(self.lamp, 0, 1, 1, 1)
        self.fan = QtWidgets.QLabel(self.centralwidget)
        self.fan.setMinimumSize(QtCore.QSize(40, 40))
        self.fan.setMaximumSize(QtCore.QSize(40, 40))
        self.fan.setText("")
        self.fan.setObjectName("fan")
        self.gridLayout_6.addWidget(self.fan, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem3, 0, 3, 1, 1)
        self.voice = QtWidgets.QLabel(self.centralwidget)
        self.voice.setMinimumSize(QtCore.QSize(40, 40))
        self.voice.setMaximumSize(QtCore.QSize(40, 40))
        self.voice.setText("")
        self.voice.setObjectName("voice")
        self.gridLayout_6.addWidget(self.voice, 0, 4, 1, 1)
        self.clearLog = QtWidgets.QPushButton(self.centralwidget)
        self.clearLog.setMinimumSize(QtCore.QSize(100, 0))
        self.clearLog.setObjectName("clearLog")
        self.gridLayout_6.addWidget(self.clearLog, 0, 6, 1, 1)
        self.connection = QtWidgets.QLabel(self.centralwidget)
        self.connection.setMinimumSize(QtCore.QSize(40, 40))
        self.connection.setMaximumSize(QtCore.QSize(40, 40))
        self.connection.setText("")
        self.connection.setObjectName("connection")
        self.gridLayout_6.addWidget(self.connection, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_6, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "اتصال"))
        self.lineEdit.setText(_translate("MainWindow", "192.168.1.138"))
        self.lineEditPort.setText(_translate("MainWindow", "8085"))
        self.clearLog.setText(_translate("MainWindow", "حذف گزارشات"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
