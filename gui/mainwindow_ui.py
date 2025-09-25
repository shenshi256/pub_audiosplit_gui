# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QProgressBar,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QTextEdit, QVBoxLayout, QWidget)
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 400)
        MainWindow.setMinimumSize(QSize(600, 400))
        MainWindow.setMaximumSize(QSize(800, 600))
        icon = QIcon()
        icon.addFile(u":/img/img/favicon.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.le_select_inputfile = QLineEdit(self.centralWidget)
        self.le_select_inputfile.setObjectName(u"le_select_inputfile")
        self.le_select_inputfile.setMinimumSize(QSize(0, 30))
        self.le_select_inputfile.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_3.addWidget(self.le_select_inputfile)

        self.horizontalSpacer_3 = QSpacerItem(8, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.btn_select_file = QPushButton(self.centralWidget)
        self.btn_select_file.setObjectName(u"btn_select_file")
        self.btn_select_file.setMinimumSize(QSize(110, 30))
        self.btn_select_file.setMaximumSize(QSize(110, 30))

        self.horizontalLayout_3.addWidget(self.btn_select_file)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.le_select_outputfile = QLineEdit(self.centralWidget)
        self.le_select_outputfile.setObjectName(u"le_select_outputfile")
        self.le_select_outputfile.setMinimumSize(QSize(0, 30))
        self.le_select_outputfile.setSizeIncrement(QSize(0, 30))

        self.horizontalLayout_4.addWidget(self.le_select_outputfile)

        self.horizontalSpacer_2 = QSpacerItem(8, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.btn_save = QPushButton(self.centralWidget)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setMinimumSize(QSize(110, 30))
        self.btn_save.setMaximumSize(QSize(110, 30))
        self.btn_save.setSizeIncrement(QSize(0, 30))

        self.horizontalLayout_4.addWidget(self.btn_save)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.groupBox = QGroupBox(self.centralWidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.rbtn_htdemucs = QRadioButton(self.groupBox)
        self.rbtn_htdemucs.setObjectName(u"rbtn_htdemucs")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.rbtn_htdemucs.sizePolicy().hasHeightForWidth())
        self.rbtn_htdemucs.setSizePolicy(sizePolicy1)
        self.rbtn_htdemucs.setChecked(True)

        self.horizontalLayout.addWidget(self.rbtn_htdemucs)

        self.rbtn_mdx_extra = QRadioButton(self.groupBox)
        self.rbtn_mdx_extra.setObjectName(u"rbtn_mdx_extra")
        sizePolicy1.setHeightForWidth(self.rbtn_mdx_extra.sizePolicy().hasHeightForWidth())
        self.rbtn_mdx_extra.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.rbtn_mdx_extra)

        self.rbtn_htdemucs_ft = QRadioButton(self.groupBox)
        self.rbtn_htdemucs_ft.setObjectName(u"rbtn_htdemucs_ft")
        sizePolicy1.setHeightForWidth(self.rbtn_htdemucs_ft.sizePolicy().hasHeightForWidth())
        self.rbtn_htdemucs_ft.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.rbtn_htdemucs_ft)


        self.horizontalLayout_5.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(self.centralWidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy2)
        self.groupBox_3.setMinimumSize(QSize(170, 0))
        self.groupBox_3.setMaximumSize(QSize(170, 16777215))
        self.groupBox_3.setSizeIncrement(QSize(130, 0))
        self.horizontalLayout_31 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_31.setSpacing(6)
        self.horizontalLayout_31.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setContentsMargins(5, 0, 0, 0)
        self.memoryRate = QLabel(self.groupBox_3)
        self.memoryRate.setObjectName(u"memoryRate")
        sizePolicy.setHeightForWidth(self.memoryRate.sizePolicy().hasHeightForWidth())
        self.memoryRate.setSizePolicy(sizePolicy)
        self.memoryRate.setMinimumSize(QSize(0, 35))
        self.memoryRate.setMaximumSize(QSize(16777215, 35))
        self.memoryRate.setSizeIncrement(QSize(0, 0))
        self.memoryRate.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_31.addWidget(self.memoryRate)


        self.horizontalLayout_5.addWidget(self.groupBox_3)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(6)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.groupBox_2 = QGroupBox(self.centralWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy3)
        self.groupBox_2.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.chk_vocals = QCheckBox(self.groupBox_2)
        self.chk_vocals.setObjectName(u"chk_vocals")
        self.chk_vocals.setChecked(True)

        self.horizontalLayout_6.addWidget(self.chk_vocals)

        self.chk_other = QCheckBox(self.groupBox_2)
        self.chk_other.setObjectName(u"chk_other")

        self.horizontalLayout_6.addWidget(self.chk_other)

        self.chk_drums = QCheckBox(self.groupBox_2)
        self.chk_drums.setObjectName(u"chk_drums")

        self.horizontalLayout_6.addWidget(self.chk_drums)

        self.chk_bass = QCheckBox(self.groupBox_2)
        self.chk_bass.setObjectName(u"chk_bass")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.chk_bass.sizePolicy().hasHeightForWidth())
        self.chk_bass.setSizePolicy(sizePolicy4)

        self.horizontalLayout_6.addWidget(self.chk_bass)


        self.horizontalLayout_8.addWidget(self.groupBox_2)

        self.groupBox_4 = QGroupBox(self.centralWidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy2.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy2)
        self.groupBox_4.setMinimumSize(QSize(170, 0))
        self.groupBox_4.setMaximumSize(QSize(170, 16777215))
        self.groupBox_4.setSizeIncrement(QSize(130, 0))
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(10, 0, 0, 0)
        self.rbtn_wav = QRadioButton(self.groupBox_4)
        self.rbtn_wav.setObjectName(u"rbtn_wav")
        sizePolicy4.setHeightForWidth(self.rbtn_wav.sizePolicy().hasHeightForWidth())
        self.rbtn_wav.setSizePolicy(sizePolicy4)
        self.rbtn_wav.setChecked(True)

        self.horizontalLayout_7.addWidget(self.rbtn_wav)

        self.rbtn_mp3 = QRadioButton(self.groupBox_4)
        self.rbtn_mp3.setObjectName(u"rbtn_mp3")
        sizePolicy4.setHeightForWidth(self.rbtn_mp3.sizePolicy().hasHeightForWidth())
        self.rbtn_mp3.setSizePolicy(sizePolicy4)
        self.rbtn_mp3.setToolTipDuration(-1)

        self.horizontalLayout_7.addWidget(self.rbtn_mp3)


        self.horizontalLayout_8.addWidget(self.groupBox_4)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.chk_debug = QCheckBox(self.centralWidget)
        self.chk_debug.setObjectName(u"chk_debug")
        sizePolicy4.setHeightForWidth(self.chk_debug.sizePolicy().hasHeightForWidth())
        self.chk_debug.setSizePolicy(sizePolicy4)

        self.horizontalLayout_2.addWidget(self.chk_debug)

        self.horizontalSpacer_5 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.btn_help = QPushButton(self.centralWidget)
        self.btn_help.setObjectName(u"btn_help")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.btn_help.sizePolicy().hasHeightForWidth())
        self.btn_help.setSizePolicy(sizePolicy5)
        self.btn_help.setMinimumSize(QSize(80, 30))
        self.btn_help.setMaximumSize(QSize(80, 30))
        self.btn_help.setSizeIncrement(QSize(0, 30))

        self.horizontalLayout_2.addWidget(self.btn_help)

        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btn_model_desc = QPushButton(self.centralWidget)
        self.btn_model_desc.setObjectName(u"btn_model_desc")
        sizePolicy5.setHeightForWidth(self.btn_model_desc.sizePolicy().hasHeightForWidth())
        self.btn_model_desc.setSizePolicy(sizePolicy5)
        self.btn_model_desc.setMinimumSize(QSize(80, 30))
        self.btn_model_desc.setMaximumSize(QSize(80, 30))
        self.btn_model_desc.setSizeIncrement(QSize(0, 30))

        self.horizontalLayout_2.addWidget(self.btn_model_desc)

        self.horizontalSpacer_4 = QSpacerItem(13, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.btn_start = QPushButton(self.centralWidget)
        self.btn_start.setObjectName(u"btn_start")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.btn_start.sizePolicy().hasHeightForWidth())
        self.btn_start.setSizePolicy(sizePolicy6)
        self.btn_start.setMinimumSize(QSize(110, 30))
        self.btn_start.setSizeIncrement(QSize(0, 30))

        self.horizontalLayout_2.addWidget(self.btn_start)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.progressBar = QProgressBar(self.centralWidget)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy6.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy6)
        self.progressBar.setMinimumSize(QSize(0, 10))
        self.progressBar.setMaximumSize(QSize(16777215, 10))
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)

        self.te_msg = QTextEdit(self.centralWidget)
        self.te_msg.setObjectName(u"te_msg")
        self.te_msg.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.verticalLayout.addWidget(self.te_msg)

        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        MainWindow.setStyleSheet(QCoreApplication.translate("MainWindow", u"QWidget#MainWindow {\n"
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
"QWidget#centralWidget {\n"
"    background: transparent;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: white;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background: rgba(255, 255, 255, 90);\n"
"    border: 1px solid rgba(255, 255, 255, 50);\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"    color: #333;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid rgba(255, 255, 255, 150);\n"
"    background: rgba(255, 255, 255, 95);\n"
"}\n"
"\n"
"\n"
"\n"
"QLineEdit[placeholderText] {\n"
"    color: white; /* \u6c34\u5370\u6587\u5b57\u989c\u8272 */\n"
""
                        "}\n"
"\n"
"QPushButton {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 80), stop:1 rgba(255, 255, 255, 60));\n"
"    border: 1px solid rgba(255, 255, 255, 100);\n"
"    border-radius: 5px;\n"
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
"QPushButton#btn_start {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, \n"
"        stop:0 rgba(0, 212, 255, 120), \n"
"        stop:1 rgba(0, 102, 255, 100));\n"
"    border: 1px solid rgba(0, 212, 255, 150);\n"
"    color: #ffffff;\n"
"    text-shadow: 0px 0px 8px rgba(0, 212, 255, 0.5);\n"
" "
                        "   box-shadow: 0px 0px 15px rgba(0, 212, 255, 0.3);\n"
"    border-radius: 5px;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"QPushButton#btn_start:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, \n"
"        stop:0 rgba(0, 212, 255, 150), \n"
"        stop:1 rgba(0, 102, 255, 130));\n"
"    border: 1px solid rgba(0, 212, 255, 200);\n"
"    box-shadow: 0px 0px 20px rgba(0, 212, 255, 0.5);\n"
"    text-shadow: 0px 0px 10px rgba(0, 212, 255, 0.7);\n"
"}\n"
"\n"
"QPushButton#btn_start:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, \n"
"        stop:0 rgba(0, 212, 255, 80), \n"
"        stop:1 rgba(0, 102, 255, 60));\n"
"    border: 1px solid rgba(0, 212, 255, 100);\n"
"    box-shadow: 0px 0px 10px rgba(0, 212, 255, 0.2);\n"
"}\n"
"\n"
"QGroupBox {\n"
"    color: white;\n"
"    font-size: 12px;\n"
"    font-weight: bold;\n"
"    border: 1px solid rgba(255, 255, 255, 100);\n"
"    border-radius: 5px;\n"
"    margin-top: 10px;\n"
"    padding-top: 10px;\n"
"    background: rgba(2"
                        "55, 255, 255, 10);\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 8px 0 8px;\n"
"    color: white;\n"
"    font-size: 12px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QRadioButton {\n"
"    color: white;\n"
"    spacing: 8px;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    border-radius: 9px;\n"
"    border: 1px solid rgba(255, 255, 255, 100);\n"
"    background: rgba(255, 255, 255, 30);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4facfe, stop:1 #00f2fe);\n"
"    border: 1px solid rgba(79, 172, 254, 150);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #5fbdff, stop:1 #10f3ff);\n"
"}\n"
"\n"
"QCheckBox {\n"
"    color: white;\n"
"    spacing: 8px;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 18px;\n"
"    h"
                        "eight: 18px;\n"
"    border-radius: 3px;\n"
"    border: 1px solid rgba(255, 255, 255, 100);\n"
"    background: rgba(255, 255, 255, 30);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4facfe, stop:1 #00f2fe);\n"
"    border: 1px solid rgba(79, 172, 254, 150);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #5fbdff, stop:1 #10f3ff);\n"
"}\n"
"\n"
"QProgressBar {\n"
"    border: 1px solid rgba(255, 255, 255, 100);\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"    background: rgba(255, 255, 255, 20);\n"
"    color: white;\n"
"    font-size: 10px;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4facfe, stop:1 #00f2fe);\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QTextEdit {\n"
"     background: rgba(255, 255, 255, 90);\n"
"    /*background: white;*/\n"
"    border: 1px solid rgba(255, 255, 255, 50);\n"
"    b"
                        "order-radius: 5px;\n"
"    /*color: #333;*/\n"
"    color:white;\n"
"    font-size: 12px;\n"
"    padding: 8px;\n"
"}\n"
"\n"
"QTextEdit:focus {\n"
"    border: 1px solid rgba(255, 255, 255, 150);\n"
"    background: rgba(255, 255, 255, 95);\n"
"}", None))
        self.le_select_inputfile.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u9009\u62e9\u97f3\u89c6\u9891\u6587\u4ef6", None))
        self.btn_select_file.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None))
        self.le_select_outputfile.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u9009\u62e9\u4fdd\u5b58\u4f4d\u7f6e(\u9ed8\u8ba4\u540c\u540d\u76ee\u5f55\u4e0b)", None))
#if QT_CONFIG(tooltip)
        self.btn_save.setToolTip(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba4\u5c06\u4fdd\u5b58\u5728\u6587\u4ef6\u540c\u540d\u76ee\u5f55\u4e0b", None))
#endif // QT_CONFIG(tooltip)
        self.btn_save.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u4f4d\u7f6e", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8bf7\u9009\u62e9\u6a21\u578b", None))
#if QT_CONFIG(tooltip)
        self.rbtn_htdemucs.setToolTip(QCoreApplication.translate("MainWindow", u"\u6700\u5e38\u7528\u7684\u6a21\u578b, \u901f\u5ea6\u548c\u7cbe\u5ea6\u90fd\u53ef\u4ee5", None))
#endif // QT_CONFIG(tooltip)
        self.rbtn_htdemucs.setText(QCoreApplication.translate("MainWindow", u"htdemucs(\u63a8\u8350)", None))
#if QT_CONFIG(tooltip)
        self.rbtn_mdx_extra.setToolTip(QCoreApplication.translate("MainWindow", u"\u53cc\u89c4\u6a21\u578b, \u4ec5\u4eba\u58f0\u548c\u4f34\u594f", None))
#endif // QT_CONFIG(tooltip)
        self.rbtn_mdx_extra.setText(QCoreApplication.translate("MainWindow", u"mdx_extra(\u53cc\u89c4\u6a21\u578b)", None))
#if QT_CONFIG(tooltip)
        self.rbtn_htdemucs_ft.setToolTip(QCoreApplication.translate("MainWindow", u"\u9ad8\u7cbe\u5ea6\u6a21\u578b, \u5355CPU\u7684\u65f6\u5019\u901f\u5ea6\u8f83\u6162", None))
#endif // QT_CONFIG(tooltip)
        self.rbtn_htdemucs_ft.setText(QCoreApplication.translate("MainWindow", u"htdemucs_ft(\u9ad8\u7cbe\u5ea6)", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u7cfb\u7edf\u4fe1\u606f", None))
        self.memoryRate.setText(QCoreApplication.translate("MainWindow", u"\u8fdb\u7a0b: \u5185\u5b58 321M,CPU: 0% \n"
"\u7cfb\u7edf: \u5185\u5b58 92%, CPU: 0%", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u8bf7\u9009\u62e9\u8f93\u51fa\u97f3\u8f68", None))
        self.chk_vocals.setText(QCoreApplication.translate("MainWindow", u"vocals(\u4eba\u58f0)", None))
        self.chk_other.setText(QCoreApplication.translate("MainWindow", u"other(\u5176\u4ed6\u58f0\u97f3)", None))
        self.chk_drums.setText(QCoreApplication.translate("MainWindow", u"drums(\u9f13)", None))
        self.chk_bass.setText(QCoreApplication.translate("MainWindow", u"bass(\u8d1d\u65af)", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u5176\u4ed6\u8bbe\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.rbtn_wav.setToolTip(QCoreApplication.translate("MainWindow", u"\u65e0\u635f\u97f3\u9891\uff0c\u4f53\u79ef\u5927\uff0c\u97f3\u8d28\u6700\u597d, \u9002\u5408\u8f6c\u5f55\u4e0e\u526a\u8f91", None))
#endif // QT_CONFIG(tooltip)
        self.rbtn_wav.setText(QCoreApplication.translate("MainWindow", u"wav(\u63a8\u8350)", None))
#if QT_CONFIG(tooltip)
        self.rbtn_mp3.setToolTip(QCoreApplication.translate("MainWindow", u"\u538b\u7f29\u97f3\u9891\uff0c\u4f53\u79ef\u5c0f\uff0c\u97f3\u8d28\u7565\u635f, \u9002\u5408\u666e\u901a\u542c\u97f3\u6216\u5206\u4eab", None))
#endif // QT_CONFIG(tooltip)
        self.rbtn_mp3.setText(QCoreApplication.translate("MainWindow", u"mp3", None))
        self.chk_debug.setText(QCoreApplication.translate("MainWindow", u"\u8c03\u8bd5\u6a21\u5f0f", None))
#if QT_CONFIG(tooltip)
        self.btn_help.setToolTip(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba4\u5c06\u4fdd\u5b58\u5728\u6587\u4ef6\u540c\u540d\u76ee\u5f55\u4e0b", None))
#endif // QT_CONFIG(tooltip)
        self.btn_help.setText(QCoreApplication.translate("MainWindow", u"\u4f7f\u7528\u5e2e\u52a9", None))
#if QT_CONFIG(tooltip)
        self.btn_model_desc.setToolTip(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba4\u5c06\u4fdd\u5b58\u5728\u6587\u4ef6\u540c\u540d\u76ee\u5f55\u4e0b", None))
#endif // QT_CONFIG(tooltip)
        self.btn_model_desc.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u4ecb\u7ecd", None))
#if QT_CONFIG(tooltip)
        self.btn_start.setToolTip(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba4\u5c06\u4fdd\u5b58\u5728\u6587\u4ef6\u540c\u540d\u76ee\u5f55\u4e0b", None))
#endif // QT_CONFIG(tooltip)
        self.btn_start.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5904\u7406", None))
    # retranslateUi

