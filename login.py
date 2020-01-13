# coding = utf-8
from selenium import webdriver
import time
import traceback
import logging
import configparser
import random
from  win32api  import  GetSystemMetrics
import psutil
import os
import json
import shutil
import glob
from selenium.webdriver.common.action_chains import ActionChains

# folders location
path = r'C:/Users/admin.PC/AppData/Local/Temp'

def delfile( path):

#   read all the files under the folder
    fileNames = glob.glob(path + r'\*')
    for fileName in fileNames:
        if (fileName != "C:\\Users\\admin.PC\\AppData\\Local\\Temp\\FXSAPIDebugLogFile.txt"):
            if (fileName != "C:\\Users\\admin.PC\\AppData\\Local\\Temp\\VSCode Crashes"):
                print(fileName)
                try:
        #           delete file
                    os.remove( fileName)
                except:
                    try:
        #               delete empty folders
                        os.rmdir( fileName)
                    except:
        #               Not empty, delete files under folders
                        delfile( fileName)
        #               now, folders are empty, delete it
                        os.rmdir( fileName)

def judgeprocess(processname):
    pl = psutil.pids()
    for pid in pl:
        if psutil.Process(pid).name() == processname:
            os.popen("taskkill /im " + processname + " -f")
            break
    else:
        print("not found")

logging.basicConfig(filename='log.log')

#生成config对象
conf = configparser.ConfigParser()
#用config对象读取配置文件
conf.read("test.cfg")
#以列表形式返回所有的section
sections = conf.sections()
print("sections:", sections)          #sections: ['sec_b', 'Option']
#得到指定section的所有option
options = conf.options("Option")
print("options:", options)            #options: ['a_key1', 'a_key2']
#得到指定section的所有键值对
kvs = conf.items("Option")
print("Option:", kvs)                  #Option: [('a_key1', '20'), ('a_key2', '10')]
#指定section，option读取值
interval_1 = conf.getint("Option", "interval_1")
interval_2 = conf.getint("Option", "interval_2")
interval_3 = conf.getint("Option", "interval_3")
interval_4 = conf.getint("Option", "interval_4")
sent_time_1 = conf.getint("Option", "sent_time_1")
sent_time_2 = conf.getint("Option", "sent_time_2")
web_site = conf.get("Option", "web_site")

print(web_site)

#生成config对象
conf_2 = configparser.ConfigParser()
#用config对象读取配置文件
conf_2.read("qq_index.txt")
#以列表形式返回所有的section
sections = conf_2.sections()
print("sections:", sections)          #sections: ['sec_b', 'Option']
#得到指定section的所有option
options = conf_2.options("Option")
print("options:", options)            #options: ['a_key1', 'a_key2']
#得到指定section的所有键值对
kvs = conf_2.items("Option")

#写配置文件
#更新指定section，option的值
# conf.set("sent_time_2", "Option", "new-$r")
#写入指定section增加新option和值
# conf.set("sent_time_2", "Option", "new-value")
#增加新的section
# conf.add_section('a_new_section')

# 取随机间隔时间
send_time = random.randint(sent_time_1, sent_time_2)

def move_and_sharpness():
    try:
        print("make video center")
        time.sleep(3)
        element = dr.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[2]')
        ActionChains(dr).move_to_element(element).perform()
        print("移动ok")
    except Exception as e:
        print(e)
    time.sleep(2)
    try:
        dr.find_element_by_xpath("//*[@id='video-container-" + web_site[21:] + "']/div/div[5]/div[8]").click()
        time.sleep(1)
        dr.find_element_by_link_text("流畅").click()
        ActionChains(dr).move_by_offset(-40, -40).perform()
        print("流畅")
    except:
        try:
            dr.find_element_by_link_text("高清").click()
            ActionChains(dr).move_by_offset(-40, -40).perform()
            print("高清")
        except:
            print("高清+++++")
            s = traceback.format_exc()
            logging.error(s)
    time.sleep(1)
    try:
        dr.find_element_by_xpath("//*[@id='video-container-" + web_site[21:] + "']/div/div[5]/div[9]").click()
        time.sleep(2)
        dr.find_element_by_xpath("//*[@id='video-container-" + web_site[21:] + "']/div/div[5]/div[10]").click()
        time.sleep(2)
        print("屏蔽礼物特效")
    except:
        print("屏蔽礼物特效失败")
        s = traceback.format_exc()
        logging.error(s)

    time.sleep(1)

    try:
        dr.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[3]/div[4]/div[2]/div/div/div/div/i').click()
        print("关闭红包成功")
    except:
        print("关闭红包失败")
        s = traceback.format_exc()
        logging.error(s)
    time.sleep(1)


while (0 < 9):
    options = webdriver.ChromeOptions()
    #options.add_argument('--no-startup-window')
    options.add_argument('--disable-application-cache')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-gpu')
    options.add_argument('blink-settings=imagesEnabled=false')
    options.add_argument('-disk-cache-size=1,-media-cache-size=1,-incognito')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    qq_index = conf_2.getint("Option", "qq_index")
    # 切换账号
    if qq_index == 3:
        conf_2.set('Option', 'qq_index', '1')
        conf_2.write(open("qq_index.txt", "w"))
        print("qq_index = 1")
        userDataPath = "C:/Users/admin.PC/AppData/Local/Google/Chrome/User Data/believe"
    else:
        conf_2.set('Option', 'qq_index', '3')
        conf_2.write(open("qq_index.txt", "w"))
        print("qq_index = 3")
        userDataPath = "C:/Users/admin.PC/AppData/Local/Google/Chrome/User Data/believe2"
    options.add_argument("--user-data-dir=" + userDataPath + "/ChromeUserData")
    options.add_argument("--profile-directory=Profile")
    dr = webdriver.Chrome(options=options)
    try:
        dr.set_window_position(x=40,y=40)
        dr.set_window_size(GetSystemMetrics (0) * 11 / 12,  GetSystemMetrics (1) * 9 / 10)
        dr.get("https://egame.qq.com")
        print(dr.title)
        time.sleep(3)
        dr.get(web_site)
        dr.implicitly_wait(5)
        time.sleep(2)

        move_and_sharpness()

        #点击QQ登录
        try:
            dr.find_element_by_link_text("登录").click()
        except:
            s = traceback.format_exc()
            logging.error(s)

        time.sleep(5)
        #切换到iframe
        try:
            dr.switch_to.frame("_egame_login_frame_qq_")
            dr.switch_to.frame("ptlogin_iframe")
        except:
            s = traceback.format_exc()
            logging.error(s)
        # 点击本地qq号登陆
        qq_index = conf_2.getint("Option", "qq_index")
        try:
            if (qq_index == 3):
                dr.find_element_by_xpath("//*[@id='qlogin_list']/a[1]").click()
            else:
                dr.find_element_by_xpath("//*[@id='qlogin_list']/a[3]").click()
        except:
            s = traceback.format_exc()
            logging.error(s)
        print("登录成功")

        # 刷新指定次数
        interval_time = random.randint(interval_1, interval_2)
        count = send_time
        time.sleep(interval_time)
        while (count > 0):
            print('The count is:', count)
            count = count - 1
            dr.refresh() # 刷新方法 refresh
            time.sleep(3)
            move_and_sharpness()
            print("刷新成功")
            time.sleep(interval_time)
        print("to exit browser")
        # ActionChains(dr).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
        dr.close()
        time.sleep(4)
        print("exit browser")
        dr.quit()
    except:
        s = traceback.format_exc()
        logging.error(s)
    # try:
    #     judgeprocess('chrome.exe')
    #     judgeprocess('chromedriver.exe')
    # except:
    #     s = traceback.format_exc()
    #    logging.error(s)
    del_extension = {
    '.tmp': '临时文件',
    '._mp': '临时文件_mp',
    '.log': '日志文件',
    '.gid': '临时帮助文件',
    '.chk': '磁盘检查文件',
    '.old': '临时备份文件',
    '.xlk': 'Excel备份文件',
    '.bak': '临时备份文件bak'
    }

    del_userprofile = ['cookies', 'recent', 'Temporary Internet Files', 'Temp']
    del_windir = ['prefetch', 'temp']

    # 获取系统盘
    SYS_DRIVE = os.environ['systemdrive'] + '\\'
    # 获取用户目录
    USER_PROFILE = os.environ['userprofile']
    # 获取 Windows 目录
    WIN_DIR = os.environ['windir']

    # 获取当前路径 os.getcwd()  'E:\\Software\\Python27'
    # 跳转至指定的文件目录 os.chdir('d://wamp')
    # 获取系统盘符 os.environ['systemdrive']  'C:'
    # 获取用户目录 os.environ['userprofile'] 'C:\\Users\\Administrator'
    # 获取 Windows 目录 os.environ['windir'] 'C:\\Windows'
    def del_dir_or_file(root):
        try:
            if os.path.isfile(root):
                # 删除文件
                os.remove(root)
                print( 'file: ' + root + ' removed')
            elif os.path.isdir(root):
                # 删除文件夹
                shutil.rmtree(root)
                print( 'directory: ' + root + ' removed')
        except WindowsError:
            print( 'failure: ' + root + " can't remove")

    # 字节bytes转化kb\m\g
    def formatSize(bytes):
        try:
            bytes = float(bytes)
            kb = bytes / 1024
        except:
            print("传入的字节格式不对")
            return "Error"
        if kb >= 1024:
            M = kb / 1024
            if M >= 1024:
                G = M / 1024
                return "%fG" % (G)
            else:
                return "%fM" % (M)
        else:
            return "%fkb" % (kb)

    class DiskClean(object):
        def __init__(self):
            self.del_info = {}
            self.del_file_paths = []
            self.total_size = 0
            for k,v in del_extension.items():
                self.del_info[k] = dict(name = v, count = 0)

        def scan(self):
            for roots, dirs, files in os.walk(USER_PROFILE, topdown=False):
                # 生成并展开以 root 为根目录的目录树，参数 topdown 设定展开方式从底层到顶层
                for file_item in files:
                    # 获取扩展名
                    file_extension = os.path.splitext(file_item)[1]
                    # print os.path.join(roots, file_item)
                    if file_extension in self.del_info:
                        # 文件完整路径
                        file_full_path = os.path.join(roots, file_item)
                        self.del_file_paths.append(file_full_path)
                        self.del_info[file_extension]['count'] += 1
                        self.total_size += os.path.getsize(file_full_path)

        def show(self):
            print( json.dumps(self.del_info, indent=4, ensure_ascii=False) )
            print( '删除可节省:%s 空间' % formatSize(self.total_size) )

        def delete_files(self):
            for i in self.del_file_paths:
                del_dir_or_file(i)

    if __name__ == '__main__':
        cleaner = DiskClean()
        cleaner.scan()
        cleaner.show()
        cleaner.delete_files()
    time.sleep(1)
    print("qingli wenjian ")
    # delfile( path)
    print("qingli wenjian done")
    # 切换 qq 号
    qq_interval_time = random.randint(interval_3, interval_4)
    print(qq_interval_time)
    time.sleep(qq_interval_time)
