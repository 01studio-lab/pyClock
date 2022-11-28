import re

def getIdCardCode(cityName: str):
    city = None
    with open('D:\python\pyClock\code\data\IdCard.txt', 'r') as f:
        while True:
            text = f.readline()
            if cityName in text:
                city = re.match(r'"(.+?)"', text.split(':')[1]).group(1)  # "获取城市编码"
                break
            elif '}' in text:  # 结束，没这个城市。
                print('No City Name!')
                break
    return city


if __name__ == '__main__':
    print(getIdCardCode("广州"))
