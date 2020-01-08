#include "dialog.h"
#include "server.h"
#include <QApplication>
#include <QDesktopWidget>

int main(int argc, char *argv[])
{
    QCoreApplication::addLibraryPath("./plugins");
    QApplication a(argc, argv);

    Dialog w;
    w.show();

    return a.exec();
}
