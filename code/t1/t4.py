import json

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
def getHeight(head: int = 24, row: int = 0, rowHeight: int = 16):
    fixedHeight = head + rowHeight * row
    return fixedHeight


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


# 最多能显示的行数
screenHeight = 240
titleHeight = 24
rowHeight = 16
rowCount = (screenHeight - titleHeight) / rowHeight


def getRowOffset(second: int):
    row_offset_start = int(second / 44 * rowCount)
    row_offset_end = -1 if row_offset_start + 13 > 30 else row_offset_start + 13
    return row_offset_start, row_offset_end


if __name__ == '__main__':

    data = getDailyEpidemicData()
    for i in range(60):
        second = i
        row_offset_start, row_offset_end = getRowOffset(i)
        print("data" * 60)
        if data != None:
            for i, item in enumerate(data[row_offset_start:row_offset_end]):
                print(i, getHeight(row=i))
                print('日期', item['date'], end=":")
                print('昨日确诊新增', item['yes_confirm_add'], end=" ")
                print('昨日无症状新增', item['yes_wzz_add'])
