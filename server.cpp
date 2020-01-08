#include "server.h"
#include "ui_server.h"
#include "mysql.h"
#include <QMessageBox>

Server::Server(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Server)
{
    ui->setupUi(this);
    if (!MySql::GetInstance()->GetStatus()){
        QMessageBox::about(this, "警告", "数据库连接失败");
    }
    Qt::WindowFlags flags=Qt::Dialog;
    flags |=Qt::WindowMinMaxButtonsHint;
    flags |=Qt::WindowCloseButtonHint;
    setWindowFlags(flags);
    InitTable();
}



void Server::InitTable()
{
    ui->table->horizontalHeader()->setStretchLastSection(true);
    GetData();
}

void Server::GetData()
{   
    int server = ui->comboBox->currentIndex();
    QStringList res = MySql::GetInstance()->SelectByServer(server);
    qDebug() << res;
    int row_count = res.size() / 5;
    ui->table->setRowCount(row_count);
    for (int i = 0; i < res.size(); ++i) {
        if ((i + 1) % 6 == 1) ui->table->setColumnHidden(i,true);
        if ((i + 1) % 5 == 0) continue;
        QTableWidgetItem *item=new QTableWidgetItem(res.value(i));
        ui->table->setItem(i / 5, i % 5, item);
    }
}

Server::~Server()
{
    delete ui;
}

void Server::on_comboBox_currentIndexChanged(int index)
{
    GetData();
}

void Server::on_btn_add_clicked()
{
    QString begin_time = ui->begin_hour->text() + ":" + ui->begin_min->text();
    if (ui->begin_hour->text() == "" || ui->begin_min->text() == ""){
        QMessageBox::about(this,"提示", "开始时间为空");
        return;
    }
    QString end_time = ui->end_hour->text() + ":" + ui->end_min->text();
    if (ui->end_hour->text() == "" || ui->end_min->text() == ""){
        QMessageBox::about(this,"提示", "结束时间为空");
        return;
    }
    QString web_site = ui->web_site->text();
    if (web_site == ""){
        QMessageBox::about(this,"提示", "网站为空");
        return;
    }
    QString server = QString::number(ui->comboBox->currentIndex());
    if (server == ""){
        QMessageBox::about(this,"提示", "服务器为空");
        return;
    }
    QStringList value;
    value.append(begin_time);
    value.append(end_time);
    value.append(web_site);
    value.append(server);
    if (MySql::GetInstance()->InsertData(value))
    {
        QMessageBox::about(this,"提示", "插入成功");
        GetData();
    }
    else {
        QMessageBox::about(this,"提示", "插入失败");
    }
}

void Server::on_btn_del_clicked()
{
    int sel_index = ui->table->currentRow();
    if (sel_index < 0){
        QMessageBox::about(this,"提示", "选中删除行");
    }
    int id = ui->table->item(sel_index, 0)->text().toInt();
    if(MySql::GetInstance()->DeleteData(id)){
        QMessageBox::about(this,"提示", "删除成功");
        GetData();
    }
    else {
        QMessageBox::about(this,"提示", "删除失败");
    }
}

void Server::on_btn_update_clicked()
{
    int sel_index = ui->table->currentRow();
    if (sel_index < 0){
        QMessageBox::about(this,"提示", "选中更新行");
    }
    int id = ui->table->item(sel_index, 0)->text().toInt();
    QString begin_time = ui->begin_hour->text() + ":" + ui->begin_min->text();
    if (ui->begin_hour->text() == "" || ui->begin_min->text() == ""){
        QMessageBox::about(this,"提示", "开始时间为空");
        return;
    }
    QString end_time = ui->end_hour->text() + ":" + ui->end_min->text();
    if (ui->end_hour->text() == "" || ui->end_min->text() == ""){
        QMessageBox::about(this,"提示", "结束时间为空");
        return;
    }
    QString web_site = ui->web_site->text();
    if (web_site == ""){
        QMessageBox::about(this,"提示", "网站为空");
        return;
    }
    QString server = QString::number(ui->comboBox->currentIndex());
    if (server == ""){
        QMessageBox::about(this,"提示", "服务器为空");
        return;
    }
    QStringList value_list;
    value_list.append(QString::number(id));
    value_list.append(begin_time);
    value_list.append(end_time);
    value_list.append(web_site);
    value_list.append(server);
    if(MySql::GetInstance()->UpdateData(value_list)){
        QMessageBox::about(this,"提示", "更新成功");
        GetData();
    }
    else {
        QMessageBox::about(this,"提示", "更新失败");
    }
}

void Server::on_btn_refresh_clicked()
{
    GetData();
}
