#ifndef DIALOG_H
#define DIALOG_H

#include <QDialog>
#include <QProcess>
#include <QStandardItemModel>
#include <QTimer>

namespace Ui {
class Dialog;
}

class Dialog : public QDialog
{
    Q_OBJECT

public:
    explicit Dialog(QWidget *parent = nullptr);
    ~Dialog();

private slots:
    void on_btn_start_clicked();
    void on_comboBox_currentIndexChanged(int index);
    void showTime();
    void on_pushButton_clicked();

private:
    void InitTable();
    void GetData();
    void WriteCfg();
    void StartProcess();
    void StopProcess();
    void KillTask();
    void ListViewAdd(QString str);
    bool CheckAppRunningStatus(const QString &appName);
    bool FindAllWindow();
private:
    QStandardItemModel *list_model_;
    QTimer *timer_;
    QProcess *proc_;
    int cur_row_ = -1;
    bool is_run_;
    Ui::Dialog *ui;
};

#endif // DIALOG_H
