# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui\detailsPanel.ui'
#
# Created: Mon Mar 23 22:58:30 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DetailsPanel(object):
    def setupUi(self, DetailsPanel):
        DetailsPanel.setObjectName("DetailsPanel")
        DetailsPanel.resize(350, 600)
        DetailsPanel.setMinimumSize(QtCore.QSize(350, 600))
        DetailsPanel.setMaximumSize(QtCore.QSize(350, 600))
        DetailsPanel.setStyleSheet("#details_panel_widget \n"
"{\n"
"    background-image: url(:/assets/panels/details/details_panel_overlay.png);\n"
"}")
        self.boss_name_label = QtGui.QLabel(DetailsPanel)
        self.boss_name_label.setGeometry(QtCore.QRect(0, 29, 350, 51))
        self.boss_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.boss_name_label.setObjectName("boss_name_label")
        self.level_name_label = QtGui.QLabel(DetailsPanel)
        self.level_name_label.setGeometry(QtCore.QRect(146, 73, 46, 16))
        self.level_name_label.setObjectName("level_name_label")
        self.level_label = QtGui.QLabel(DetailsPanel)
        self.level_label.setGeometry(QtCore.QRect(182, 74, 21, 16))
        self.level_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.level_label.setObjectName("level_label")
        self.loot_widget = QtGui.QWidget(DetailsPanel)
        self.loot_widget.setGeometry(QtCore.QRect(75, 460, 200, 120))
        self.loot_widget.setObjectName("loot_widget")
        self.loot_name_label = QtGui.QLabel(self.loot_widget)
        self.loot_name_label.setGeometry(QtCore.QRect(0, 5, 200, 26))
        self.loot_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.loot_name_label.setObjectName("loot_name_label")
        self.loot_items_widget = QtGui.QWidget(self.loot_widget)
        self.loot_items_widget.setGeometry(QtCore.QRect(-1, 29, 201, 91))
        self.loot_items_widget.setObjectName("loot_items_widget")
        self.horizontalLayoutWidget = QtGui.QWidget(self.loot_items_widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 201, 91))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.loot_items_layout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.loot_items_layout.setSpacing(16)
        self.loot_items_layout.setContentsMargins(0, 0, 0, 0)
        self.loot_items_layout.setObjectName("loot_items_layout")
        self.close_button = QtGui.QPushButton(DetailsPanel)
        self.close_button.setGeometry(QtCore.QRect(325, 7, 16, 16))
        self.close_button.setText("")
        self.close_button.setObjectName("close_button")
        self.waypoint_label = QtGui.QLabel(DetailsPanel)
        self.waypoint_label.setGeometry(QtCore.QRect(115, 280, 120, 21))
        self.waypoint_label.setAlignment(QtCore.Qt.AlignCenter)
        self.waypoint_label.setObjectName("waypoint_label")
        self.waypoint_name_label = QtGui.QLabel(DetailsPanel)
        self.waypoint_name_label.setGeometry(QtCore.QRect(30, 310, 141, 21))
        self.waypoint_name_label.setText("")
        self.waypoint_name_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.waypoint_name_label.setObjectName("waypoint_name_label")
        self.waypoint_link_label = QtGui.QLabel(DetailsPanel)
        self.waypoint_link_label.setGeometry(QtCore.QRect(175, 310, 81, 20))
        self.waypoint_link_label.setText("")
        self.waypoint_link_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.waypoint_link_label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.waypoint_link_label.setObjectName("waypoint_link_label")
        self.waypoint_copy_button = QtGui.QPushButton(DetailsPanel)
        self.waypoint_copy_button.setGeometry(QtCore.QRect(260, 312, 18, 18))
        self.waypoint_copy_button.setText("")
        self.waypoint_copy_button.setObjectName("waypoint_copy_button")

        self.retranslateUi(DetailsPanel)
        QtCore.QObject.connect(self.close_button, QtCore.SIGNAL("released()"), DetailsPanel.hide)
        QtCore.QMetaObject.connectSlotsByName(DetailsPanel)

    def retranslateUi(self, DetailsPanel):
        DetailsPanel.setWindowTitle(QtGui.QApplication.translate("DetailsPanel", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.boss_name_label.setText(QtGui.QApplication.translate("DetailsPanel", "Boss Name", None, QtGui.QApplication.UnicodeUTF8))
        self.level_name_label.setText(QtGui.QApplication.translate("DetailsPanel", "Level:", None, QtGui.QApplication.UnicodeUTF8))
        self.level_label.setText(QtGui.QApplication.translate("DetailsPanel", "#", None, QtGui.QApplication.UnicodeUTF8))
        self.loot_name_label.setText(QtGui.QApplication.translate("DetailsPanel", "Loot", None, QtGui.QApplication.UnicodeUTF8))
        self.waypoint_label.setText(QtGui.QApplication.translate("DetailsPanel", "Waypoint", None, QtGui.QApplication.UnicodeUTF8))

import assets_rc
