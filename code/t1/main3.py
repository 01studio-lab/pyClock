'''
实验名称：1.5寸LCD液晶显示屏(240x240)
版本：v1.0
日期：2022.4
作者：01Studio
实验平台：pyController
说明：通过编程实现LCD的各种显示功能，包括填充、画点、线、矩形、圆形、显示英文、显示图片等。
'''
import gc
import json

from libs import global_var
from libs.tool import printChinese
from libs.urllib import urequest

# 导入相关模块

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

rollCount = 0
data = None


def getDailyEpidemicData(adCode: str = '440100'):
    r = urequest.urlopen(
        r"https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?limit=30&adCode=" + adCode)  # 发get请求
    text = r.read(39000).decode('utf-8')  # 抓取约前4W个字符，节省内存。
    info = json.loads(text)
    if info['ret'] == 0:
        return info['data']
    else:
        return None


# 用于显示动画
second2 = 61


def message_display(second):
    global data
    d.fill(BLACK)  # 清屏
    printChinese('日   ', 0, 0, color=WHITE, backcolor=BLACK, size=2)
    printChinese('确诊 ', 72, 0, color=WHITE, backcolor=BLACK, size=2)
    printChinese('无症状', 144, 0, color=WHITE, backcolor=BLACK, size=2)
    for i in range(len(data)):
        d.printStr(data[i]['date'], 0, 24 + 16 * i + second, WHITE, size=1)
        d.printStr(data[i]['yes_confirm_add'], 72, 24 + 16 * i + second, RED, size=1)
        d.printStr(data[i]['yes_wzz_add'], 144, 24 + 16 * i + second, RED, size=1)

if __name__=='__main__':
    global data
    data=getDailyEpidemicData()
    message_display(0)