
# -*- coding: utf-8 -*-
"""
@author: Yinan

常用站点cookies： 
                 宁德：%u5B81%u5FB7%2CNES
                 福州：%u798F%u5DDE%2CFZS
                 云霄：%u4E91%u9704%2CYBS
                 漳州：%u6F33%u5DDE%2CZUS
                 南平：%u5357%u5E73%2CNPS

"""

from splinter.browser import Browser
from time import sleep
import traceback
import getpass

#设置站点字典
station_name = {"宁德":"%u5B81%u5FB7%2CNES",
                 "福州":"%u798F%u5DDE%2CFZS",
                 "云霄":"%u4E91%u9704%2CYBS",
                 "漳州":"%u6F33%u5DDE%2CZUS",
                 "南平":"%u5357%u5E73%2CNPS"}

# 用户名，密码
username = u"qw5653382"
passwd = u"jyn5669569"
# cookies值
starts = station_name['宁德']
ends = station_name['福州']
# 时间格式2016-12-22
dtime = u"2016-12-23"
# 车次，选择第几趟，0则从上之下依次点击
order = 17
###乘客名
pa = u"江益楠"

"""网址"""
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
login_url = "https://kyfw.12306.cn/otn/login/init"
initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"



def login():
    b.find_by_text(u"登录").click()
    sleep(1)
    b.fill("loginUserDTO.user_name", username)
    sleep(1)
    b.fill("userDTO.password", passwd)
    sleep(1)
    print u"等待验证码，自行输入..."
    while True:
        if b.url != initmy_url:
            sleep(1)
        else:
            break

def huoche():
    global b
    b = Browser(driver_name="chrome")
    b.visit(ticket_url)

    while b.is_text_present(u"登录"):
        sleep(1)
        login()
        if b.url == initmy_url:
            break

    try:
        print u"购票页面..."
        # 跳回购票页面
        b.visit(ticket_url)

        # 加载查询信息
        b.cookies.add({"_jc_save_fromStation": starts})
        b.cookies.add({"_jc_save_toStation": ends})
        b.cookies.add({"_jc_save_fromDate": dtime})
        b.reload()

        sleep(2)

        count = 0
        # 循环点击预订
        if order != 0:
            while b.url == ticket_url:
                b.find_by_text(u"查询").click()
                count +=1
                print u"循环点击查询... 第 %s 次" % count
                sleep(1)
                try:
                    b.find_by_text(u"预订")[order - 1].click()
                except:
                    print u"还没开始预订"
                    continue
        else:
            while b.url == ticket_url:
                b.find_by_text(u"查询").click()
                count += 1
                print u"循环点击查询... 第 %s 次" % count
                sleep(1)
                try:
                    for i in b.find_by_text(u"预订"):
                        i.click()
                except:
                    print u"还没开始预订"
                    continue
        sleep(1)
        b.find_by_text(pa)[1].click()
        #b.find_by_text(u"提交订单").click()
        sleep(1)
        b.find_by_id('qr_submit_id').click()
        print  u"能做的都做了.....不再对浏览器进行任何操作"
    except Exception as e:
        print(traceback.print_exc())

if __name__ == "__main__":
    huoche()
