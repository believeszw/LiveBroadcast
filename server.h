#ifndef SERVER_H
#define SERVER_H

#include <QDialog>

namespace Ui {
class Server;
}

class Server : public QDialog
{
    Q_OBJECT

public:
    explicit Server(QWidget *parent = nullptr);
    ~Server();

private slots:
    void on_comboBox_currentIndexChanged(int index);

    void on_btn_add_clicked();

    void on_btn_del_clicked();

    void on_btn_update_clicked();

    void on_btn_refresh_clicked();

private:
    void InitTable();
    void GetData();
private:
    Ui::Server *ui;
};

#endif // SERVER_H
