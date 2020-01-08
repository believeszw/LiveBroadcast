#ifndef MYSQL_H
#define MYSQL_H


#include <QCoreApplication>
#include <QSqlDriver>
#include <QSqlDatabase>
#include <QSqlQuery>
#include <QDebug>
#include <QMutex>
#include <QSqlQueryModel>
#include <QSettings>

class MySql
{
public:
   static MySql* GetInstance()
   {
       static QMutex mutex;
       if (!m_instance_) {
           QMutexLocker locker(&mutex);
           if (!m_instance_)
               m_instance_ = new MySql;
       }

       return m_instance_;
   }
   void InitDatabase();
   QSqlQueryModel* SelectAll();
   QStringList SelectByServer(int server);
   bool InsertData(QStringList list);
   bool DeleteData(int id);
   bool UpdateData(QStringList list);
   bool GetStatus();
   QString GetIp();
   bool ReadConfig();
   bool DeleteInstance();
private:
private:
    MySql();
    ~MySql();
    static MySql* m_instance_;
    QSqlDatabase db_;
    QSqlQuery sqlquery_;
    bool status_;
    QString ip_;
    QString database_name_;
    QString user_name_;
    QString password_;
    QSettings *settings_;
};

#endif // MYSQL_H
