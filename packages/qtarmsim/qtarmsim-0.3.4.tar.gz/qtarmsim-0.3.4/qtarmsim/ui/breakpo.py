# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './qtarmsim/ui/breakpo.ui'
#
# Created: Sat Mar  5 19:21:11 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Break(object):
    def setupUi(self, Break):
        Break.setObjectName("Break")
        Break.resize(400, 300)

        self.retranslateUi(Break)
        QtCore.QMetaObject.connectSlotsByName(Break)

    def retranslateUi(self, Break):
        Break.setWindowTitle(QtGui.QApplication.translate("Break", "Puntos de ruptura", None, QtGui.QApplication.UnicodeUTF8))

