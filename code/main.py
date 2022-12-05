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
from machine import Pin, RTC

from libs import global_var, ap, color
from libs.urllib import urequest
from ui import daily_epidemic  # 30天疫情主题
# 导入主题
from ui import default  # 默认经典主题
from ui import dial  # 极简表盘主题
from ui import photo_album  # 相册主题

ui_qty = 4  # UI总数量
ui_choice = 0  # 初始UI标志位

########################
# 构建1.5寸LCD对象并初始化
########################
d = global_var.LCD

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

# 启动看门狗，超时30秒。
# wdt = WDT(timeout=30000)
wdt = None


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
            d.fill(color.BLACK)
            d.printStr('Connecting...', 10, 50, color.RED, size=2)
            d.printStr(info['SSID'], 10, 110, color.WHITE, size=2)
            d.printStr('Press KEY 5s RESET!', 5, 180, color.BLUE, size=2)
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


# 记录天气爬虫次数，用于调试
total = 0
lost = 0


# 网页获取天气数据
def weather_get(datetime):
    global weather, lost, total, city
    for tryCount in range(5):  # 失败会重试，最多5
        a = False
        b = False
        c = False
        myURL = urequest.urlopen("http://www.weather.com.cn/weather1d/" + city[1] + ".shtml")
        gc.collect()  # 内存回收
        for i in range(30):  # 假设有30段数据
            try:
                text = myURL.read(7500).decode('utf-8')  # 抓取约前4W个字符，节省内存。

                # 获取当日天气、高低温
                info1 = re.search('id="hidden_title" value="(.*?)°C', text)
                if info1 != None:
                    print("获取当日天气、高低温" + info1.group(0))
                    text1 = info1.group(1)
                    if weather[0] == '':
                        weather[0] = text1.split()[2]  # 当日天气
                    if weather[1] == '':
                        weather[1] = str(min(list(map(int, text1.split()[3].split('/')))))  # 当天最低温
                    if weather[2] == '':
                        weather[2] = str(max(list(map(int, text1.split()[3].split('/')))))  # 当天最高温
                    a = True
                # 获取实时天气
                info2 = re.search('var hour3data=(.*?)\n', text)
                if info2 != None:
                    gc.collect()  # 内存回收
                    print("获取实时天气" + info2.group(0))
                    text2 = json.loads(info2.group(1))
                    for i in range(len(text2['1d'])):
                        if int(text2['1d'][i].split(',')[0].split('日')[0]) == datetime[2]:  # 日期相同
                            if datetime[4] <= int(text2['1d'][i].split(',')[0].split('日')[1].split('时')[0]):  # 小时
                                if i == 0 or datetime[4] == int(
                                        text2['1d'][i].split(',')[0].split('日')[1].split('时')[0]):
                                    weather[3] = text2['1d'][i].split(',')[2]  # 实时天气
                                else:
                                    weather[3] = text2['1d'][i - 1].split(',')[2]  # 实时天气
                                break
                    b = True

                # 获取实时空气质量、风向风力、温湿度
                info3 = re.search('var observe24h_data = (.*?);', text)
                if info3 != None:
                    gc.collect()  # 内存回收
                    print("获取实时空气质量、风向风力、温湿度" + info3.group(0))
                    text3 = json.loads(info3.group(1))
                    od_data = text3['od']['od2']
                    for i in range(len(od_data)):
                        weather[4] = od_data[i]['od28']  # 空气质量
                        weather[5] = od_data[i]['od24']  # 实时风向
                        weather[6] = od_data[i]['od25']  # 实时风力级数
                        weather[8] = od_data[i]['od27']  # 相对湿度
                        weather[7] = od_data[i]['od22']  # 温度
                    c = True

                total = total + 1
                if a and b and c:
                    return None
                else:
                    raise Exception("没结束")

            except Exception as e:
                print(e)
                print("Can not get weather!", i)
                lost = lost + 1
                gc.collect()  # 内存回收

        time.sleep_ms(1000)


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
    print('total:', total)
    print('lost:', lost)


# 获取城市信息
def city_get():
    global city

    # 获取城市编码
    with open('wifi.txt', 'r') as f:
        info = json.loads(f.read())
        f.close()

        city[0] = info['CITY']
        city[2] = getIdCardCode(city[0])

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


def getDailyEpidemicData(adCode: str = '440100'):
    gc.collect()  # 内存回收
    r = urequest.urlopen(
        r"https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?limit=1&adCode=" + adCode)  # 发get请求
    text = r.read(444).decode('utf-8')  # 抓取约前4W个字符，节省内存。
    print(text)
    info = json.loads(text)
    if info['ret'] == 0:
        return info['data'][0]
    else:
        return None


def epidemic_situation_get():
    global weather, city
    data = getDailyEpidemicData(city[2])
    weather[9] = str(data['yes_confirm_add'])
    weather[10] = str(data['yes_wzz_add'])


def feedDog():
    global wdt
    if wdt is not None:
        wdt.feed()  # 喂狗


################
#    主程序    #
################
if __name__ == '__main__':
    # 没有WiFi配置文件,出厂模式
    while 'wifi.txt' not in os.listdir():
        ap.startAP()  # 启动AP配网模式

    # 连接WiFi
    while not WIFI_Connect():  # 等待wifi连接
        pass

    feedDog()  # 喂狗

    # 获取城市名称和编码
    d.fill(color.BLACK)
    d.printStr('Getting...', 10, 60, color.RED, size=3)
    d.printStr('City Data', 10, 120, color.WHITE, size=3)
    city_get()
    feedDog()  # 喂狗
    # 同步网络时钟
    d.fill(color.BLACK)
    d.printStr('Getting...', 10, 60, color.RED, size=3)
    d.printStr('Date & Time', 10, 120, color.WHITE, size=3)
    ntp_get()
    feedDog()  # 喂狗

    # 同步天气信息
    d.fill(color.BLACK)
    d.printStr('Getting...', 10, 60, color.RED, size=3)
    d.printStr('Weather Data', 10, 120, color.WHITE, size=3)
    weather_get(rtc.datetime())
    feedDog()  # 喂狗

    # 获取疫情新增人数信息
    d.fill(color.BLACK)
    d.printStr('Getting...', 10, 60, color.RED, size=3)
    d.printStr('Epidemic Situation', 10, 120, color.WHITE, size=3)
    d.printStr('Data', 10, 180, color.WHITE, size=3)
    epidemic_situation_get()
    feedDog()  # 喂狗

    # 信息打印
    info_print()

    tick = 61  # 每秒刷新标志位
    while True:
        # 获取时间
        datetime = rtc.datetime()

        # 30分钟在线获取一次天气信息,顺便检测wifi是否掉线
        if datetime[5] % 30 == 0 and datetime[6] == 0:
            WIFI_Connect()  # 检查WiFi，掉线的话自动重连
            weather_get(datetime)  # 获取天气信息
            epidemic_situation_get()  # 获取疫情信息
            info_print()  # 打印相关信息

        # 每秒刷新一次UI
        if tick != datetime[6]:
            tick = datetime[6]
            feedDog()  # 喂狗
            if ui_choice == 0:
                daily_epidemic.UI_Display(city, weather, datetime)  # 30天疫情
            elif ui_choice == 1:
                default.UI_Display(city, weather, datetime)  # 默认UI
            elif ui_choice == 2:
                dial.UI_Display(datetime)  # 极简表盘
            elif ui_choice == 3:
                photo_album.UI_Display(datetime)  # 相册主图

        # print('gc2:',gc.mem_free()) #内存监测

        time.sleep_ms(200)
