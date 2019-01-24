# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\luspock\Documents\Projects\PyDrivers\SweepMeasureSystem\tools\..\SMS.ui',
# licensing of 'C:\Users\luspock\Documents\Projects\PyDrivers\SweepMeasureSystem\tools\..\SMS.ui' applies.
#
# Created: Thu Jan 17 11:51:36 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(937, 648)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setObjectName("tabWidget")
        self.tabSerial = QtWidgets.QWidget()
        self.tabSerial.setObjectName("tabSerial")
        self.tabWidget.addTab(self.tabSerial, "")
        self.tabPlot = QtWidgets.QWidget()
        self.tabPlot.setObjectName("tabPlot")
        self.tabWidget.addTab(self.tabPlot, "")
        self.tabOpenGL = QtWidgets.QWidget()
        self.tabOpenGL.setObjectName("tabOpenGL")
        self.tabWidget.addTab(self.tabOpenGL, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 937, 31))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSerial), QtWidgets.QApplication.translate("MainWindow", "Serial", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPlot), QtWidgets.QApplication.translate("MainWindow", "Plot", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabOpenGL), QtWidgets.QApplication.translate("MainWindow", "OpenGL", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.menuEdit.setTitle(QtWidgets.QApplication.translate("MainWindow", "Edit", None, -1))
        self.menuHelp.setTitle(QtWidgets.QApplication.translate("MainWindow", "Help", None, -1))
        self.actionNew.setText(QtWidgets.QApplication.translate("MainWindow", "New", None, -1))
        self.actionOpen.setText(QtWidgets.QApplication.translate("MainWindow", "Open", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

