# coding = utf-8
from selenium import webdriver
import time
import configparser  
import random

while (0 < 9):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    dr = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', options=options)    
    try:
        # print(web_site)        
        dr.get("https://egame.qq.com")    
        print("gaga")
        # dr.implicitly_wait(10)
        # print("gaga")
        dr.maximize_window()
        print("gaga")
        dr.implicitly_wait(15)
        print(dr.title)        
        dr.get(web_site)
        dr.implicitly_wait(15)
        time.sleep(5)
        #点击QQ登录
        dr.find_element_by_link_text("登录").click()
        time.sleep(5)
        #切换到iframe
        dr.switch_to.frame("_egame_login_frame_qq_")
        dr.switch_to.frame("ptlogin_iframe")
        # 点击本地qq号登陆
        dr.find_element_by_xpath("//*[@id='qlogin_list']/a[1]").click()
        # dr.find_element_by_xpath("//*[@id='qlogin_list']/a[3]").click()
        print("登录成功")
        # 刷新指定次数
        interval_time = random.randint(interval_1, interval_2)
        count = send_time
        while (count > 0):
            print('The count is:', count)
            count = count - 1
            time.sleep(interval_time)
            dr.refresh() # 刷新方法 refresh
            print("刷新成功")
        print("关闭显示器")
        dr.quit()
    except Exception as e:
        print(e)
    # 切换 qq 号
    qq_interval_time = random.randint(interval_3, interval_4)
    print(qq_interval_time)
    time.sleep(qq_interval_time)

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    dr = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', options=options)    
    try:
        print(web_site)
        dr.get("https://egame.qq.com/")
        dr.maximize_window()
        dr.implicitly_wait(15)
        print(dr.title)
        time.sleep(5)
        dr.get(web_site)
        dr.implicitly_wait(15)
        time.sleep(5)
        #点击QQ登录
        dr.find_element_by_link_text("登录").click()
        time.sleep(3)
        #切换到iframe
        dr.switch_to.frame("_egame_login_frame_qq_")
        dr.switch_to.frame("ptlogin_iframe")
        # 点击本地qq号登陆
        # dr.find_element_by_xpath("//*[@id='qlogin_list']/a[1]").click()
        dr.find_element_by_xpath("//*[@id='qlogin_list']/a[3]").click()
        print("登录成功")
        # 刷新指定次数
        interval_time = random.randint(interval_1, interval_2)
        count = send_time
        while (count > 0):
            print('The count is:', count)
            count = count - 1
            time.sleep(interval_time)
            dr.refresh() # 刷新方法 refresh
            print("刷新成功")
        print("关闭显示器")
        dr.quit()
    except Exception as e:
        print(e)
