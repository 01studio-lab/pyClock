'''
实验名称：疫情30天滚动信息
版本：v1.0
日期：2022.12
作者：Kyle Luo
说明：查询近30天疫情数据，轮播
'''
import gc
import json
import math

from libs import global_var
from libs.color import RED, BLACK, WHITE, getRandomColor
from libs.tool import printChinese
from libs.urllib import urequest

# 导入相关模块

########################
# 构建1.5寸LCD对象并初始化
########################
d = global_var.LCD

# 数据限制
limit = 15

class HeightCalculator():
    def __init__(self):
        global limit
        # 屏幕高度
        self.screenHeight = 240
        # 标题高度
        self.titleHeight = 16
        # 每行数据高度
        self.rowHeight = 16
        # 一屏幕能显示数据的行数
        self.rowCount = math.floor((self.screenHeight - self.titleHeight) / self.rowHeight)
        # 多少秒触发一次数据移动
        self.triggerSecond = 5
        # 一分钟内数据能移动的次数
        self.numberOfMoves = math.floor(60 / self.triggerSecond)
        # 数据条数
        self.numberOfData = limit
        # 移动距离
        self.movingDistance = math.ceil((self.numberOfData - self.rowCount) / self.numberOfMoves)
        # 移动速度
        self.movingSpeed = self.movingDistance / self.triggerSecond

    def getRowOffset(self, second: int):
        offset = math.floor(second * self.movingSpeed)
        if offset - 1 < 0:
            offset = 0
        if offset > self.numberOfData:
            offset = self.numberOfData - 1
        row_offset_start = offset
        row_offset_end = None if row_offset_start + self.rowCount > self.numberOfData else row_offset_start + self.rowCount
        return row_offset_start, row_offset_end

    def getHeight(self, row: int = 0):
        fixedHeight = self.titleHeight + self.rowHeight * row
        return fixedHeight


data = []


def getDailyEpidemicData(adCode: str = '440100', limit: int = 30):
    gc.collect()
    r = urequest.urlopen(
        r"https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?limit=" + str(
            limit) + "&adCode=" + adCode)  # 发get请求
    text = r.read(7000).decode('utf-8')  # 抓取约前4W个字符，节省内存。
    info = json.loads(text)
    if info['ret'] == 0:
        gc.collect()
        return info['data']
    else:
        return None


# 用于显示动画
second2 = 61
heightCalculator = HeightCalculator()


def message_display(second):
    global data, heightCalculator
    if data != None:
        d.fill(BLACK)  # 清屏
        printTitle()
        row_offset_start, row_offset_end = heightCalculator.getRowOffset(second)
        for i, item in enumerate(data[row_offset_start:row_offset_end]):
            height = heightCalculator.getHeight(row=i)
            d.printStr(item['date'], 0, height, WHITE, size=1)
            d.printStr(str(item['yes_confirm_add']), 72, height, RED, size=1)
            d.printStr(str(item['yes_wzz_add']), 144, height, RED, size=1)


def printTitle():
    printChinese('日期', 0, 0, color=getRandomColor(), backcolor=BLACK, size=1)
    printChinese('确诊', 72, 0, color=getRandomColor(), backcolor=BLACK, size=1)
    printChinese('无症状', 144, 0, color=getRandomColor(), backcolor=BLACK, size=1)


def UI_Display(city, weather, datetime):
    global second2, data, limit
    if global_var.UI_Change:  # 首次画表盘
        global_var.UI_Change = 0
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
        data = getDailyEpidemicData(city[2], limit)
        # 更新最新的疫情信息
        if data is not None and data[-1] is not None:
            weather[9] = str(data[-1]['yes_confirm_add'])
            weather[10] = str(data[-1]['yes_wzz_add'])
