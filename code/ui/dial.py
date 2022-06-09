'''
实验名称：UI1
版本：v1.0
日期：2022.5
作者：CaptainJackey
说明：极简时钟
'''

#导入相关模块
import time,math
from libs import global_var

########################
# 构建1.5寸LCD对象并初始化
########################
d = global_var.LCD

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

def background():#画出表盘
    
    d.drawCircle(120, 120, 100, BLUE, border=5)
    for i in range(12):
        
        x0 = 120+round(95*math.sin(math.radians(i*30)))
        y0 = 120-round(95*math.cos(math.radians(i*30)))
        x1 = 120+round(85*math.sin(math.radians(i*30)))
        y1 = 120-round(85*math.cos(math.radians(i*30)))
        d.drawLine(x0, y0, x1, y1, WHITE)
    
def datetime_display(datetime):
    
    second = datetime[6]
    minute = datetime[5]
    hour = datetime[4]
    
    #秒钟处理
    
    #清除上一帧
    x0 = 120+round(80*math.sin(math.radians(second*6-6)))
    y0 = 120-round(80*math.cos(math.radians(second*6-6)))
    d.drawLine(x0, y0, 120, 120, BLACK)
    
    #显示
    x1 = 120+round(80*math.sin(math.radians(second*6)))
    y1 = 120-round(80*math.cos(math.radians(second*6)))
    d.drawLine(x1, y1, 120, 120, WHITE)
    
    #分钟处理
    
    #清除上一帧
    x0 = 120+round(65*math.sin(math.radians(minute*6-6)))
    y0 = 120-round(65*math.cos(math.radians(minute*6-6)))
    d.drawLine(x0, y0, 120, 120, BLACK)
    
    #显示
    x1 = 120+round(65*math.sin(math.radians(minute*6)))
    y1 = 120-round(65*math.cos(math.radians(minute*6)))
    d.drawLine(x1, y1, 120, 120, GREEN)
        
    #时钟处理

    #清除上一帧
    x0 = 120+round(55*math.sin(math.radians(hour*30+int(minute/12)*6-6)))
    y0 = 120-round(55*math.cos(math.radians(hour*30+int(minute/12)*6-6)))
    d.drawLine(x0, y0, 120, 120, BLACK)
    
    #显示
    x1 = 120+round(55*math.sin(math.radians(hour*30+int(minute/12)*6)))
    y1 = 120-round(55*math.cos(math.radians(hour*30+int(minute/12)*6)))
    d.drawLine(x1, y1, 120, 120, RED)

#显示图片
def UI_Display(datetime):
    
    if global_var.UI_Change: #首次画表盘
        
        global_var.UI_Change = 0        
        d.fill(BLACK) #清屏
        background()        

    
    datetime_display(datetime)