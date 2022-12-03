'''
实验名称：疫情30天滚动信息
版本：v1.0
日期：2022.12
作者：Kyle Luo
说明：查询近30天疫情数据，轮播
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
# 最多能显示的行数
screenHeight = 240
titleHeight = 24
rowHeight = 16
limit = 30
rowCount = (screenHeight - titleHeight) / rowHeight


def getRowOffset(second: int):
    global limit
    row_offset_start = int(second / 44 * rowCount)
    row_offset_end = limit if row_offset_start + 13 > limit else row_offset_start + 13
    return row_offset_start, row_offset_end


data = []


def getHeight(head: int = 24, row: int = 0, rowHeight: int = 16):
    fixedHeight = head + rowHeight * row
    return fixedHeight


def getDailyEpidemicData(adCode: str = '440100', limit: int = 30):
    gc.collect()
    r = urequest.urlopen(
        r"https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?limit=" + str(limit) + "&adCode=" + adCode)  # 发get请求
    text = r.read(7000).decode('utf-8')  # 抓取约前4W个字符，节省内存。
    info = json.loads(text)
    if info['ret'] == 0:
        return info['data']
    else:
        return None


# 用于显示动画
second2 = 61


def message_display(second):
    global data
    if data != None:
        row_offset_start, row_offset_end = getRowOffset(second)
        for i, item in enumerate(data[row_offset_start:row_offset_end]):
            height = getHeight(row=i)
            d.printStr(item['date'], 0, height, WHITE, size=1)
            d.printStr(str(item['yes_confirm_add']), 72, height, RED, size=1)
            d.printStr(str(item['yes_wzz_add']), 144, height, RED, size=1)


def printTitle():
    d.fill(BLACK)  # 清屏
    printChinese('日   ', 0, 0, color=WHITE, backcolor=BLACK, size=2)
    printChinese('确诊 ', 72, 0, color=WHITE, backcolor=BLACK, size=2)
    printChinese('无症状', 144, 0, color=WHITE, backcolor=BLACK, size=2)


def UI_Display(city, datetime):
    global second2, data, limit
    if global_var.UI_Change:  # 首次画表盘
        global_var.UI_Change = 0
        d.fill(BLACK)  # 清屏
        printTitle()
        data = getDailyEpidemicData(city[2], limit)
        message_display(datetime[6])

    # 定期回收内存
    if second2 != datetime[6]:
        if gc.mem_free() < 15000:  # 内存不足
            gc.collect()  # 回收内存
        second2 = datetime[6]

    if datetime[6] % 5 == 0:
        message_display(datetime[6])

    # 疫情刷新时间30分钟
    if datetime[5] % 30 == 0 and datetime[6] == 0:
        printTitle()
        data = getDailyEpidemicData(city[2], limit)
