#include "helpmodelwindow.h"
#include "ui_helpmodelwindow.h"

HelpModelWindow::HelpModelWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::HelpModelWindow)
{
    ui->setupUi(this);
}

HelpModelWindow::~HelpModelWindow()
{
    delete ui;
}
