#ifndef HELPMODELWINDOW_H
#define HELPMODELWINDOW_H

#include <QMainWindow>

namespace Ui {
class HelpModelWindow;
}

class HelpModelWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit HelpModelWindow(QWidget *parent = 0);
    ~HelpModelWindow();

private:
    Ui::HelpModelWindow *ui;
};

#endif // HELPMODELWINDOW_H
