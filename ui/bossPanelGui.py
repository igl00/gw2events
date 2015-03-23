# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui\bossPanel.ui'
#
# Created: Mon Mar 23 22:58:29 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_BossPanel(object):
    def setupUi(self, BossPanel):
        BossPanel.setObjectName("BossPanel")
        BossPanel.resize(350, 150)
        BossPanel.setMinimumSize(QtCore.QSize(350, 150))
        BossPanel.setMaximumSize(QtCore.QSize(350, 150))
        self.title_label = QtGui.QLabel(BossPanel)
        self.title_label.setGeometry(QtCore.QRect(5, 116, 140, 28))
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setWordWrap(True)
        self.title_label.setObjectName("title_label")
        self.time_label = QtGui.QLabel(BossPanel)
        self.time_label.setGeometry(QtCore.QRect(270, 9, 75, 16))
        self.time_label.setText("TIME")
        self.time_label.setScaledContents(False)
        self.time_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.time_label.setObjectName("time_label")
        self.active_title_label = QtGui.QLabel(BossPanel)
        self.active_title_label.setGeometry(QtCore.QRect(35, 46, 280, 40))
        self.active_title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.active_title_label.setObjectName("active_title_label")
        self.active_time_label = QtGui.QLabel(BossPanel)
        self.active_time_label.setGeometry(QtCore.QRect(137, 82, 76, 16))
        self.active_time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.active_time_label.setObjectName("active_time_label")

        self.retranslateUi(BossPanel)
        QtCore.QMetaObject.connectSlotsByName(BossPanel)

    def retranslateUi(self, BossPanel):
        BossPanel.setWindowTitle(QtGui.QApplication.translate("BossPanel", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.title_label.setText(QtGui.QApplication.translate("BossPanel", "BOSS NAME", None, QtGui.QApplication.UnicodeUTF8))
        self.active_title_label.setText(QtGui.QApplication.translate("BossPanel", "ACTIVE BOSS NAME", None, QtGui.QApplication.UnicodeUTF8))
        self.active_time_label.setText(QtGui.QApplication.translate("BossPanel", "ACTIVE TIME", None, QtGui.QApplication.UnicodeUTF8))

