# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created: Sun Feb 15 12:45:57 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(312, 230)
        self.buttonBox = QtGui.QDialogButtonBox(Settings)
        self.buttonBox.setGeometry(QtCore.QRect(10, 190, 291, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.iipUdate_box = QtGui.QGroupBox(Settings)
        self.iipUdate_box.setGeometry(QtCore.QRect(10, 10, 291, 80))
        self.iipUdate_box.setCheckable(True)
        self.iipUdate_box.setObjectName("iipUdate_box")
        self.iipUpdate_spinBox = QtGui.QSpinBox(self.iipUdate_box)
        self.iipUpdate_spinBox.setGeometry(QtCore.QRect(150, 30, 131, 22))
        self.iipUpdate_spinBox.setMinimum(1)
        self.iipUpdate_spinBox.setMaximum(99999)
        self.iipUpdate_spinBox.setProperty("value", 5)
        self.iipUpdate_spinBox.setObjectName("iipUpdate_spinBox")
        self.iipUpdate_label = QtGui.QLabel(self.iipUdate_box)
        self.iipUpdate_label.setGeometry(QtCore.QRect(20, 30, 111, 20))
        self.iipUpdate_label.setObjectName("iipUpdate_label")

        self.retranslateUi(Settings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Settings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QtGui.QApplication.translate("Settings", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.iipUdate_box.setTitle(QtGui.QApplication.translate("Settings", "Update Instance IP", None, QtGui.QApplication.UnicodeUTF8))
        self.iipUpdate_spinBox.setSuffix(QtGui.QApplication.translate("Settings", "s", None, QtGui.QApplication.UnicodeUTF8))
        self.iipUpdate_label.setText(QtGui.QApplication.translate("Settings", "Update every:", None, QtGui.QApplication.UnicodeUTF8))

