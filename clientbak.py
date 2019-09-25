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
import random
from selenium import webdriver

from PyQt5.QtWidgets import QTableWidgetItem

# /tmp/.com.google.Chrome.XxgqMm/Default
# /tmp/.com.google.Chrome.Z3zbNV/Default

class UiDialog(object):
    test_interval_1 = 0
    test_interval_2 = 0
    test_interval_3 = 0
    test_interval_4 = 0
    test_sent_time_1 = 0
    test_sent_time_2 = 0
    test_web_site = ""
    qq_index = 0
    conf = configparser.ConfigParser()
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

    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    def __init__(self):
        self.ReadCfg()
        self.send_time = random.randint(self.test_sent_time_1, self.test_sent_time_2)

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
        print(ret_json)
        json_array = json.loads(ret_json)

        self.table.clearContents()
        count = 0
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
            count = count + 1

    # 开始
    def Start(self):
        if self.btn_start.text() == "结束":
            self.btn_start.setText("开始")
            self.dr.quit()
        else:
            print("开始")
            self.btn_start.setText("结束")
            if self.qq_index == 3:
                userDataPath = "/home/believe/.config/google-chrome/test"
            else:
                userDataPath = "/home/believe/.config/google-chrome/believe"
            self.options.add_argument("--user-data-dir=" + userDataPath + "/ChromeUserData")
            self.options.add_argument("--profile-directory=Profile ")

            try:
                self.dr = webdriver.Chrome(options=self.options)
                self.dr.get("https://egame.qq.com")
                print("gaga")
                self.dr.get(self.test_web_site)
                self.dr.implicitly_wait(3)
                # try:
                #     # 点击QQ登录
                #     self.dr.find_element_by_link_text("登录").click()
                #     time.sleep(3)
                #
                #     # 切换到iframe
                #     self.dr.switch_to.frame("_egame_login_frame_qq_")
                #     self.dr.switch_to.frame("ptlogin_iframe")
                #
                #     # 点击本地qq号登陆
                #     self.dr.execute_script('document.getElementById("qlogin").style="display: none;"')
                #     self.dr.execute_script('document.getElementsByClassName("authLogin").style="display: none;"')
                #     self.dr.execute_script('document.getElementById("web_qr_login").style="display: block;"')
                #     # browser.evaluate_script('document.getElementById("batch_quto").contentEditable = true')
                #     time.sleep(3)
                #
                #     if self.qq_index == 3:
                #         # self.dr.find_element_by_xpath("//*[@id='qlogin_list']/a[1]").click()
                #         # 隐藏初始界面
                #         # elem_user = self.dr.find_element_by_name("u").send_keys("1576558587")
                #         elem_user = self.dr.find_element_by_name("u").send_keys("765846560")
                #         time.sleep(1)
                #         # elem_pwd = self.dr.find_element_by_name("p").send_keys("dudu666")
                #         elem_pwd = self.dr.find_element_by_name("p").send_keys("believe123")
                #         elem_but = self.dr.find_element_by_id("login_button").click()
                #         self.conf.set('Option', 'qq_index', '1')
                #         self.conf.write(open("qq_index.txt", "w"))
                #     else:
                #         # self.dr.find_element_by_xpath("//*[@id='qlogin_list']/a[3]").click()
                #         elem_user = self.dr.find_element_by_name("u").send_keys("765846560")
                #         time.sleep(1)
                #         elem_pwd = self.dr.find_element_by_name("p").send_keys("believe123")
                #         elem_but = self.dr.find_element_by_id("login_button").click()
                #         self.conf.set('Option', 'qq_index', '3')
                #         self.conf.write(open("qq_index.txt", "w"))
                #     print("登录成功")
                # except Exception as e:
                #     print(e)
                time.sleep(3)
                try:
                    print("找流畅")
                    self.dr.find_element_by_xpath(
                        "//*[@id='video-container-" + self.test_web_site[21:] + "']/div/div[5]/div[8]/a").click()
                    time.sleep(1)
                    self.dr.find_element_by_link_text("流畅").click()
                    # dr.find_element_by_xpath("//*[@id='video-container-" + web_site[21:] + "']/div/div[5]/div[8]/div/div[2]/div[2]/a[4]").click()
                except:
                    try:
                        print("找高清")
                        time.sleep(1)
                        self.dr.find_element_by_link_text("高清").click()
                        # dr.find_element_by_xpath("//*[@id='video-container-" + web_site[21:] + "']/div/div[5]/div[8]").click()
                        # dr.find_element_by_xpath("//*[@id='video-container-" + web_site[21:] + "']/div/div[5]/div[8]/div/div[2]/div[2]/a[3]").click()
                    except Exception as e:
                        print(e)

                # 刷新指定次数
                interval_time = random.randint(self.test_interval_1, self.test_interval_2)
                count = self.send_time
                while count > 0:
                    print('The count is:', count)
                    count = count - 1
                    time.sleep(interval_time)
                    self.dr.refresh()  # 刷新方法 refresh
                    print("刷新成功")
                print("关闭显示器")
                self.dr.quit()
            except Exception as e:
                print(e)
            # 切换 qq 号
            qq_interval_time = random.randint(self.test_interval_3, self.test_interval_4)
            print(qq_interval_time)
            time.sleep(qq_interval_time)

    # 选择切换
    def Select(self, index):
        print("重新加载数据", index)
        self.Refresh()

    def ReadCfg(self):
        # 生成config对象

        # 用config对象读取配置文件
        self.conf.read("test.cfg")
        # 以列表形式返回所有的section
        sections = self.conf.sections()
        print("sections:", sections)  # sections: ['sec_b', 'Option']
        # 得到指定section的所有option
        options = self.conf.options("Option")
        print("options:", options)  # options: ['a_key1', 'a_key2']
        # 得到指定section的所有键值对
        kvs = self.conf.items("Option")
        print("Option:", kvs)  # Option: [('a_key1', '20'), ('a_key2', '10')]
        # 指定section，option读取值
        self.test_interval_1 = self.conf.getint("Option", "test_interval_1")
        self.test_interval_2 = self.conf.getint("Option", "test_interval_2")
        self.test_interval_3 = self.conf.getint("Option", "test_interval_3")
        self.test_interval_4 = self.conf.getint("Option", "test_interval_4")
        self.test_sent_time_1 = self.conf.getint("Option", "test_sent_time_1")
        self.test_sent_time_2 = self.conf.getint("Option", "test_sent_time_2")
        self.test_web_site = self.conf.get("Option", "test_web_site")
        self.qq_index = self.conf.getint("Option", "qq_index")

        print("value for Option's interval_1:", self.test_interval_1)  # value for Option's a_key1: 20
        print("value for Option's interval_2:", self.test_interval_2)  # value for Option's a_key2: 10
        print("value for Option's interval_3:", self.test_interval_3)  # value for Option's a_key2: 10
        print("value for Option's interval_ 4:", self.test_interval_4)  # value for Option's a_key2: 10
        print("value for Option's sent_time_1:", self.test_sent_time_1)  # value for Option's a_key2: 10
        print("value for Option's sent_time_2:", self.test_sent_time_2)  # value for Option's a_key2: 10
        print("value for Option's web:", self.test_web_site)  # value for Option's a_key2: 10

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

        # 加载配置文件内容
        self.interval_1.setText(str(self.test_interval_1))
        self.interval_2.setText(str(self.test_interval_2))
        self.interval_3.setText(str(self.test_interval_3))
        self.interval_4.setText(str(self.test_interval_4))
        self.sent_time_1.setText(str(self.test_sent_time_1))
        self.sent_time_2.setText(str(self.test_sent_time_2))

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
        self.btn_start.setText(_translate("Dialog", "开始操作"))
