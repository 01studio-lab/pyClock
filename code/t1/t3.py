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
def getDailyEpidemicData(adCode: str = '440100'):
    url = "https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list"
    data = {'adCode': adCode, 'limit': '1'}
    r = requests.get(url, params=data)  # 发get请求
    print(r.json())  # 将返回的json串转为字典
    info = json.loads(r.text)
    if info['ret'] == 0:
        return info['data'][0]
    else:
        return None


if __name__ == '__main__':
    data = getDailyEpidemicData()
    print(data)
    # 昨日确诊新增 yes_confirm_add: 1129
    # 昨日无症状新增 yes_wzz_add: 7166
    print('昨日确诊新增', data['yes_confirm_add'])
    print('昨日无症状新增', data['yes_wzz_add'])
