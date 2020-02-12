#include "mysql.h"

#include <QFile>
#include <QTextCodec>


MySql *MySql::m_instance_ = nullptr;

MySql::MySql()
{
    ReadConfig();
    InitDatabase();
}

MySql::~MySql()
{
    DeleteInstance();
}

void MySql::InitDatabase()
{
    //连接数据库
    //显示已有的数据库driver
    qDebug()<<QSqlDatabase::drivers();
    settings_->setValue("drivers",QSqlDatabase::drivers());
    db_ = QSqlDatabase::addDatabase("QMYSQL");
    sqlquery_ = QSqlQuery(db_);
    settings_->setValue("db_",db_.driverName());
    settings_->setValue("sqlquery_",sqlquery_.driver());
//    db_.setHostName("192.168.31.163");//连接本地的Mysql数据库，如果是远程的remote，需要输入对应的IP:"127.0.0.1"
    db_.setHostName(ip_);//连接本地的Mysql数据库，如果是远程的remote，需要输入对应的IP:"127.0.0.1"
    db_.setDatabaseName(database_name_);//默认连接的数据库名称为 test，后面的例子在名称为 test 的数据库里面，创建了一个名称为  test_talbe 的表
    db_.setPort(3306);
    db_.setUserName(user_name_);//数据库登录用户名
    db_.setPassword(password_);//数据库登录密码
    settings_->setValue("setHostName",db_.hostName());
    settings_->setValue("setDatabaseName",db_.databaseName());
    settings_->setValue("setUserName",db_.userName());
    settings_->setValue("setPassword",db_.password());
    settings_->setValue("setPort",db_.port());
    if(!db_.open()) //连接数据库，成功显示open success，否则显示Failed to connect to root mysql admin
    {
         qDebug()<<"Failed to connect to root mysql admin";
         settings_->setValue("open_fail",db_.databaseName() + " " + db_.userName() + " " + db_.password());
         status_ = false;

    } else {
        qDebug()<<"open success!";
        status_ = true;
    }

}

QSqlQueryModel* MySql::SelectAll()
{
    QSqlQueryModel *model = new QSqlQueryModel;
    model->setQuery(QString("SELECT * FROM %1").arg("test.test"));
    qDebug() << model;
    return model;
}

QStringList MySql::SelectByServer(int server)
{
   QStringList retstr;
   QString sq=QStringLiteral("select *from test where server='%1' ").arg(server);
   sqlquery_.exec(sq);
   while (sqlquery_.next())
   {
       for(int i = 0; i < 5; i++)
           retstr.append(sqlquery_.value(i).toString());
   }
   return retstr;
}

bool MySql::InsertData(QStringList list)
{
//    qDebug() << list.value(0);
//    qDebug() << list.value(1);
//    qDebug() << list.value(2);
//    qDebug() << list.value(3);
    sqlquery_.prepare("INSERT INTO test(begin_time,end_time,web,server)" "VALUES(:begin_time,:end_time,:web,:server)");
    sqlquery_.bindValue(":begin_time",list.value(0));
    sqlquery_.bindValue(":end_time",list.value(1));
    sqlquery_.bindValue(":web",list.value(2));
    sqlquery_.bindValue(":server",list.value(3));
    return sqlquery_.exec();
}

bool MySql::DeleteData(int id)
{
    sqlquery_.prepare(QString("DELETE FROM test WHERE id=?"));
    sqlquery_.addBindValue(id);
    return sqlquery_.exec();
}

bool MySql::UpdateData(QStringList list)
{
    qDebug() << list.value(0);
    qDebug() << list.value(1);
    qDebug() << list.value(2);
    qDebug() << list.value(3);
    qDebug() << list.value(4);
    sqlquery_.prepare("update test set begin_time=?,end_time=?,web=?,server=? where id=?");
    sqlquery_.addBindValue(list.value(1));
    sqlquery_.addBindValue(list.value(2));
    sqlquery_.addBindValue(list.value(3));
    sqlquery_.addBindValue(list.value(4));
    sqlquery_.addBindValue(list.value(0));

    return sqlquery_.exec();
}

bool MySql::GetStatus()
{
    return status_;
}

QString MySql::GetIp()
{
    return ip_;
}

bool MySql::ReadConfig()
{
    QString appPath = QCoreApplication::applicationDirPath();
    settings_ = new QSettings (appPath + "\\config.ini",QSettings::IniFormat);
    settings_->beginGroup("SerialPort");
    ip_ = settings_->value("ip","192.168.31.163").toString();
    database_name_ = settings_->value("database_name","test").toString();
    user_name_ = settings_->value("user_name","root").toString();
    password_ = settings_->value("password","1234").toString();
    qDebug() << ip_;
}

bool MySql::DeleteInstance()
{
    delete settings_;    //删除指针，防止内存泄露
    db_.close();
}

bool MySql::DownloadPy()
{
    QStringList retstr;
    QString sq=QStringLiteral("select *from python");
    sqlquery_.exec(sq);
    if (sqlquery_.next())
    {
        QFile file("login.py");

        file.open(QIODevice::ReadWrite | QIODevice::Truncate);

        file.resize(0);

        QTextStream in(&file);



        QByteArray array = sqlquery_.value(0).toByteArray();


        QTextCodec* gbk_codec = QTextCodec::codecForName("gbk");

        QString gbk_string = gbk_codec->toUnicode(array);

        //QByteArray utf8_bytes=utf8->fromUnicode(gbk_string);
        //QString python = utf8_bytes.data(); //获取其char *

        in << gbk_string;

        return true;
    }
    return false;
}

