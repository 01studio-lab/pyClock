'''
实验名称：1.5寸LCD液晶显示屏(240x240)
版本：v1.0
日期：2022.4
作者：01Studio
实验平台：pyController
说明：通过编程实现LCD的各种显示功能，包括填充、画点、线、矩形、圆形、显示英文、显示图片等。
'''

#导入相关模块
from tftlcd import LCD15
import time
from data.Fonts import fonts
import gc
#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

########################
# 构建1.5寸LCD对象并初始化
########################
d = LCD15(portrait=1) #默认方向竖屏
gc.collect()
def printChinese(text, x, y, color=(0, 0, 0), backcolor=(255, 255, 255), size=1):
    font_size = [0, 16, 24, 32, 40, 48]  # 分别对应size=1,2,3,4,5的字体尺寸，0无效。

    chinese_dict = {}

    # 获取对应的字模
    if size == 1:
        chinese_dict = fonts.hanzi_16x16_dict

    elif size == 2:
        chinese_dict = fonts.hanzi_24x24_dict

    elif size == 3:
        chinese_dict = fonts.hanzi_32x32_dict

    elif size == 4:
        chinese_dict = fonts.hanzi_40x40_dict

    elif size == 5:
        chinese_dict = fonts.hanzi_48x48_dict

    xs = x
    ys = y

    # 定义字体颜色,RGB888转RGB565
    fc = ((color[0] >> 3) << 11) + ((color[1] >> 2) << 5) + (color[2] >> 3)  # 字体
    bc = ((backcolor[0] >> 3) << 11) + ((backcolor[1] >> 2) << 5) + (backcolor[2] >> 3)  # 字体背景颜色

    for i in range(0, len(text)):

        ch_buf = chinese_dict[text[i]]  # 汉子对应码表

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

        d.write_buf(bytearray(rgb_buf), xs, y, font_size[size], font_size[size])

        xs += font_size[size]

#填充白色
d.fill(BLACK)

#写字符,4种尺寸

printChinese('确诊新增', 160, 176, color=WHITE, backcolor=BLACK, size=1)  # 清除显示残留
d.printStr('12', 160, 192, WHITE, size=1)
printChinese('无症状新增', 160, 208, color=WHITE, backcolor=BLACK, size=1)
d.printStr('13', 160, 224, WHITE, size=1)



