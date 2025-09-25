#-------------------------------------------------
#
# Project created by QtCreator 2025-07-09T16:55:48
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = qt
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    splashscreen.cpp \
    auth.cpp \
    helpwindow.cpp \
    helpmodelwindow.cpp

HEADERS  += mainwindow.h \
    splashscreen.h \
    auth.h \
    helpwindow.h \
    helpmodelwindow.h

FORMS    += mainwindow.ui \
    splashscreen.ui \
    auth.ui \
    helpwindow.ui \
    helpmodelwindow.ui

RESOURCES += \
    resource.qrc
