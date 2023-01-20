# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(899, 609)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 10, 881, 591))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(20)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.wat_logo = QLabel(self.horizontalLayoutWidget)
        self.wat_logo.setObjectName(u"wat_logo")
        self.wat_logo.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.wat_logo)

        self.description = QLabel(self.horizontalLayoutWidget)
        self.description.setObjectName(u"description")
        font1 = QFont()
        font1.setPointSize(14)
        self.description.setFont(font1)
        self.description.setScaledContents(False)
        self.description.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.description.setWordWrap(True)
        self.description.setMargin(0)

        self.horizontalLayout_2.addWidget(self.description)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.simple_button = QPushButton(self.horizontalLayoutWidget)
        self.simple_button.setObjectName(u"simple_button")

        self.verticalLayout.addWidget(self.simple_button)

        self.deutsch_button = QPushButton(self.horizontalLayoutWidget)
        self.deutsch_button.setObjectName(u"deutsch_button")

        self.verticalLayout.addWidget(self.deutsch_button)

        self.teleportationButton = QPushButton(self.horizontalLayoutWidget)
        self.teleportationButton.setObjectName(u"teleportationButton")

        self.verticalLayout.addWidget(self.teleportationButton)


        self.horizontalLayout.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Symulator kwantowy", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Witaj w symulatorze kwantowym! Wybierz modu\u0142, naciskaj\u0105c przycisk po prawej.", None))
        self.wat_logo.setText("")
        self.description.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Ten program stanowi integraln\u0105 cz\u0119\u015b\u0107 pracy in\u017cynierskiej wykonanej przez Bart\u0142omieja Klimka, studenta wydzia\u0142u Cybernetyki WAT, kierunku Informatyka, pod nadzorem dr Joanny Wi\u015bniewskiej.</p></body></html>", None))
        self.simple_button.setText(QCoreApplication.translate("MainWindow", u"Proste spl\u0105tanie", None))
        self.deutsch_button.setText(QCoreApplication.translate("MainWindow", u"Algorytm Deutscha-Jozsy", None))
        self.teleportationButton.setText(QCoreApplication.translate("MainWindow", u"Kwantowa teleportacja", None))
    # retranslateUi

