import json
import re
import traceback

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


'''
天气信息:
[0]当日天气,[1]当日最高温,[2]当日最低温,[3]实时天气,[4]实时空气质量,[5]实时风向,[6]实时风力级数,[7]实时温度,[8]实时湿度,[9]昨日确诊新增,[10]昨日无症状新增
'''
weather = [''] * 11
# 记录天气爬虫次数，用于调试
total = 0
lost = 0
'''
城市信息:
[0]城市，[1]天气编码，[2]身份证编码
'''
city = ['广州', '101280101', '440100']


def weather_get(datetime):
    global weather, lost, total, city

    for i in range(5):  # 失败会重试，最多5次

        try:

            myURL = requests.get("http://www.weather.com.cn/weather1d/" + city[1] + ".shtml")
            myURL.encoding = 'utf-8'
            text = myURL.text  # 抓取约前4W个字符，节省内存。
            # 获取当日天气、高低温
            text1 = re.search('id="hidden_title" value="' + '(.*?)' + '°C', text).group(1)
            weather[0] = text1.split()[2]  # 当日天气
            weather[1] = str(min(list(map(int, text1.split()[3].split('/')))))  # 当天最低温
            weather[2] = str(max(list(map(int, text1.split()[3].split('/')))))  # 当天最高温

            # 获取实时天气
            text2 = json.loads(re.search('var hour3data=(.+)\n', text).group(1))
            for i in range(len(text2['1d'])):
                if int(text2['1d'][i].split(',')[0].split('日')[0]) == datetime[2]:  # 日期相同
                    if datetime[4] <= int(text2['1d'][i].split(',')[0].split('日')[1].split('时')[0]):  # 小时
                        if i == 0 or datetime[4] == int(text2['1d'][i].split(',')[0].split('日')[1].split('时')[0]):
                            weather[3] = text2['1d'][i].split(',')[2]  # 实时天气
                        else:
                            weather[3] = text2['1d'][i - 1].split(',')[2]  # 实时天气
                        break

            # 获取实时空气质量、风向风力、温湿度
            text3 = json.loads(re.search('var\sobserve24h_data\s=\s' + '(.*?)' + ';', text).group(1))
            for i in range(len(text3['od']['od2'])):
                weather[4] = text3['od']['od2'][i]['od28']  # 空气质量
                if weather[4] != '':
                    break

            for i in range(len(text3['od']['od2'])):
                weather[5] = text3['od']['od2'][i]['od24']  # 实时风向
                if weather[5] != '':
                    break

            for i in range(len(text3['od']['od2'])):
                weather[6] = text3['od']['od2'][i]['od25']  # 实时风力级数
                if weather[6] != '':
                    break

            for i in range(len(text3['od']['od2'])):
                weather[8] = text3['od']['od2'][i]['od27']  # 相对湿度
                if weather[8] != '':
                    break

            for i in range(len(text3['od']['od2'])):
                weather[7] = text3['od']['od2'][i]['od22']  # 温度
                if weather[7] != '':
                    break

            total = total + 1
            return None
        except:
            traceback.print_exc()
            print("Can not get weather!", i)
            lost = lost + 1


def info_print():
    global city, weather

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


if __name__ == '__main__':
    data = weather_get((2022, 12, 5, 0, 10, 40, 9, 239427))
    info_print()
