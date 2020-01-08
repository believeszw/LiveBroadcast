#include "dialog.h"
#include "ui_dialog.h"
#include <QDebug>
#include <QFile>
#include <QTime>
#include "mysql.h"
#include <QMessageBox>
#include <fstream>
#include <Windows.h>
#include <tlhelp32.h>

BOOL CALLBACK EnumWindowsProc(HWND hWnd, long lParam) {

    wchar_t buff[255];
    hWnd = GetForegroundWindow();
    if (IsWindowVisible(hWnd))
    {
//        GetWindowText(hWnd, buff, 254);
        GetWindowTextW(hWnd,buff,254);
        DWORD  Process_id;
        GetWindowThreadProcessId(hWnd,&Process_id);
        QString process_name = QString::fromWCharArray(buff);
        if (process_name != "客户端" && process_name != "Program Manager"
                && process_name != "" && process_name.right(6) != "Chrome"
                && process_name != "开始" && Process_id != 0)
        {
            qDebug() << QString::fromWCharArray(buff);
            HANDLE hProcess=OpenProcess(PROCESS_TERMINATE,FALSE,Process_id);
            FILE *fp = NULL;
            fp = fopen("process.txt", "a");
            fputs(QString::fromWCharArray(buff).toStdString().c_str(), fp);
            fputs(QString::number(Process_id).toStdString().c_str(), fp);
            fputs("\n",fp);
            fclose(fp);
            TerminateProcess(hProcess,0);            
        }
    }
    return TRUE;
}

Dialog::Dialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Dialog)
{
    ui->setupUi(this);
    if (!MySql::GetInstance()->GetStatus()){
        QMessageBox::about(this, "警告", "数据库连接失败");
        QMessageBox::about(this, "提示", MySql::GetInstance()->GetIp());
    }
    Qt::WindowFlags flags=Qt::Dialog;
    flags |=Qt::WindowMinMaxButtonsHint;
    flags |=Qt::WindowCloseButtonHint;
    setWindowFlags(flags);

    is_run_ = false;
    //proc_ = new QProcess();
    //proc_->setEnvironment(proc_->environment());
    InitTable();
    // 设置 1 min 的定时器
    timer_ = new QTimer(this);
    connect(timer_, SIGNAL(timeout()), this, SLOT(showTime()));
}


Dialog::~Dialog()
{
    StopProcess();
    delete list_model_;
    list_model_ = nullptr;
    delete timer_;
    timer_ = nullptr;
    delete ui;
}


void Dialog::InitTable()
{
    ui->table->horizontalHeader()->setStretchLastSection(true);
    GetData();
    list_model_ = new QStandardItemModel(this);
    ui->listView->setModel(list_model_);
}

void Dialog::GetData()
{
    int server = ui->comboBox->currentIndex();
    QStringList res = MySql::GetInstance()->SelectByServer(server);   
    int row_count = res.size() / 5;
    for (int i = 0;i < 3; ++i) {
        if (row_count == 0) {
            MySql::GetInstance()->DeleteInstance();
            MySql::GetInstance()->ReadConfig();
            MySql::GetInstance()->InitDatabase();
            res = MySql::GetInstance()->SelectByServer(server);
            row_count = res.size() / 5;
        } else {
            break;
        }
    }

    ui->table->setRowCount(row_count);
    for (int i = 0; i < res.size(); ++i) {
        if ((i + 1) % 6 == 1) ui->table->setColumnHidden(i,true);
        if ((i + 1) % 5 == 0) continue;
        QTableWidgetItem *item=new QTableWidgetItem(res.value(i));
        ui->table->setItem(i / 5, i % 5, item);
    }
}


void Dialog::WriteCfg(){

    QFile file("test.cfg");
    QString tmp;
    //判断文件是否存在
    if(file.exists()){
        tmp += "文件已存在 ";
    }else{
        tmp += "文件不存在 ";
    }
    //已读写方式打开文件，
    //如果文件不存在会自动创建文件
    if(!file.open(QIODevice::ReadWrite | QIODevice::Truncate)){
        tmp += "打开失败 ";
    }else{
        tmp += "打开成功 ";
    }

    //获得文件大小
    qint64 pos;
    pos = file.size();
    //重新定位文件输入位置，这里是定位到文件尾端
    file.seek(pos);

    QString content = "[Option]";
    content += "\ninterval_1 = " + ui->interval_1->text();
    content += "\ninterval_2 = " + ui->interval_2->text();
    content += "\nsent_time_1 = " + ui->sent_time_1->text();
    content += "\nsent_time_2 = " + ui->sent_time_2->text();
    content += "\ninterval_3 = " + ui->interval_3->text();
    content += "\ninterval_4 = " + ui->interval_4->text();
    content += "\nweb_site = " + ui->table->item(ui->table->currentRow(), 3)->text();

    //写入文件
    qint64 length = -1;
    length = file.write(content.toLatin1(),content.length());

    if(length == -1){
        tmp += "写入文件失败 ";
        QMessageBox::about(this, "提示", "文件写入失败");
    }else{
        tmp += "写入文件成功";
    }
    ListViewAdd(tmp);

    //关闭文件
    file.close();
}

void Dialog::StartProcess()
{
    is_run_ = true;
    Sleep(3000);
    QString appPath = QCoreApplication::applicationDirPath();
    qDebug() << "Start Process";
//    proc_->execute("python .")+appPath+tr("\\login.py");
    QProcess proc_;
    proc_.start(tr("py ")+appPath+tr(".\\login.py"));
    proc_.waitForStarted();

    ListViewAdd("py login.py");
//    proc_->start("cmd.exe");
//    QString arg = "cd " + appPath + tr(" \r\n");
//    arg.replace("/","\\\\");
//    char* args = arg.toLatin1().data();
//    qDebug() << args;
//    proc_->write(args);
//    proc_->waitForStarted();
//    proc_->write("mkdir test\r\n py login.py\r\n");
//    proc_->waitForFinished();
////    proc_->waitForFinished();
////    proc_->write("exit\n\r");
}

void Dialog::StopProcess()
{
    is_run_ = false;
    ListViewAdd("timer stop");
    timer_->stop();
    ListViewAdd("停止");
    KillTask();
}

void Dialog::KillTask()
{
    QProcess process;
    process.start("cmd.exe");
    process.write ("taskkill -f -im chromedriver.exe \n\r");
    process.write ("taskkill -f -im chrome.exe \n\r");
    process.write ("taskkill -f -im python.exe \n\r");
    process.write ("exit\n\r");
    process.waitForFinished();
//    process.close();
    ListViewAdd("killTaskDone");
}

void Dialog::ListViewAdd(QString str)
{
    QTime cur_time = QTime::currentTime();
    QString cur_hour = cur_time.toString("hh::mm::ss"); // 这儿有各种格式，比如 ("yyyy-MM-dd hh:mm:ss dddd") 等等;
    QStandardItem *item = new QStandardItem(str + "    " + cur_hour);
    QStandardItemModel *model = dynamic_cast<QStandardItemModel*>(ui->listView->model());
    model->appendRow(item);
}

bool Dialog::CheckAppRunningStatus(const QString &appName)
{
    qDebug() << "CheckAppRunningStatus";
#ifdef Q_OS_WIN
    QProcess* process = new QProcess;
    process->start("tasklist" ,QStringList()<<"/FI"<<"imagename eq " +appName);
    process->waitForFinished();
    QString outputStr = QString::fromLocal8Bit(process->readAllStandardOutput());
    if(outputStr.contains(appName)){
        return true;
    }
    else{
        return false;
    }
#endif
}

bool Dialog::FindAllWindow()
{
    WCHAR buff[MAX_PATH] = { 0 };
    setlocale(LC_ALL, "");
    HWND hWnd = GetForegroundWindow();
    if (IsWindowVisible(hWnd))
    {
        GetWindowTextW(hWnd,buff,254);
        DWORD  Process_id;
        GetWindowThreadProcessId(hWnd,&Process_id);
        QString process_name = QString::fromWCharArray(buff);
        ListViewAdd(process_name);
        if (process_name != "客户端" && process_name != "Program Manager"
                && process_name != "" && process_name.right(6) != "Chrome"
                && process_name != "开始" && Process_id != 0)
        {
            qDebug() << QString::fromWCharArray(buff);
            HANDLE hProcess=OpenProcess(PROCESS_TERMINATE,FALSE,Process_id);
            FILE *fp = NULL;
            fp = fopen("process.txt", "a");
            fputs(QString::fromWCharArray(buff).toStdString().c_str(), fp);
            fputs(QString::number(Process_id).toStdString().c_str(), fp);
            fputs("\n",fp);
            fclose(fp);
            TerminateProcess(hProcess,0);
        }
    }
}


void Dialog::on_btn_start_clicked()
{
    if (ui->btn_start->text() == "开始操作")
    {
        qDebug() << (ui->btn_start->text() == "开始操作");
        ui->btn_start->setText("运行中");
        timer_->start(30000);
//        timer_->start(1000);
//        StartProcess();
        return;
    }
    if (ui->btn_start->text() == "运行中")
    {
        StopProcess();
        ui->btn_start->setText("开始操作");
    }
}

void Dialog::on_comboBox_currentIndexChanged(int index)
{
    GetData();
}

void Dialog::showTime()
{
    GetData();
//    FindAllWindow();
    QTime cur_time = QTime::currentTime();
    int cur_date = cur_time.toString("dd").toInt();
    int cur_hour = cur_time.toString("hh").toInt(); // 这儿有各种格式，比如 ("yyyy-MM-dd hh:mm:ss dddd") 等等;
    int cur_min = cur_time.toString("mm").toInt();
//    qDebug() << "cur_hour = " << cur_hour << ", min = " << cur_min;

    int row_count = ui->table->rowCount();
    if (row_count == 0)
    {
        // 结束进程
        qDebug() << "jieshu";
        ListViewAdd("结束进程，行数为0");
        is_run_ = false;
        KillTask();
        return;
    }

    for (int i = 0; i < row_count; ++i)
    {
        int begin_time_hour = ui->table->item(i, 1)->text().mid(0,2).toInt();
        int begin_time_min  = ui->table->item(i, 1)->text().mid(3,2).toInt();
        int end_time_hour   = ui->table->item(i, 2)->text().mid(0,2).toInt();
        int end_time_min    = ui->table->item(i, 2)->text().mid(3,2).toInt();
//        qDebug() << "begin_time_hour = " << begin_time_hour << ", min = " << begin_time_min;
//        qDebug() << "end_time_hour   = " << end_time_hour   << ", min = " << end_time_min;
        if (end_time_hour < begin_time_hour)
        {
            end_time_hour += 24;
        }
        // 启动程序
        if ((begin_time_hour * 60 + begin_time_min) <= (cur_hour * 60 + cur_min)
                && (cur_hour * 60 + cur_min) < (end_time_hour * 60 + end_time_min))
        {
            ui->table->setCurrentCell(i, i);
            // 运行脚本
            cur_row_ = i;
            if (is_run_ == false)
            {
                WriteCfg();
                StartProcess();
                qDebug() << "执行脚本";
                is_run_ = true;
                return;
            }
//            if ((cur_hour * 60 + cur_min - (begin_time_hour * 60 + begin_time_min)) % 120 == 0
//                    && (cur_hour * 60 + cur_min - (begin_time_hour * 60 + begin_time_min)) > 0)
//            {
//                // 清除进程
//                ListViewAdd("两小时重新运行");
//                KillTask();
//                Sleep(5000);
//                StartProcess();
//                return;
//            }
            if (!CheckAppRunningStatus("py.exe"))
            {
                qDebug() << "py.exe";
                ListViewAdd("python未运行，重新调用");
                KillTask();
                Sleep(5000);
                StartProcess();
                return;
            }
        }
        int tmp_cur_hour = cur_hour;
        if (is_run_ == true && cur_row_ == i && cur_hour < begin_time_hour)
        {
            tmp_cur_hour += 24;
        }
        if (is_run_ == true && cur_row_ == i && (tmp_cur_hour * 60 + cur_min) > (end_time_hour * 60 + end_time_min))
        {
            // 结束进程
            qDebug() << "结束进程";
            is_run_ = false;
            cur_row_ = -1;
            ListViewAdd("到时间，结束");
            KillTask();
            return;
        }
    }
}



void Dialog::on_pushButton_clicked()
{
    GetData();
    KillTask();
}
