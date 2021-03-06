# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql
import json
import configparser
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QTimer

class UiDialog(object):
    is_run = -1
    id = -1
    conf = configparser.ConfigParser()
    timer = QTimer() #初始化一个定时器
    web_site_ = ""
    # 读取 json 配置文件
    with open('conf/default.conf', 'r') as confFile:
        confStr = confFile.read()
    conf_json = json.JSONDecoder().decode(confStr)
    # connect table result
    dbStaticResult = conf_json['database']['test']

    # 打开数据库连接
    connection = pymysql.connect(host=dbStaticResult['host'],
                                 port=3306,
                                 user=dbStaticResult['user'],
                                 password=dbStaticResult['password'],
                                 db=dbStaticResult['database'],
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    # 获取游标
    cursor = connection.cursor()

    # def close_chrome(self):
        
    # def __init__(self):
    #     self.ReadCfg()
    #     self.send_time = random.randint(self.test_sent_time_1, self.test_sent_time_2)

    def __del__(self):
        # 关闭游标和数据库的连接
        self.cursor.close()
        self.connection.close()

    # 刷新界面
    def Refresh(self):
        index = self.comboBox.currentIndex()

        # 使用execute()方法执行SQL语句
        self.cursor.execute("select *from test where server=" + str(index))

        # 获取单条数据
        data = self.cursor.fetchall()
        ret_json = json.dumps(data)
        # print(ret_json)
        json_array = json.loads(ret_json)

        self.table.clearContents()
        count = 0
        self.is_run = -1
        self.id = -1
        print("id = " + str(self.id) + ", is_run = " + str(self.is_run))
        current_time = time.strftime("%H:%M")  # 24小时格式 
        for it in json_array:
            self.table.setRowCount(count + 1)
            item = QTableWidgetItem()
            item.setText(str(it['id']))
            self.table.setItem(count, 0, item)
            item = QTableWidgetItem()
            item.setText(it['begin_time'])
            self.table.setItem(count, 1, item)
            item = QTableWidgetItem()
            item.setText(it['end_time'])
            self.table.setItem(count, 2, item)
            item = QTableWidgetItem()
            item.setText(it['web'])
            self.table.setItem(count, 3, item)            

            begin_time = it['begin_time']
            end_time   = it['end_time']
            # 判断是否有正在运行的任务
            if current_time >= begin_time:
                if current_time < end_time:
                    print("有正在运行的任务")
                    self.web_site_ = it['web']
                    self.is_run = count
                    self.id = self.table.item(count, 0).text()
                    print("is_run = ", self.is_run)
                    print("id = ", self.id)
            # 判断是否有需要停止的任务
            if (self.is_run >= 0):
                if (self.is_run != count):
                    count = count + 1
                    continue
                if (current_time >= end_time):
                    print("有需要停止的任务")
                    self.is_run = -1
                    self.id = -1
                    self.web_site_ = ""
                    print("is_run = ", self.is_run)
                    print("id = ", self.id)  
            count = count + 1
    
    # 开始
    def Start(self):
        if self.btn_start.text() == "结束":
            print("end_button click!")
            self.btn_start.setText("开始")
            self.is_run = -2
            self.id     = -2
            self.timer.stop() 
        else:
            print("开始")
            self.btn_start.setText("结束")
            self.is_run = -1
            self.id     = -1
            self.timer.timeout.connect(self.operate) #计时结束调用operate()方法
            self.timer.start(5400) #设置计时间隔并启动
                
    def operate(self):
        if (self.is_run == -2):
            return
        self.Refresh()
    
    # 选择切换
    def Select(self, index):
        print("重新加载数据", index)
        self.Refresh()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1025, 549)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.table = QtWidgets.QTableWidget(Dialog)
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setObjectName("table")
        self.table.setColumnCount(4)
        self.table.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(0, 3, item)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setSortIndicatorShown(False)
        self.table.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_3.addWidget(self.table)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(0, 30))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.interval_1 = QtWidgets.QLineEdit(Dialog)
        self.interval_1.setMinimumSize(QtCore.QSize(0, 30))
        self.interval_1.setObjectName("interval_1")
        self.gridLayout.addWidget(self.interval_1, 0, 1, 1, 1)
        self.interval_2 = QtWidgets.QLineEdit(Dialog)
        self.interval_2.setMinimumSize(QtCore.QSize(0, 30))
        self.interval_2.setObjectName("interval_2")
        self.gridLayout.addWidget(self.interval_2, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.sent_time_1 = QtWidgets.QLineEdit(Dialog)
        self.sent_time_1.setMinimumSize(QtCore.QSize(0, 30))
        self.sent_time_1.setObjectName("sent_time_1")
        self.gridLayout.addWidget(self.sent_time_1, 1, 1, 1, 1)
        self.sent_time_2 = QtWidgets.QLineEdit(Dialog)
        self.sent_time_2.setMinimumSize(QtCore.QSize(0, 30))
        self.sent_time_2.setObjectName("sent_time_2")
        self.gridLayout.addWidget(self.sent_time_2, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.interval_3 = QtWidgets.QLineEdit(Dialog)
        self.interval_3.setMinimumSize(QtCore.QSize(0, 30))
        self.interval_3.setObjectName("interval_3")
        self.gridLayout.addWidget(self.interval_3, 2, 1, 1, 1)
        self.interval_4 = QtWidgets.QLineEdit(Dialog)
        self.interval_4.setMinimumSize(QtCore.QSize(0, 30))
        self.interval_4.setObjectName("interval_4")
        self.gridLayout.addWidget(self.interval_4, 2, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.listView = QtWidgets.QListView(Dialog)
        self.listView.setObjectName("listView")
        self.horizontalLayout_2.addWidget(self.listView)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215, 55))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.btn_start = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_start.sizePolicy().hasHeightForWidth())
        self.btn_start.setSizePolicy(sizePolicy)
        self.btn_start.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.btn_start.setObjectName("btn_start")
        self.verticalLayout_2.addWidget(self.btn_start)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.Refresh()
        self.pushButton.clicked.connect(self.Refresh)
        self.btn_start.clicked.connect(self.Start)
        self.comboBox.currentIndexChanged.connect(self.Select)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "客户端"))
        item = self.table.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.table.verticalHeaderItem(1)
        item.setText(_translate("Dialog", "2"))
        item = self.table.verticalHeaderItem(2)
        item.setText(_translate("Dialog", "3"))
        item = self.table.verticalHeaderItem(3)
        item.setText(_translate("Dialog", "4"))
        item = self.table.verticalHeaderItem(4)
        item.setText(_translate("Dialog", "5"))
        item = self.table.verticalHeaderItem(5)
        item.setText(_translate("Dialog", "6"))
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "id"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "启动时间"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "结束时间"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "地址"))
        __sortingEnabled = self.table.isSortingEnabled()
        self.table.setSortingEnabled(False)
        item = self.table.item(0, 0)
        item.setText(_translate("Dialog", "0"))
        item = self.table.item(0, 1)
        item.setText(_translate("Dialog", "10:29"))
        item = self.table.item(0, 2)
        item.setText(_translate("Dialog", "12:29"))
        item = self.table.item(0, 3)
        item.setText(_translate("Dialog", "www.baidu.com/31313l1jk31lj"))
        self.table.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(_translate("Dialog", "间隔时间"))
        self.interval_1.setText(_translate("Dialog", "1200"))
        self.interval_2.setText(_translate("Dialog", "1500"))
        self.label_3.setText(_translate("Dialog", "刷新次数"))
        self.sent_time_1.setText(_translate("Dialog", "3"))
        self.sent_time_2.setText(_translate("Dialog", "5"))
        self.label_4.setText(_translate("Dialog", "间隔时间"))
        self.interval_3.setText(_translate("Dialog", "60"))
        self.interval_4.setText(_translate("Dialog", "80"))
        self.label.setText(_translate("Dialog", "服务器地址"))
        self.comboBox.setItemText(0, _translate("Dialog", "wang1"))
        self.comboBox.setItemText(1, _translate("Dialog", "wang2"))
        self.comboBox.setItemText(2, _translate("Dialog", "wang3"))
        self.comboBox.setItemText(3, _translate("Dialog", "wang4"))
        self.comboBox.setItemText(4, _translate("Dialog", "wang5"))
        self.comboBox.setItemText(5, _translate("Dialog", "wang6"))
        self.comboBox.setItemText(6, _translate("Dialog", "wang7"))
        self.comboBox.setItemText(7, _translate("Dialog", "wang8"))
        self.comboBox.setItemText(8, _translate("Dialog", "wang9"))
        self.pushButton.setText(_translate("Dialog", "刷新"))
        self.btn_start.setText(_translate("Dialog", "开始"))
