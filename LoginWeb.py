#coding='utf-8'
 
from PyQt5 import QtCore, QtGui
import time
import random
from client import UiDialog
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

class SeleniumHandler(QtCore.QThread, UiDialog):
    uidialog = None
    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    dr = None
     
    def __init__(self,  parent=None):
        super(SeleniumHandler,  self).__init__(parent)
        self.timer.timeout.connect(self.StartTask) #计时结束调用operate()方法
        self.timer.start(5400) #设置计时间隔并启动
        pass
    def GetUi(self, test):
        self.uidialog = test
        
    def run(self):
        # self.StartTask()
        # time.sleep(55)
        return

    def StartTask(self):
        print(self.uidialog.btn_start.text())
        if (self.uidialog.btn_start.text() == "开始"):
            return
        self.test_web_site = self.uidialog.web_site_
        print(self.test_web_site)
        self.ReadCfg()
        # 切换账号
        if self.qq_index == 3:
            self.conf.set('Option', 'qq_index', '1')
            print("qq_index = 1")
            self.conf.write(open("conf/test.cfg", "w"))
            userDataPath = "/home/believe/.config/google-chrome/believe"
        else:
            self.conf.set('Option', 'qq_index', '3')
            print("qq_index = 3")
            self.conf.write(open("conf/test.cfg", "w"))
            userDataPath = "/home/believe/.config/google-chrome/believe2"
        self.options.add_argument("--user-data-dir=" + userDataPath + "/ChromeUserData")
        self.options.add_argument("--profile-directory=Profile ")

        # 启动浏览器
        try:
            self.dr = webdriver.Chrome(options=self.options)
            self.dr.get("https://egame.qq.com")
            self.dr.implicitly_wait(5)
            self.dr.get(self.test_web_site)
            self.dr.implicitly_wait(5)
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
            time.sleep(1)
            element = self.dr.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[1]/div[2]/div[1]')
            ActionChains(self.dr).move_to_element(element).perform()
            try:
                print("关闭弹幕")
                self.dr.find_element_by_xpath("//*[@id='video-container-" + self.test_web_site[21:] + "']/div/div[5]/div[9]").click()            
                self.dr.find_element_by_xpath("//*[@id='video-container-" + self.test_web_site[21:] + "']/div/div[5]/div[10]").click()
            except Exception as e:
                print(e)
            # 刷新指定次数
            interval_time = random.randint(int(self.uidialog.interval_1.text()), int(self.uidialog.interval_2.text()))
            count = random.randint(int(self.uidialog.sent_time_1.text()), int(self.uidialog.sent_time_2.text()))
            while count > 0:
                print('The count is:', count)
                count = count - 1
                print("sleep for", interval_time)
                time.sleep(interval_time)
                self.dr.refresh()  # 刷新方法 refresh
                print("刷新成功")
                time.sleep(1)
                element = self.dr.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[1]/div[2]/div[1]')
                ActionChains(self.dr).move_to_element(element).perform()
                try:
                    print("关闭弹幕")
                    self.dr.find_element_by_xpath("//*[@id='video-container-" + self.test_web_site[21:] + "']/div/div[5]/div[9]").click()            
                    self.dr.find_element_by_xpath("//*[@id='video-container-" + self.test_web_site[21:] + "']/div/div[5]/div[10]").click()
                except Exception as e:
                    print(e)
            print("关闭显示器")
            self.dr.quit()
        except Exception as e:
            self.dr.quit()
            print(e)

        # 切换 qq 号
        qq_interval_time = random.randint(int(self.uidialog.interval_3.text()), int(self.uidialog.interval_4.text()))
        print("qq_interval_time = ", qq_interval_time)
        time.sleep(qq_interval_time)

    def ReadCfg(self):
        # 用config对象读取配置文件
        self.conf.read("conf/test.cfg")
        # 以列表形式返回所有的section
        sections = self.conf.sections()
        # print("sections:", sections)  # sections: ['sec_b', 'Option']
        # 得到指定section的所有option
        options = self.conf.options("Option")
        # print("options:", options)  # options: ['a_key1', 'a_key2']
        # 得到指定section的所有键值对
        kvs = self.conf.items("Option")
        print("Option:", kvs)  # Option: [('a_key1', '20'), ('a_key2', '10')]
        # 指定section，option读取值
        self.qq_index = self.conf.getint("Option", "qq_index")