# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'teleportationsetup_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QRadioButton,
    QSizePolicy, QSlider, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 200)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.xGateRadio = QRadioButton(Form)
        self.xGateRadio.setObjectName(u"xGateRadio")
        self.xGateRadio.setChecked(True)

        self.horizontalLayout.addWidget(self.xGateRadio)

        self.zGateRadio = QRadioButton(Form)
        self.zGateRadio.setObjectName(u"zGateRadio")

        self.horizontalLayout.addWidget(self.zGateRadio)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.phaseSlider = QSlider(Form)
        self.phaseSlider.setObjectName(u"phaseSlider")
        self.phaseSlider.setMaximum(100)
        self.phaseSlider.setSingleStep(1)
        self.phaseSlider.setOrientation(Qt.Horizontal)
        self.phaseSlider.setTickPosition(QSlider.NoTicks)

        self.verticalLayout.addWidget(self.phaseSlider)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.label)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.xGateRadio.setText(QCoreApplication.translate("Form", u"X", None))
        self.zGateRadio.setText(QCoreApplication.translate("Form", u"T", None))
        self.label.setText(QCoreApplication.translate("Form", u"Faza bramki:", None))
    # retranslateUi

