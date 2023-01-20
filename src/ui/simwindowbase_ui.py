# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'simwindowbase.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(971, 651)
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 951, 631))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.control_space = QHBoxLayout()
        self.control_space.setObjectName(u"control_space")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.listWidget = QListWidget(self.verticalLayoutWidget)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.listWidget)

        self.stateVectorLabel = QLabel(self.verticalLayoutWidget)
        self.stateVectorLabel.setObjectName(u"stateVectorLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stateVectorLabel.sizePolicy().hasHeightForWidth())
        self.stateVectorLabel.setSizePolicy(sizePolicy1)
        self.stateVectorLabel.setFrameShape(QFrame.Box)

        self.verticalLayout_3.addWidget(self.stateVectorLabel)


        self.control_space.addLayout(self.verticalLayout_3)

        self.buttonsAndSetupLayout = QVBoxLayout()
        self.buttonsAndSetupLayout.setObjectName(u"buttonsAndSetupLayout")
        self.setup_button = QPushButton(self.verticalLayoutWidget)
        self.setup_button.setObjectName(u"setup_button")

        self.buttonsAndSetupLayout.addWidget(self.setup_button)

        self.step_button = QPushButton(self.verticalLayoutWidget)
        self.step_button.setObjectName(u"step_button")
        self.step_button.setEnabled(False)

        self.buttonsAndSetupLayout.addWidget(self.step_button)

        self.exit_button = QPushButton(self.verticalLayoutWidget)
        self.exit_button.setObjectName(u"exit_button")

        self.buttonsAndSetupLayout.addWidget(self.exit_button)


        self.control_space.addLayout(self.buttonsAndSetupLayout)


        self.verticalLayout.addLayout(self.control_space)

        self.bloch_space = QHBoxLayout()
        self.bloch_space.setObjectName(u"bloch_space")

        self.verticalLayout.addLayout(self.bloch_space)


        self.retranslateUi(Form)
        self.exit_button.released.connect(Form.close)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Symulacja", None))
        self.stateVectorLabel.setText("")
        self.setup_button.setText(QCoreApplication.translate("Form", u"Utw\u00f3rz symulator (na podstawie konfiguracji poni\u017cej)", None))
        self.step_button.setText(QCoreApplication.translate("Form", u"Nast\u0119pny krok", None))
        self.exit_button.setText(QCoreApplication.translate("Form", u"Zako\u0144cz i wyjd\u017a", None))
    # retranslateUi

