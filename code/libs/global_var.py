
import tftlcd


########################
# 构建1.5寸LCD对象并初始化
########################
global LCD
LCD = tftlcd.LCD15(portrait=1) #默认方向竖屏

global UI_Change
UI_Change = 1

def display_tutorial(pic):
    
    LCD.Picture(0,0,pic)