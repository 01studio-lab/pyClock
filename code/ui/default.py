'''
实验名称：UI0（主界面）
版本：v1.0
日期：2022.4
作者：CaptainJackey
说明：天气时钟信息
'''

#导入相关模块
import time,gc,json
from libs import global_var
from data.Fonts import fonts

#动态信息显示
message_num = 0

########################
# 构建1.5寸LCD对象并初始化
########################
d = global_var.LCD
# d = tftlcd.LCD15(portrait=1)

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
DEEPGREEN = (1,179,105)

#空气质量颜色
YOU = (156,202,127) #优
LIANG = (249,218,101) #良 
QINGDU = (242,159,57) #轻度
ZHONGDU = (219,85,94) #中度
ZDU = (186,55,121) #重度
YANZHONG = (136,11,32) #严重

week_list=['一','二','三','四','五','六','日']

air_quality=['优','良','轻度','中度','重度','严重']



#中文显示
def printChinese(text,x,y,color=(0,0,0),backcolor=(255,255,255),size=1):
    
    font_size = [0,16,24,32,40,48] #分别对应size=1,2,3,4,5的字体尺寸，0无效。
    
    chinese_dict = {}
    
    #获取对应的字模
    if size==1:
        chinese_dict = fonts.hanzi_16x16_dict
        
    elif size==2:
        chinese_dict = fonts.hanzi_24x24_dict
        
    elif size==3:
        chinese_dict = fonts.hanzi_32x32_dict
        
    elif size==4:
        chinese_dict = fonts.hanzi_40x40_dict
        
    elif size==5:
        chinese_dict = fonts.hanzi_48x48_dict    
    
    xs = x
    ys = y
    
    #定义字体颜色,RGB888转RGB565
    fc = ((color[0]>>3)<<11) + ((color[1]>>2)<<5) + (color[2]>>3)  # 字体
    bc = ((backcolor[0]>>3)<<11) + ((backcolor[1]>>2)<<5) + (backcolor[2]>>3)  # 字体背景颜色
    
    for i in range(0, len(text)):
        
        ch_buf =chinese_dict[text[i]] #汉子对应码表
        
        rgb_buf = []
        
        t1 = font_size[size] // 8
        t2 = font_size[size] % 8

        for i in range(0, len(ch_buf)):
            
            for j in range(0, 8):
                if (ch_buf[i] << j) & 0x80 == 0x00:
                    rgb_buf.append(bc & 0xff)
                    rgb_buf.append(bc >> 8)
                else:
                    rgb_buf.append(fc & 0xff)
                    rgb_buf.append(fc >> 8)

        d.write_buf(bytearray(rgb_buf),xs,y,font_size[size],font_size[size])
        
        xs += font_size[size]

#城市显示
def printCity(text,x,y,color=(0,0,0),backcolor=(255,255,255),size=2):
    
    font_size = [0,16,24,32,40,48] #分别对应size=1,2,3,4,5的字体尺寸，0无效。
    
    f = open('/data/city.txt', 'r')       
    chinese_dict = json.loads(f.read())
    f.close()   
    
    xs = x
    ys = y
    
    #定义字体颜色,RGB888转RGB565
    fc = ((color[0]>>3)<<11) + ((color[1]>>2)<<5) + (color[2]>>3)  # 字体
    bc = ((backcolor[0]>>3)<<11) + ((backcolor[1]>>2)<<5) + (backcolor[2]>>3)  # 字体背景颜色
    
    for i in range(0, len(text)):
        
        ch_buf =chinese_dict[text[i]] #汉子对应码表
        
        rgb_buf = []
        
        t1 = font_size[size] // 8
        t2 = font_size[size] % 8

        for i in range(0, len(ch_buf)):
            
            for j in range(0, 8):
                if (ch_buf[i] << j) & 0x80 == 0x00:
                    rgb_buf.append(bc & 0xff)
                    rgb_buf.append(bc >> 8)
                else:
                    rgb_buf.append(fc & 0xff)
                    rgb_buf.append(fc >> 8)

        d.write_buf(bytearray(rgb_buf),xs,y,font_size[size],font_size[size])
        
        xs += font_size[size]

'''
weather[9]:
[0]当日天气,[1]当日最高温,[2]当日最低温,[3]实时天气,[4]实时空气质量,[5]实时风向,[6]实时风力级数,[7]实时温度,[8]实时湿度,
'''    
def weather_display(city,weather):
   
    try:
        
        #城市信息,名称超出4个只显示前4个
        if len(city[0])<5:    
            #printChinese(city[0],25-(len(city[0])-2)*10,5,color=WHITE,backcolor=BLACK,size=2)
            printCity(city[0],25-(len(city[0])-2)*10,5,color=WHITE,backcolor=BLACK,size=2)
            
        else:        
            #printChinese(city[0][:4],5,5,color=WHITE,backcolor=BLACK,size=2)
            printCity(city[0][:4],5,5,color=WHITE,backcolor=BLACK,size=2)
            
    except:
        
        #如果城市中文无法显示，那么就显示城市编码。
        d.printStr(city[1],5, 5, WHITE, size=2)
        
    #空气质量
    #优[0-50],良[50-100],轻度[100-150],中度[150-200],重度[200-300],严重[300-500]
    try:
        if 0 <= int(weather[4]) < 50: #优
            d.drawRect(115, 5, 50, 24, GREEN, border=1,fillcolor=GREEN)
            printChinese('优',129,5,color=BLACK,backcolor=GREEN,size=2)
            
        elif 50 <= int(weather[4]) < 100:#良
            d.drawRect(115, 5, 50,  24, LIANG, border=1,fillcolor=LIANG)
            printChinese('良',129,5,color=BLACK,backcolor=LIANG,size=2)
            
        elif 100 <= int(weather[4]) < 150:#轻度
            d.drawRect(115, 5, 50, 24, QINGDU, border=1,fillcolor=QINGDU)
            printChinese('轻度',117,5,color=BLACK,backcolor=QINGDU,size=2)
            
        elif 150 <= int(weather[4]) < 200:#中度
            d.drawRect(115, 5, 50,  24, ZHONGDU, border=1,fillcolor=ZHONGDU)
            printChinese('中度',117,5,color=BLACK,backcolor=ZHONGDU,size=2)
            
        elif 200 <= int(weather[4]) < 300:#重度
            d.drawRect(115, 5, 50,  24, ZHONGDU, border=1,fillcolor=ZHONGDU)
            printChinese('重度',117,5,color=BLACK,backcolor=ZHONGDU,size=2)
            
        elif 300 <= int(weather[4]) <= 500:#严重
            d.drawRect(115, 5, 50,  24, YANZHONG, border=1,fillcolor=YANZHONG)
            printChinese('严重',117,5,color=BLACK,backcolor=YANZHONG,size=2)
    except:
        print("No air quality data!")
        

    #实时温度
    d.Picture(10,175,"/data/picture/default/temp.jpg")
    d.drawRect(44, 185, 48, 10, WHITE, border=2,fillcolor=BLACK)
    d.drawRect(46, 187, 25, 6, RED, border=2,fillcolor=RED)
    d.printStr('   ', 100, 177, BLACK, size=2) #消除重影
    d.printStr(weather[7], 115-len(weather[7]*5), 177, RED, size=2)
    printChinese('℃',135,177,color=WHITE,backcolor=BLACK,size=2)
    
    #实时湿度
    d.Picture(10,205,"/data/picture/default/humi.jpg")
    d.drawRect(44, 215, 48, 10, WHITE, border=2,fillcolor=BLACK)
    d.drawRect(46, 217, 30, 6, DEEPGREEN, border=2,fillcolor=DEEPGREEN)

    if weather[8] == '100':
        d.printStr(weather[8], 100, 207, DEEPGREEN, size=2)
    else:
        d.printStr('   ', 100, 207, BLACK, size=2) #消除100%的重影
        d.printStr(weather[8], 105, 207, DEEPGREEN, size=2)
    printChinese('％',135,207,color=WHITE,backcolor=BLACK,size=2)

def message_display(weather,datetime):
    
    global message_num
    
    #实时天气
    if message_num == 0:
        printChinese('       ',5,40,color=WHITE,backcolor=BLACK,size=2) #清除显示残留
        if len(weather[3])<3:#2个文字以内
            printChinese('实时天气 '+weather[3],5,40,color=WHITE,backcolor=BLACK,size=2)
        else:    
            printChinese('实时 '+weather[3],5,40,color=WHITE,backcolor=BLACK,size=2)
        
        if weather[3] == '晴':
            if  7 <= datetime[4] < 19: #白天7点~19点
                d.Picture(175,5,"/data/picture/default/weather/qing.jpg")
            else:
                d.Picture(175,5,"/data/picture/default/weather/qing_night.jpg")
            
        elif weather[3] == '阴':
            if  7 <= datetime[4] < 19: #白天7点~19点
                d.Picture(175,5,"/data/picture/default/weather/yin.jpg")
            else:
                d.Picture(175,5,"/data/picture/default/weather/yin_night.jpg")
            
        elif weather[3] == '多云':
            d.Picture(175,5,"/data/picture/default/weather/duoyun.jpg")

        elif weather[3] == '小雨':
            d.Picture(175,5,"/data/picture/default/weather/xiaoyu.jpg")
            
        elif weather[3] == '中雨':
            d.Picture(175,5,"/data/picture/default/weather/zhongyu.jpg")
            
        elif weather[3] == '大雨':
            d.Picture(175,5,"/data/picture/default/weather/dayu.jpg")

        elif weather[3] == '暴雨':
            d.Picture(175,5,"/data/picture/default/weather/dayu.jpg")

        elif weather[3] == '雷阵雨':
            d.Picture(175,5,"/data/picture/default/weather/dayu.jpg")
            
        elif weather[3] == '阵雨':
            d.Picture(175,5,"/data/picture/default/weather/zhongyu.jpg")
            
        elif weather[3] == '雾':
            d.Picture(175,5,"/data/picture/default/weather/wu.jpg")
            
        elif weather[3] == '雨夹雪':
            d.Picture(175,5,"/data/picture/default/weather/yujiaxue.jpg")
            
        elif weather[3] == '小雪':
            d.Picture(175,5,"/data/picture/default/weather/xiaoxue.jpg")

        elif weather[3] == '中雪':
            d.Picture(175,5,"/data/picture/default/weather/daxue.jpg")
            
        elif weather[3] == '大雪':
            d.Picture(175,5,"/data/picture/default/weather/daxue.jpg")
            
        elif weather[3] == '扬沙':
            d.Picture(175,5,"/data/picture/default/weather/sand.jpg")
            
        elif weather[3] == '浮尘':
            d.Picture(175,5,"/data/picture/default/weather/sand.jpg")
            
        elif weather[3] == '沙尘暴':
            d.Picture(175,5,"/data/picture/default/weather/sand.jpg")
            
        else: #未知天气
            d.Picture(175,5,"/data/picture/default/weather/no.jpg")

    #今天天气
    elif message_num == 1:
        printChinese('       ',5,40,color=WHITE,backcolor=BLACK,size=2) #清除显示残留
        if len(weather[0])<3: #2个字以内
            printChinese('今天天气 '+ weather[0],5,40,color=WHITE,backcolor=BLACK,size=2)        
        elif len(weather[0])<5: #4个字以内
            printChinese('今天 '+ weather[0],5,40,color=WHITE,backcolor=BLACK,size=2)
        elif len(weather[0])<8: #7个字以内
            printChinese(weather[0],41-(len(weather[0])-4)*12,40,color=WHITE,backcolor=BLACK,size=2)
        else:#8个字以上,显示前7个
            printChinese(weather[0][:7],5,40,color=WHITE,backcolor=BLACK,size=2) 
    #风向
    elif message_num == 2:
        printChinese('       ',5,40,color=WHITE,backcolor=BLACK,size=2) #清除显示残留
        
        if '无' in weather[5]: #无持续风向
            
            printChinese(weather[5],30,40,color=WHITE,backcolor=BLACK,size=2)
        
        else: #有风向
            
            printChinese(weather[5],30,40,color=WHITE,backcolor=BLACK,size=2)
            d.printStr(weather[6],110, 40, WHITE, size=2)
            printChinese('级',125,40,color=WHITE,backcolor=BLACK,size=2)
  
    #最高温度
    elif message_num == 3:
        printChinese('       ',5,40,color=WHITE,backcolor=BLACK,size=2) #清除显示残留
        printChinese('最低温度 ',5,40,color=WHITE,backcolor=BLACK,size=2)
        d.printStr(weather[1], 140-len(weather[1])*10, 40, WHITE, size=2)
        printChinese('℃',148,40,color=WHITE,backcolor=BLACK,size=2)
  
    #最低温度
    elif message_num == 4:
        printChinese('       ',5,40,color=WHITE,backcolor=BLACK,size=2) #清除显示残留
        printChinese('最高温度 ',5,40,color=WHITE,backcolor=BLACK,size=2)    
        d.printStr(weather[2], 140-len(weather[2])*10, 40, WHITE, size=2)
        printChinese('℃',148,40,color=WHITE,backcolor=BLACK,size=2)
        
    #动态信息显示选择
    message_num = message_num + 1
    if message_num == 5:
        message_num = 0
    
#月，日显示重影标志位
month_node = 0
day_node = 0

def datetime_display(datetime):
    
    #日期显示
    year = datetime[0]
    month = datetime[1]
    day = datetime[2]
    week = datetime[3]
    
    global month_node,day_node #月，日显示重影标志位
    
    #月显示
    if month > 9:
        d.printStr(str(month), 5, 140, WHITE, size=2)
        month_node = 1
        
    else:
        
        if month_node == 1: #月份从双位数变换到单位数
            d.printStr('  ', 5, 140, BLACK, size=2) #消除月显示重影
            month_node = 0
            
        d.printStr(str(month), 13, 140, WHITE, size=2)
        
    printChinese('月',30,140,color=WHITE,backcolor=BLACK,size=2)
    
    #日显示
    if day > 9:
        d.printStr(str(day), 55, 140, WHITE, size=2)
        day_node = 1
        
    else:
        
        if day_node == 1: #日从双位数变换到单位数
            d.printStr('  ', 55, 140, BLACK, size=2) #消除日显示重影
            day_node = 0
            
        d.printStr(str(day), 63, 140, WHITE, size=2)
        
    printChinese('日',80,140,color=WHITE,backcolor=BLACK,size=2)
    
    #周显示
    printChinese('周'+week_list[week],115,140,color=WHITE,backcolor=BLACK,size=2)
    
    #时间显示
    second = datetime[6]
    minute = datetime[5]
    hour = datetime[4]

    
    if hour > 9:
        d.printStr(str(hour), 20, 80, WHITE, size=4)
    else:
        d.printStr('0'+str(hour), 20, 80, WHITE, size=4)
    
    d.printStr(':', 68, 80, WHITE, size=4)
    
    if minute > 9:
        d.printStr(str(minute), 92, 80, YELLOW, size=4)
    else:
        d.printStr('0'+str(minute), 92, 80, YELLOW, size=4)
        
    d.printStr(':', 140, 80, WHITE, size=4)
    
    if second > 9:
        d.printStr(str(second), 164, 80, WHITE, size=4)
    else:
        d.printStr('0'+str(second), 164, 80, WHITE, size=4)

#用于显示动画
second2 = 61

#显示图片
def UI_Display(city,weather,datetime):
    
    global second2,message_num
    
    if global_var.UI_Change: #首次显示
        
        global_var.UI_Change = 0
        message_num = 0
        
        d.fill(BLACK) #清屏        
        weather_display(city,weather)
        message_display(weather,datetime)

    datetime_display(datetime)

    #logo动态显示
    if second2 != datetime[6]:
        if gc.mem_free() < 15000: #内存不足
            gc.collect() #回收内存
        d.Picture(165,165,"/data/picture/default/"+str(datetime[6]%4+1)+".jpg")
        second2 = datetime[6]
        
    #动态信息显示刷新时间5秒
    if datetime[6]%5 == 0: 
        
        message_display(weather,datetime)
    
    #天气信息显示刷新时间10分钟
    if datetime[5]%10 == 0 and datetime[6]==0:
        
        weather_display(city,weather)
