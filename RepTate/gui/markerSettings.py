# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/markerSettings.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_markerSettings(object):
    def setupUi(self, markerSettings):
        markerSettings.setObjectName("markerSettings")
        markerSettings.resize(312, 191)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/Images/new_icons/icons8-star-filled_setting.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        markerSettings.setWindowIcon(icon)
        self.verticalLayoutWidget = QtWidgets.QWidget(markerSettings)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 291, 171))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.labelPickedColor = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.labelPickedColor.setText("")
        self.labelPickedColor.setObjectName("labelPickedColor")
        self.horizontalLayout_2.addWidget(self.labelPickedColor)
        self.pickColor = QtWidgets.QToolButton(self.verticalLayoutWidget)
        self.pickColor.setObjectName("pickColor")
        self.horizontalLayout_2.addWidget(self.pickColor)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 2, 1, 1, 1)
        self.checkBoxFilled = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxFilled.setText("")
        self.checkBoxFilled.setCheckable(True)
        self.checkBoxFilled.setChecked(False)
        self.checkBoxFilled.setTristate(False)
        self.checkBoxFilled.setObjectName("checkBoxFilled")
        self.gridLayout.addWidget(self.checkBoxFilled, 4, 2, 1, 1)
        self.checkBoxSize = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxSize.setObjectName("checkBoxSize")
        self.gridLayout.addWidget(self.checkBoxSize, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.checkBoxType = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxType.setObjectName("checkBoxType")
        self.gridLayout.addWidget(self.checkBoxType, 2, 2, 1, 1)
        self.checkBoxColor = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxColor.setObjectName("checkBoxColor")
        self.gridLayout.addWidget(self.checkBoxColor, 3, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(40)
        self.spinBox.setProperty("value", 12)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushOK = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushOK.setObjectName("pushOK")
        self.horizontalLayout.addWidget(self.pushOK)
        self.pushCancel = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushCancel.setObjectName("pushCancel")
        self.horizontalLayout.addWidget(self.pushCancel)
        self.pushApply = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushApply.setObjectName("pushApply")
        self.horizontalLayout.addWidget(self.pushApply)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(markerSettings)
        self.pushCancel.clicked.connect(markerSettings.reject)
        self.pushOK.clicked.connect(markerSettings.accept)
        self.checkBoxColor.clicked['bool'].connect(self.pickColor.setDisabled)
        self.checkBoxType.clicked['bool'].connect(self.comboBox.setDisabled)
        self.checkBoxColor.clicked['bool'].connect(self.label_4.setDisabled)
        self.checkBoxSize.clicked['bool'].connect(self.spinBox.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(markerSettings)

    def retranslateUi(self, markerSettings):
        _translate = QtCore.QCoreApplication.translate
        markerSettings.setWindowTitle(_translate("markerSettings", "Adjust Marker Settings"))
        self.label_4.setText(_translate("markerSettings", "Pick Color"))
        self.pickColor.setText(_translate("markerSettings", "..."))
        self.label.setText(_translate("markerSettings", "Size"))
        self.checkBoxSize.setText(_translate("markerSettings", "Use Defaut"))
        self.label_2.setText(_translate("markerSettings", "Type"))
        self.checkBoxType.setText(_translate("markerSettings", "Variable"))
        self.checkBoxColor.setText(_translate("markerSettings", "Variable"))
        self.label_3.setText(_translate("markerSettings", "Color"))
        self.label_5.setText(_translate("markerSettings", "Filled"))
        self.pushOK.setText(_translate("markerSettings", "OK"))
        self.pushCancel.setText(_translate("markerSettings", "Cancel"))
        self.pushApply.setText(_translate("markerSettings", "Apply"))

import MainWindow_rc
import Reptate_rc