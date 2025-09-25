#include "mainwindow.h"
#include "splashscreen.h"
#include "helpmodelwindow.h"
#include "helpwindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

//   SplashScreen sp;
//   sp.show();

//HelpModelWindow hmw;
//hmw.show();
    return a.exec();
}
