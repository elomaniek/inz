# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5 import Qt
import time
import subprocess
import threading
import signal
import psutil
server = None
import preview


class IP4Validator(Qt.QValidator):
    def __init__(self, parent=None):
        super(IP4Validator, self).__init__(parent)

    def validate(self, address, pos):
        if not address:
            return Qt.QValidator.Acceptable, pos
        octets = address.split(".")
        size = len(octets)
        if size > 4:
            return Qt.QValidator.Invalid, pos
        emptyOctet = False
        for octet in octets:
            if not octet or octet == "___" or octet == "   ": # check for mask symbols
                emptyOctet = True
                continue
            try:
                value = int(str(octet).strip(' _')) # strip mask symbols
            except:
                return Qt.QValidator.Intermediate, pos
            if value < 0 or value > 255:
                return Qt.QValidator.Invalid, pos
        if size < 4 or emptyOctet:
            return Qt.QValidator.Intermediate, pos
        return Qt.QValidator.Acceptable, pos

#Kill function is used to kill all processes in this APP
def kill():
    global server
    print("TERMINATE")
    parent = psutil.Process(server.pid)
    for child in parent.children(recursive=True):
        child.send_signal(signal.CTRL_C_EVENT)
        #On app close we not only need to kill flask server but also every other process that is running,
        #in this case we need to close ffmpeg
    parent.send_signal(signal.SIGTERM)
    server.wait()
    print("KILLED")
    return

class Ui_MainWindow(QtWidgets.QMainWindow):

    #Add funciolanity to close button
    def closeEvent(self, a0: QtGui.QCloseEvent):
        kill()
        a0.accept()
        return

    #Launch Button is used to start flask server and if checkbox - startStreamImmediately is marked, it will start deafult stream
    @pyqtSlot()
    def launch_button(self):
        global server
        print( self.lineServerIP.text())
        if self.startStreamImmediately.isChecked():
            server = subprocess.Popen('python app.py --ip ' +
                                      self.lineServerIP.text() +
                                      ' --name ' + self.lineName.text() +
                                      ' --pass ' + self.linePassword.text() , stderr= open('testlog.txt', 'a'))
        else:
            server = subprocess.Popen('python app.py --do-not-start-stream')

        return
    @pyqtSlot()
    def get_logs(self):
        data_list = open('testlog.txt', 'r').readlines()
        data_string = ""
        for line in data_list:
            data_string += line
            data_string += '\n'

        ui.appOutput.setPlainText(data_string)
        ui.appOutput.update()
        return

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(279, 306)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setObjectName("connectButton")
        self.connectButton.clicked.connect(self.launch_button)
        self.gridLayout_3.addWidget(self.connectButton, 5, 0, 1, 3)
        self.startStreamImmediately = QtWidgets.QCheckBox(self.centralwidget)
        self.startStreamImmediately.setWhatsThis("")
        self.startStreamImmediately.setChecked(True)
        self.startStreamImmediately.setObjectName("startStreamImmediately")
        self.gridLayout_3.addWidget(self.startStreamImmediately, 3, 2, 1, 1)
        self.appOutput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.appOutput.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.appOutput.setReadOnly(True)
        self.appOutput.setCenterOnScroll(True)
        self.appOutput.setPlaceholderText("")
        self.appOutput.setObjectName("appOutput")
        self.gridLayout_3.addWidget(self.appOutput, 8, 0, 1, 3)
        self.labelServerIP = QtWidgets.QLabel(self.centralwidget)
        self.labelServerIP.setObjectName("labelServerIP")
        self.gridLayout_3.addWidget(self.labelServerIP, 0, 0, 1, 1)
        self.labelName = QtWidgets.QLabel(self.centralwidget)
        self.labelName.setObjectName("labelName")
        self.gridLayout_3.addWidget(self.labelName, 1, 0, 1, 1)
        self.lineName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineName.setInputMask("")
        self.lineName.setMaxLength(30)
        self.lineName.setAlignment(QtCore.Qt.AlignCenter)
        self.lineName.setObjectName("lineName")
        regex = QtCore.QRegExp("[0-9a-zA-Z_]+")
        validator = QtGui.QRegExpValidator(regex)
        self.lineName.setValidator(validator)
        self.gridLayout_3.addWidget(self.lineName, 1, 1, 1, 2)
        self.labelStreamImmediately = QtWidgets.QLabel(self.centralwidget)
        self.labelStreamImmediately.setObjectName("labelStreamImmediately")
        self.gridLayout_3.addWidget(self.labelStreamImmediately, 3, 0, 1, 2)
        self.lineServerIP = QtWidgets.QLineEdit(self.centralwidget)
        self.lineServerIP.setAutoFillBackground(False)
        self.lineServerIP.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineServerIP.setMaxLength(15)
        self.lineServerIP.setFrame(True)
        self.lineServerIP.setAlignment(QtCore.Qt.AlignCenter)
        self.lineServerIP.setReadOnly(False)
        self.lineServerIP.setPlaceholderText("")
        self.lineServerIP.setObjectName("lineServerIP")
        #regex_ip = QtCore.QRegExp("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]).){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
        #validator_ip = QtGui.QRegExpValidator(regex_ip)
        #self.lineServerIP.setValidator(validator_ip)
        self.gridLayout_3.addWidget(self.lineServerIP, 0, 1, 1, 2)
        self.labelPassword = QtWidgets.QLabel(self.centralwidget)
        self.labelPassword.setObjectName("labelPassword")
        self.gridLayout_3.addWidget(self.labelPassword, 2, 0, 1, 1)
        self.previewButton = QtWidgets.QPushButton(self.centralwidget)
        self.previewButton.setObjectName("previewButton")
        self.previewButton.clicked.connect(preview.open_ffplay)
        self.gridLayout_3.addWidget(self.previewButton, 6, 0, 1, 3)
        self.linePassword = QtWidgets.QLineEdit(self.centralwidget)
        self.linePassword.setMaxLength(30)
        self.linePassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.linePassword.setAlignment(QtCore.Qt.AlignCenter)
        self.linePassword.setObjectName("linePassword")
        self.gridLayout_3.addWidget(self.linePassword, 2, 1, 1, 2)
        self.logsButton = QtWidgets.QPushButton(self.centralwidget)
        self.logsButton.setObjectName("logsButton")
        self.logsButton.clicked.connect(self.get_logs)
        self.gridLayout_3.addWidget(self.logsButton, 7, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CameraAPP"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.startStreamImmediately.setText(_translate("MainWindow", "YES"))
        self.labelServerIP.setText(_translate("MainWindow", "Server IP:"))
        self.labelName.setText(_translate("MainWindow", "Name:"))
        self.labelStreamImmediately.setText(_translate("MainWindow", "Do you want to start streaming immediately?"))
        #self.lineServerIP.setInputMask(_translate("MainWindow", "000.000.000.000"))
        #self.lineServerIP.setText(_translate("MainWindow", "..."))
        self.labelPassword.setText(_translate("MainWindow", "Password:"))
        self.previewButton.setText(_translate("MainWindow", "Video Preview"))
        self.logsButton.setText(_translate("MainWindow", "Get Logs"))



if __name__ == "__main__":
    import sys
    qt_app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.setupUi(ui)
    ui.show()
    #ui = ""

  # guiThread.join()
    sys.exit(qt_app.exec_())