import json
import math

import requests


# adcode: "440100"
# city: "广州"
# 全省确诊 confirm: 19392
# 全省确诊新增 confirm_add: "1129"
# date: "11.27"
# 死亡 dead: 0
# 治愈 heal: 0
# is_show_wzz_add: 1
# suspect: 0
# 本日新增 today_confirm_add: 0
# 本日无症状新增 today_wzz_add: 0
# y: "2022"
# 昨日确诊新增 yes_confirm_add: 1129
# 昨日无症状新增 yes_wzz_add: 7166


def getDailyEpidemicData(adCode: str = '440100'):
    url = "https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list"
    data = {'adCode': adCode, 'limit': '30'}
    r = requests.get(url, params=data)  # 发get请求
    print(len(r.text))
    print(r.json())  # 将返回的json串转为字典
    info = json.loads(r.text)
    if info['ret'] == 0:
        return info['data']
    else:
        return None


class HeightCalculator():
    def __init__(self):
        # 屏幕高度
        self.screenHeight = 240
        # 标题高度
        self.titleHeight = 24
        # 每行数据高度
        self.rowHeight = 16
        # 一屏幕能显示数据的行数
        self.rowCount = math.floor((self.screenHeight - self.titleHeight) / self.rowHeight)
        # 多少秒触发一次数据移动
        self.triggerSecond = 5
        # 一分钟内数据能移动的次数
        self.numberOfMoves = math.floor(60 / self.triggerSecond)
        # 数据条数
        self.numberOfData = 30
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


if __name__ == '__main__':
    heightCalculator = HeightCalculator()
    # data2 = [i for i in range(heightCalculator.numberOfData)]
    # for i in range(60):
    #     row_offset_start, row_offset_end = heightCalculator.getRowOffset(i)
    #     if data2 != None:
    #         print("*" * 60, "起点=", str(row_offset_start), "终点=", str(row_offset_end))
    #         print(data2[row_offset_start:row_offset_end])
    #         for item in data2[row_offset_start:row_offset_end]:
    #             print(item)

    data = getDailyEpidemicData()
    for i in range(60):
        second = i
        row_offset_start, row_offset_end = heightCalculator.getRowOffset(i)
        print("*" * 60)
        if data != None:
            for i, item in enumerate(data[row_offset_start:row_offset_end]):
                # print(i, heightCalculator.getHeight(row=i))
                print('日期', item['date'], end=":")
                print('昨日确诊新增', item['yes_confirm_add'], end=" ")
                print('昨日无症状新增', item['yes_wzz_add'])
