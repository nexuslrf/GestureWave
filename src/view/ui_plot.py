# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_plot.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_win_plot(object):
    def setupUi(self, win_plot):
        win_plot.setObjectName("win_plot")
        win_plot.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(win_plot)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.qwtPlot = QwtPlot(self.centralwidget)
        self.qwtPlot.setEnabled(False)
        self.qwtPlot.setObjectName("qwtPlot")
        self.verticalLayout.addWidget(self.qwtPlot)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(6, 0, 6, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_gesture_0 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gesture_0.setEnabled(True)
        self.btn_gesture_0.setCheckable(False)
        self.btn_gesture_0.setAutoRepeat(False)
        self.btn_gesture_0.setObjectName("btn_gesture_0")
        self.horizontalLayout.addWidget(self.btn_gesture_0)
        self.btn_gesture_1 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gesture_1.setObjectName("btn_gesture_1")
        self.horizontalLayout.addWidget(self.btn_gesture_1)
        self.btn_gesture_2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gesture_2.setObjectName("btn_gesture_2")
        self.horizontalLayout.addWidget(self.btn_gesture_2)
        self.btn_gesture_3 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gesture_3.setObjectName("btn_gesture_3")
        self.horizontalLayout.addWidget(self.btn_gesture_3)
        self.btn_gesture_4 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gesture_4.setObjectName("btn_gesture_4")
        self.horizontalLayout.addWidget(self.btn_gesture_4)
        self.btn_gesture_5 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gesture_5.setObjectName("btn_gesture_5")
        self.horizontalLayout.addWidget(self.btn_gesture_5)
        self.btn_gesture_6 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gesture_6.setObjectName("btn_gesture_6")
        self.horizontalLayout.addWidget(self.btn_gesture_6)
        self.btn_gesture_7 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gesture_7.setObjectName("btn_gesture_7")
        self.horizontalLayout.addWidget(self.btn_gesture_7)
        self.verticalLayout.addLayout(self.horizontalLayout)
        win_plot.setCentralWidget(self.centralwidget)

        self.retranslateUi(win_plot)
        QtCore.QMetaObject.connectSlotsByName(win_plot)

    def retranslateUi(self, win_plot):
        _translate = QtCore.QCoreApplication.translate
        win_plot.setWindowTitle(_translate("win_plot", "Soundwave gestures using Doppler Effect"))
        self.btn_gesture_0.setToolTip(_translate("win_plot", "Right-To-Left-One-Hand"))
        self.btn_gesture_0.setText(_translate("win_plot", "Record 0"))
        self.btn_gesture_1.setToolTip(_translate("win_plot", "Top-to-Bottom-One-Hand"))
        self.btn_gesture_1.setText(_translate("win_plot", "Record 1"))
        self.btn_gesture_2.setToolTip(_translate("win_plot", "Entgegengesetzt with two hands"))
        self.btn_gesture_2.setText(_translate("win_plot", "Record 2"))
        self.btn_gesture_3.setToolTip(_translate("win_plot", "Single-push with one hand"))
        self.btn_gesture_3.setText(_translate("win_plot", "Record 3"))
        self.btn_gesture_4.setToolTip(_translate("win_plot", "Double-push with one hand"))
        self.btn_gesture_4.setText(_translate("win_plot", "Record 4"))
        self.btn_gesture_5.setToolTip(_translate("win_plot", "Rotate one hand"))
        self.btn_gesture_5.setText(_translate("win_plot", "Record 5"))
        self.btn_gesture_6.setToolTip(_translate("win_plot", "Background noise (no gesture, but in silent room)"))
        self.btn_gesture_6.setText(_translate("win_plot", "Record 6"))
        self.btn_gesture_7.setToolTip(_translate("win_plot", "No gesture with background sound (in a Pub, at office, in the kitchen, etc.)"))
        self.btn_gesture_7.setText(_translate("win_plot", "Record 7"))

from qwt import QwtPlot
