from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        app = QApplication.instance()
        screen_geometry = app.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(int(screen_width * 0.4), int(screen_height * 0.5))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, int(screen_width * 0.1), int(screen_height * 0.05)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, int(screen_height * 0.05), int(screen_width * 0.1), int(screen_height * 0.05)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(0, int(screen_height * 0.11), int(screen_width * 0.5), int(screen_height * 0.3)))
        self.textEdit.setObjectName("textEdit")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(int(screen_width * 0.11), int(screen_height * 0.013), int(screen_width * 0.04), int(screen_height * 0.025)))
        self.spinBox.setObjectName("spinBox")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(int(screen_width * 0.15), int(screen_height * 0.42), int(screen_width * 0.1), int(screen_height * 0.05)))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        # self.menubar.setObjectName("menubar")
        # MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Выберите оценку:"))
        self.label_2.setText(_translate("MainWindow", "Введите отзыв:"))
        self.pushButton.setText(_translate("MainWindow", "Сохранить"))
