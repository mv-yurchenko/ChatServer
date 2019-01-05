# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction
from Client.Client import Client
import sys


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.StartClientButton.clicked.connect(self.button_start_clicked)
        self.client_obj : Client

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.sendMessageButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendMessageButton.setGeometry(QtCore.QRect(380, 520, 111, 27))
        self.sendMessageButton.setObjectName("sendMessageButton")
        self.sendMessageButton.clicked.connect(self.send_message_button_clicked)
        self.inputMessageLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.inputMessageLineEdit.setGeometry(QtCore.QRect(30, 520, 321, 27))
        self.inputMessageLineEdit.setObjectName("inputMessageLineEdit")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 30, 461, 481))
        self.textBrowser.setObjectName("textBrowser")
        self.inputUsernameLabel = QtWidgets.QLabel(self.centralwidget)
        self.inputUsernameLabel.setGeometry(QtCore.QRect(490, 30, 111, 21))
        self.inputUsernameLabel.setObjectName("inpuUsernameLabel")
        self.inputUsernameLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.inputUsernameLineEdit.setGeometry(QtCore.QRect(600, 30, 150, 21))
        self.inputUsernameLineEdit.setObjectName("inputUsernameLineEdit")
        self.StartClientButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartClientButton.setGeometry(QtCore.QRect(751, 30, 46, 20))
        self.StartClientButton.setObjectName("StartClientButton")
        self.HostLabel = QtWidgets.QLabel(self.centralwidget)
        self.HostLabel.setGeometry(QtCore.QRect(490, 60, 41, 17))
        self.HostLabel.setObjectName("HostLabel")
        self.hostOutput = QtWidgets.QLineEdit(self.centralwidget)
        self.hostOutput.setGeometry(QtCore.QRect(530, 60, 113, 20))
        self.hostOutput.setObjectName("hostOutput")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        self.topMenu = QtWidgets.QMenu(self.menubar)
        self.topMenu.setObjectName("topMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.exit_button = QtWidgets.QAction(MainWindow)
        self.exit_button.setObjectName("actionExit")
        self.topMenu.addAction(self.exit_button)
        self.menubar.addAction(self.topMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sendMessageButton.setText(_translate("MainWindow", "Send Message"))
        self.inputUsernameLabel.setText(_translate("MainWindow", "Input Username"))
        self.StartClientButton.setText(_translate("MainWindow", "Start"))
        self.HostLabel.setText(_translate("MainWindow", "Host:"))
        self.topMenu.setTitle(_translate("MainWindow", "Menu"))
        self.exit_button.setText(_translate("MainWindow", "Exit"))
        self.exit_button.triggered.connect(self.button_exit_clicked)

    def button_start_clicked(self):
        # Return colour to black if btn was already pressed with empty field
        self.inputUsernameLineEdit.setStyleSheet("color:black")

        username = self.inputUsernameLineEdit.text()

        # If username is empty -> print red string
        if self.is_username_empty(username):
            # Output red text in inputMessageLineEdit
            self.inputUsernameLineEdit.setStyleSheet("color:red")
            self.inputUsernameLineEdit.setText("no username")
        else:
            self.client_obj = Client(username)
            print(self.client_obj.get_host())
            print("ok")

    def send_message_button_clicked(self):
        # TODO : Rework
        self.textBrowser.setText(str(self.client_obj.get_messages_data()))

    @staticmethod
    def is_username_empty(username):
        return username == "" or username == "no username"

    def button_exit_clicked(self):
        if self.client_obj:
            self.client_obj.close_client()
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Ui_MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()

