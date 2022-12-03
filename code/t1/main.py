'''
实验名称：pyClock天气时钟-出厂例程
版本：v1.0
日期：2022.5
作者：01Studio
'''

import gc
# 导入相关模块
import json
import os
import re
import time

import machine
import network
import ntptime
from machine import Pin, RTC, WDT

from libs import global_var, ap
from libs.urllib import urequest
# 导入主题
from ui import default  # 默认经典主题
from ui import dial  # 极简表盘主题
from ui import photo_album  # 相册主题

ui_qty = 3  # UI总数量
ui_choice = 0  # 初始UI标志位

########################
# 构建1.5寸LCD对象并初始化
########################
d = global_var.LCD

# 定义常用颜色
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
DEEPGREEN = (1, 179, 105)

'''
城市信息:
[0]城市，[1]天气编码，[2]身份证编码
'''
city = ['', '', '']

'''
天气信息:
[0]当日天气,[1]当日最高温,[2]当日最低温,[3]实时天气,[4]实时空气质量,[5]实时风向,[6]实时风力级数,[7]实时温度,[8]实时湿度,[9]昨日确诊新增,[10]昨日无症状新增
'''
weather = [''] * 11  # 定义一个长度为9的字符列表

# 构建RTC时钟对象
rtc = RTC()

# 初始化WIFI指示灯
WIFI_LED = Pin(2, Pin.OUT)


# WIFI连接函数
def WIFI_Connect():
    wlan = network.WLAN(network.STA_IF)  # STA模式
    wlan.active(True)  # 激活接口
    start_time = time.time()  # 记录时间做超时判断

    if not wlan.isconnected():

        print('Connecting to network...')

        with open('wifi.txt', 'r') as f:  # 获取账号密码
            info = json.loads(f.read())
            print(info)
            d.fill(BLACK)
            d.printStr('Connecting...', 10, 50, RED, size=2)
            d.printStr(info['SSID'], 10, 110, WHITE, size=2)
            d.printStr('Press KEY 5s RESET!', 5, 180, BLUE, size=2)
            wlan.connect(info['SSID'], info['PASSWORD'])  # 输入WIFI账号密码

            while not wlan.isconnected():

                # LED闪烁提示
                WIFI_LED.value(1)
                time.sleep_ms(300)
                WIFI_LED.value(0)
                time.sleep_ms(300)

                # 超时判断,15秒没连接成功判定为超时
                if time.time() - start_time > 15:
                    wlan.active(False)
                    # 点亮LED表示没连接上WiFi
                    WIFI_LED.value(1)
                    print('WIFI Connected Timeout!')
                    return False

    # 连接成功，熄灭LED
    WIFI_LED.value(0)

    # 串口打印信息
    print('network information:', wlan.ifconfig())

    return True


# 设置NTP时间偏移量，就是我们所谓的时区，中国在UTC +8 的时区计算方式： 3155673600 - 8*3600 = 3155644800
# 3155673600 是默认的UTC，以秒计算偏移量。
ntptime.NTP_DELTA = 3155644800
ntptime.host = 'ntp1.aliyun.com'


# 获取网络时间
def ntp_get():
    for i in range(10):  # 最多尝试获取10次

        try:
            ntptime.settime()  # 获取网络时间
            print("ntp time(BeiJing): ", rtc.datetime())
            return True

        except:
            print("Can not get time!")

        time.sleep_ms(500)



# 信息打印
def info_print():
    global city, weather

    print(rtc.datetime())

    print('城市:', city[0], city[1])

    print('当日天气:', weather[0])
    print('当日最低温:', weather[1])
    print('当日最高温:', weather[2])
    print('实时天气:', weather[3])
    print('实时空气质量:', weather[4])
    print('实时风向:', weather[5])
    print('实时风力级数:', weather[6])
    print('实时温度:', weather[7])
    print('实时湿度:', weather[8])
    print('昨日确诊新增:', weather[9])
    print('昨日无症状新增:', weather[10])


# 获取城市信息
def city_get():
    global city

    # 获取城市编码
    with open('wifi.txt', 'r') as f:
        info = json.loads(f.read())
        f.close()

        city[0] = info['CITY']
        city[2] = getIdCardCode("广州")

    # 获取城市名称
    f = open('/data/CityCode.txt', 'r')
    num = 0
    while True:
        text = f.readline()
        if city[0] in text:
            if city[0] == re.match(r'"(.+?)"', text).group(1):  # 城市名称完全一样
                city[1] = re.match(r'"(.+?)"', text.split(': ')[1]).group(1)  # "获取城市编码"
                break
        elif '}' in text:  # 结束，没这个城市。
            print('No City Name!')
            break

        num = num + 1

        if num == 300:
            gc.collect()  # 内存回收
            num = 0

    f.close()
    city_node = 0

    # city.txt文件存在,判断文件是否已经有当前城市字库
    if 'city.txt' in os.listdir('/data/'):
        f = open('/data/city.txt', 'r')
        city_text = f.read()
        for i in range(len(city[0])):

            if city[0][i] in city_text:

                if i == len(city[0]) - 1:  # 全部字体都有

                    city_node = 1  # 标记字符信息正常
        f.close()

        # 城市字库正常，无需制作
    if city_node == 1:
        pass

    else:  # 获取字库文件并保存
        # 生成城市字模文件
        city_font = {}

        for i in range(len(city[0])):

            f = open('/data/Fonts/fonts_city.py', 'r')

            while True:

                text = f.readline()

                if city[0][i] in text:

                    while True:

                        text = text + f.readline()

                        if ')' in text:
                            a = re.search('[(]' + '(.*?)' + '[)]', text).group(1) \
                                .replace('\r\n', '') \
                                .replace(' ', '').split(',')

                            for j in range(len(a)):
                                a[j] = int(a[j])

                            city_font[city[0][i]] = a
                            break
                    break

                if not text:  # 读完
                    print("No City Fonts.")
                    break

            f.close()

        f = open('/data/city.txt', 'w')  # 以写的方式打开一个文件，没有该文件就自动新建
        f.write((json.dumps(city_font)))  # 写入数据
        f.close()  # 每次操作完记得关闭文件

        gc.collect()  # 内存回收


# 按键
KEY = Pin(9, Pin.IN, Pin.PULL_UP)  # 构建KEY对象


# 按键中断触发
def key(KEY):
    global ui_choice, ui_qty
    time.sleep_ms(10)  # 消除抖动
    if KEY.value() == 0:  # 确认按键被按下

        # 短按切换UI
        global_var.UI_Change = 1
        ui_choice = ui_choice + 1
        if ui_choice == ui_qty:  # UI数量
            ui_choice = 0

        # 出厂模式
        start = time.ticks_ms()
        while KEY.value() == 0:

            if time.ticks_ms() - start > 5000:  # 长按按键5秒

                WIFI_LED.value(1)  # 指示灯亮
                print("Factory Mode!")
                try:
                    os.remove('wifi.txt')
                    print('Remove wifi.txt')
                except:
                    print('no wifi.txt')

                machine.reset()  # 重启开发板。


KEY.irq(key, Pin.IRQ_FALLING)  # 定义中断，下降沿触发


def getIdCardCode(cityName: str):
    city = None
    with open('/data/IdCard.txt', 'r') as f:
        while True:
            text = f.readline()
            if cityName in text:
                city = re.match(r'"(.+?)"', text.split(':')[1]).group(1)  # "获取城市编码"
                break
            elif '}' in text:  # 结束，没这个城市。
                print('No City Name!')
                break
    return city

################
#    主程序    #
################
if __name__ == '__main__':
    # 没有WiFi配置文件,出厂模式
    while 'wifi.txt' not in os.listdir():
        ap.startAP()  # 启动AP配网模式

    # 启动看门狗，超时30秒。
    wdt = WDT(timeout=30000)

    # 连接WiFi
    while not WIFI_Connect():  # 等待wifi连接
        pass

    wdt.feed()  # 喂狗

    # 获取城市名称和编码
    d.fill(BLACK)
    d.printStr('Getting...', 10, 60, RED, size=3)
    d.printStr('City Data', 10, 120, WHITE, size=3)
    city_get()

    # 同步网络时钟
    d.fill(BLACK)
    d.printStr('Getting...', 10, 60, RED, size=3)
    d.printStr('Date & Time', 10, 120, WHITE, size=3)
    ntp_get()

    # 信息打印
    info_print()

    tick = 61  # 每秒刷新标志位

    while True:

        # 获取时间
        datetime = rtc.datetime()

        # 30分钟在线获取一次天气信息,顺便检测wifi是否掉线
        if datetime[5] % 30 == 0 and datetime[6] == 0:
            WIFI_Connect()  # 检查WiFi，掉线的话自动重连
            info_print()  # 打印相关信息

        # 每秒刷新一次UI
        if tick != datetime[6]:

            tick = datetime[6]

            wdt.feed()  # 喂狗

            if ui_choice == 0:
                pass

        time.sleep_ms(200)
