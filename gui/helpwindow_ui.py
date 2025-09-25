# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'helpwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
    QPushButton, QSizePolicy, QSpacerItem, QTextBrowser,
    QVBoxLayout, QWidget)
import resource_rc

class Ui_HelpWindow(object):
    def setupUi(self, HelpWindow):
        if not HelpWindow.objectName():
            HelpWindow.setObjectName(u"HelpWindow")
        HelpWindow.resize(600, 400)
        HelpWindow.setMinimumSize(QSize(600, 400))
        HelpWindow.setMaximumSize(QSize(800, 600))
        icon = QIcon()
        icon.addFile(u":/img/img/favicon.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        HelpWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(HelpWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lblHelp = QLabel(self.centralwidget)
        self.lblHelp.setObjectName(u"lblHelp")
        font = QFont()
        font.setFamilies([u"Arial Black"])
        font.setPointSize(24)
        font.setBold(True)
        self.lblHelp.setFont(font)
        self.lblHelp.setTextFormat(Qt.AutoText)
        self.lblHelp.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lblHelp)

        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.verticalLayout.addWidget(self.textBrowser)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(144, 31))
        self.pushButton.setMaximumSize(QSize(16777215, 31))
        font1 = QFont()
        font1.setBold(True)
        self.pushButton.setFont(font1)

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        HelpWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(HelpWindow)

        QMetaObject.connectSlotsByName(HelpWindow)
    # setupUi

    def retranslateUi(self, HelpWindow):
        HelpWindow.setWindowTitle(QCoreApplication.translate("HelpWindow", u"MainWindow", None))
        HelpWindow.setStyleSheet(QCoreApplication.translate("HelpWindow", u"QWidget#HelpWindow {\n"
"  background: qlineargradient(x1:0, y1:0, x2:1, y2:1, \n"
"        stop:0 #0f0f23, \n"
"        stop:0.3 #1a1a2e, \n"
"        stop:0.6 #16213e, \n"
"        stop:1 #0f3460);\n"
"    border-radius: 5px;\n"
"    border: 1px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, \n"
"        stop:0 #00d4ff, \n"
"        stop:0.5 #0099cc, \n"
"        stop:1 #0066ff);\n"
"}\n"
"\n"
"QWidget#centralwidget {\n"
"    background: transparent;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: white;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"QLabel#lblHelp {\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 24px;\n"
"    text-shadow: 0px 0px 10px rgba(0, 212, 255, 0.5);\n"
"}\n"
"\n"
"QTextBrowser {\n"
"    background: rgba(255, 255, 255, 90);\n"
"    border: 1px solid rgba(255, 255, 255, 50);\n"
"    border-radius: 5px;\n"
"    color: #333;\n"
"    font-size: 12px;\n"
"    padding: 8px;\n"
"    selection-background-color: rgba(0, 212, 255, 100);\n"
"}\n"
"\n"
"QTextBrow"
                        "ser:focus {\n"
"    border: 1px solid rgba(255, 255, 255, 150);\n"
"    background: rgba(255, 255, 255, 95);\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    background: rgba(255, 255, 255, 30);\n"
"    width: 12px;\n"
"    border-radius: 5px;\n"
"    border: 1px solid rgba(255, 255, 255, 50);\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4facfe, stop:1 #00f2fe);\n"
"    border-radius: 5px;\n"
"    min-height: 20px;\n"
"    border: 1px solid rgba(79, 172, 254, 150);\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5fbdff, stop:1 #10f3ff);\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    border: none;\n"
"    background: none;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 80), stop:1 rgba(255, 255, 255, 60));\n"
"    border: 1px solid rgba(255, 255, 255, 100);\n"
"    border-"
                        "radius: 5px;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 12px;\n"
"    padding: 8px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 100), stop:1 rgba(255, 255, 255, 80));\n"
"    border: 1px solid rgba(255, 255, 255, 150);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 60), stop:1 rgba(255, 255, 255, 40));\n"
"}\n"
"\n"
"QPushButton#pushButton {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, \n"
"        stop:0 rgba(0, 212, 255, 120), \n"
"        stop:1 rgba(0, 102, 255, 100));\n"
"    border: 1px solid rgba(0, 212, 255, 150);\n"
"    color: #ffffff;\n"
"    text-shadow: 0px 0px 8px rgba(0, 212, 255, 0.5);\n"
"    box-shadow: 0px 0px 15px rgba(0, 212, 255, 0.3);\n"
"    border-radius: 5px;\n"
"    font-size: 12px;\n"
"    min-width: 80px;\n"
"}\n"
"\n"
"QPushButton#pushButton:hover {\n"
"    background: qlineargradient(x1:0"
                        ", y1:0, x2:0, y2:1, \n"
"        stop:0 rgba(0, 212, 255, 150), \n"
"        stop:1 rgba(0, 102, 255, 130));\n"
"    border: 1px solid rgba(0, 212, 255, 200);\n"
"    box-shadow: 0px 0px 20px rgba(0, 212, 255, 0.5);\n"
"    text-shadow: 0px 0px 10px rgba(0, 212, 255, 0.7);\n"
"}\n"
"\n"
"QPushButton#pushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, \n"
"        stop:0 rgba(0, 212, 255, 80), \n"
"        stop:1 rgba(0, 102, 255, 60));\n"
"    border: 1px solid rgba(0, 212, 255, 100);\n"
"    box-shadow: 0px 0px 10px rgba(0, 212, 255, 0.2);\n"
"}", None))
        self.lblHelp.setText(QCoreApplication.translate("HelpWindow", u"\u6a21\u578b\u4f7f\u7528\u5e2e\u52a9", None))
        self.pushButton.setText(QCoreApplication.translate("HelpWindow", u"\u5173\u95ed", None))
    # retranslateUi

