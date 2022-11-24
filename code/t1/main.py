'''
实验名称：Socket通信
版本：v1.0
日期：2022.5
作者：01Studio
说明：通过Socket编程实现pyController与电脑服务器助手建立TCP连接，相互收发数据。
'''
import gc
import json

# 导入相关模块
import network
import time
from libs.urllib import urequest
from machine import Pin, RTC
from tftlcd import LCD15

# 定义常用颜色
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

########################
# 构建1.5寸LCD对象并初始化
########################
d = LCD15(portrait=1)  # 默认方向竖屏

# 填充白色
d.fill(WHITE)


# WIFI连接函数
def WIFI_Connect():
    WIFI_LED = Pin(2, Pin.OUT)  # 初始化WIFI指示灯
    wlan = network.WLAN(network.STA_IF)  # STA模式
    wlan.active(True)  # 激活接口
    start_time = time.time()  # 记录时间做超时判断

    if not wlan.isconnected():
        print('Connecting to network...')
        f = open('wifi.txt', 'r')  # 获取账号密码
        info = json.loads(f.read())
        f.close()

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
    # 显示IP信息
    d.printStr('IP/Subnet/GW:', 10, 10, color=BLUE, size=2)
    d.printStr(wlan.ifconfig()[0], 10, 50, color=WHITE, size=2)
    d.printStr(wlan.ifconfig()[1], 10, 80, color=WHITE, size=2)
    d.printStr(wlan.ifconfig()[2], 10, 110, color=WHITE, size=2)
    return True


# 记录天气爬虫次数，用于调试
total = 0
lost = 0


# 网页获取天气数据
def weather_get(datetime):
    global lost, total

    for i in range(5):  # 失败会重试，最多5次

        try:

            myURL = urequest.urlopen(
                "https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?adCode=440100&limit=1")
            text = myURL.read(39000 + 100 * i).decode('utf-8')  # 抓取约前4W个字符，节省内存。

            # 获取当日天气、高低温
            # text1 = json.loads(text)
            print(text)
            total = total + 1

            return None

        except:

            print("Can not get weather!", i)
            lost = lost + 1
            gc.collect()  # 内存回收

        time.sleep_ms(1000)


# 判断WIFI是否连接成功
if WIFI_Connect():
    # 构建RTC时钟对象
    rtc = RTC()
    weather_get(rtc.datetime())
    # 开启RTOS定时器，编号为-1,周期300ms，执行socket通信接收任务
    # tim = Timer(-1)
    # tim.init(period=300, mode=Timer.PERIODIC, callback=Socket_fun)
