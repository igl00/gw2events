# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui\settings.ui'
#
# Created: Sun Feb 15 21:14:52 2015
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
        self.iipUdate_box.setGeometry(QtCore.QRect(10, 10, 291, 71))
        self.iipUdate_box.setCheckable(True)
        self.iipUdate_box.setObjectName("iipUdate_box")
        self.iipUpdate_spinBox = QtGui.QSpinBox(self.iipUdate_box)
        self.iipUpdate_spinBox.setGeometry(QtCore.QRect(150, 30, 121, 22))
        self.iipUpdate_spinBox.setMinimum(1)
        self.iipUpdate_spinBox.setMaximum(99999)
        self.iipUpdate_spinBox.setProperty("value", 5)
        self.iipUpdate_spinBox.setObjectName("iipUpdate_spinBox")
        self.iipUpdate_label = QtGui.QLabel(self.iipUdate_box)
        self.iipUpdate_label.setGeometry(QtCore.QRect(20, 30, 111, 20))
        self.iipUpdate_label.setObjectName("iipUpdate_label")
        self.textEdit = QtGui.QTextEdit(Settings)
        self.textEdit.setGeometry(QtCore.QRect(20, 90, 271, 51))
        self.textEdit.setFrameShape(QtGui.QFrame.NoFrame)
        self.textEdit.setAcceptRichText(False)
        self.textEdit.setCursorWidth(0)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Settings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Settings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QtGui.QApplication.translate("Settings", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.iipUdate_box.setTitle(QtGui.QApplication.translate("Settings", "Update Instance IP", None, QtGui.QApplication.UnicodeUTF8))
        self.iipUpdate_spinBox.setSuffix(QtGui.QApplication.translate("Settings", "s", None, QtGui.QApplication.UnicodeUTF8))
        self.iipUpdate_label.setText(QtGui.QApplication.translate("Settings", "Update every:", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setHtml(QtGui.QApplication.translate("Settings", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600; color:#8c2626;\">Warning</span><span style=\" font-size:8pt;\">: Finding the instance ip is the most intensive part of this program. Please try disabling it if you are experiencing any issues.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

