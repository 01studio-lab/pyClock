'''
01Studio pyClock天气时钟 中文字符
'''

'''
size = 2 
24 x 24 汉字字库
宋体、阴码，逐行式，顺向（高位在前）
'''
hanzi_24x24_dict = {
    "期": (
        0x1e, 0x38, 0x0, 0x1e, 0x3b, 0xff, 0x1c, 0x3b, 0xff, 0x7f, 0xfd, 0xff, 0x7f, 0xfd, 0x87, 0x7f, 0xfd, 0x87, 0xc,
        0x39, 0x87, 0xf, 0xf9, 0xff, 0xf, 0xf9, 0xff, 0xc, 0x39, 0xff, 0xc, 0x39, 0x87, 0xf, 0xf9, 0x87, 0xf, 0xfb,
        0x87,
        0xc, 0x3b, 0xff, 0xc, 0x3b, 0xff, 0x7f, 0xff, 0xff, 0x7f, 0xff, 0x87, 0x4c, 0x67, 0x87, 0xe, 0xf7, 0x7, 0x1e,
        0x7f,
        0x7, 0x3c, 0x3e, 0xf, 0x78, 0x1e, 0x3f, 0x30, 0x1c, 0x3e, 0x0, 0x4, 0x1c,),
    # 空气质量
    "优": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x06, 0x00, 0x07, 0x06, 0x60, 0x06, 0x04, 0x30, 0x06,
           0x04, 0x30, 0x0C, 0x04, 0x00, 0x0C, 0x04, 0x00, 0x1D, 0xFF, 0xFC, 0x1D, 0xFF, 0xFC, 0x34, 0x0C,
           0x80, 0x74, 0x0C, 0x80, 0x64, 0x0C, 0x80, 0x04, 0x0C, 0x80, 0x04, 0x0C, 0x80, 0x04, 0x1C, 0x80,
           0x04, 0x18, 0x80, 0x04, 0x18, 0x80, 0x04, 0x30, 0x84, 0x04, 0x70, 0x86, 0x04, 0x60, 0xC6, 0x05,
           0xC0, 0xFC, 0x04, 0xC0, 0x38, 0x00, 0x00, 0x00),

    "良": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x10, 0x00, 0x07,
           0xFF, 0xE0, 0x06, 0x00, 0x60, 0x06, 0x00, 0x60, 0x07, 0xFF, 0xE0, 0x07, 0xFF, 0xE0, 0x06, 0x00,
           0x60, 0x06, 0x00, 0x60, 0x07, 0xFF, 0xE0, 0x07, 0xFF, 0xE0, 0x06, 0x18, 0x20, 0x06, 0x18, 0x70,
           0x06, 0x0C, 0xE0, 0x06, 0x0F, 0xC0, 0x06, 0x07, 0x00, 0x06, 0xE3, 0x80, 0x07, 0xC1, 0xF0, 0x0F,
           0x00, 0x7E, 0x0C, 0x00, 0x1C, 0x00, 0x00, 0x00),

    "轻": (0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x06, 0x00, 0x00, 0x06, 0x1F, 0xF0, 0x06, 0x1F, 0xF0, 0x7F,
           0xE0, 0x60, 0x0C, 0x00, 0xE0, 0x0C, 0x00, 0xC0, 0x0D, 0x81, 0xF0, 0x19, 0x83, 0x38, 0x19, 0x0E,
           0x1C, 0x31, 0x1C, 0x04, 0x3F, 0xE8, 0x00, 0x21, 0x00, 0x00, 0x01, 0x0F, 0xFC, 0x01, 0x00, 0xC0,
           0x01, 0xE0, 0xC0, 0x7F, 0xC0, 0xC0, 0x39, 0x00, 0xC0, 0x01, 0x00, 0xC0, 0x01, 0x00, 0xC0, 0x01,
           0x1F, 0xFE, 0x01, 0x00, 0x00, 0x01, 0x80, 0x00),

    "度": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1C, 0x00, 0x00, 0x0C, 0x00, 0x1F, 0xFF, 0xF8, 0x1F,
           0xFF, 0xF8, 0x18, 0x60, 0xC0, 0x18, 0x60, 0xC0, 0x18, 0x60, 0xC0, 0x1B, 0xFF, 0xF8, 0x18, 0x60,
           0xC0, 0x18, 0x60, 0xC0, 0x18, 0x7F, 0xC0, 0x18, 0x7F, 0xC0, 0x18, 0x00, 0x00, 0x19, 0xFF, 0xE0,
           0x18, 0x60, 0xC0, 0x18, 0x30, 0xC0, 0x10, 0x19, 0x80, 0x30, 0x1F, 0x00, 0x30, 0x0F, 0x00, 0x60,
           0xFB, 0xF8, 0x27, 0xE0, 0x7C, 0x00, 0x00, 0x00),

    "中": (0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00,
           0x18, 0x00, 0x1F, 0xFF, 0xF8, 0x1F, 0xFF, 0xF8, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18,
           0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x1F, 0xFF, 0xF8, 0x1F, 0xFF, 0xF8, 0x18, 0x18, 0x18,
           0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00,
           0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00),

    "重": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xE0, 0x1F, 0xFF, 0xF0, 0x0F, 0xF8, 0x00, 0x00,
           0x18, 0x00, 0x7F, 0xFF, 0xFE, 0x7F, 0xFF, 0xFE, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x07, 0xFF,
           0xE0, 0x06, 0x18, 0x60, 0x07, 0xFF, 0xE0, 0x07, 0xFF, 0xE0, 0x06, 0x18, 0x60, 0x07, 0xFF, 0xE0,
           0x07, 0xFF, 0xE0, 0x00, 0x18, 0x00, 0x0F, 0xFF, 0xF8, 0x0F, 0xFF, 0xF8, 0x00, 0x18, 0x00, 0x3F,
           0xFF, 0xFC, 0x3F, 0xFF, 0xFC, 0x00, 0x00, 0x00),

    "严": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0xFF, 0xFC, 0x00, 0x63, 0x00, 0x00,
           0x63, 0x00, 0x0C, 0x63, 0x30, 0x06, 0x63, 0x30, 0x06, 0x63, 0x60, 0x04, 0x63, 0x20, 0x00, 0x63,
           0x04, 0x0F, 0xFF, 0xFC, 0x08, 0x00, 0x00, 0x08, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00,
           0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x30, 0x00, 0x00, 0x30, 0x00, 0x00, 0x70,
           0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00),

    "温": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x38, 0xFF, 0xF0, 0x0C, 0x40, 0x30, 0x04,
           0x40, 0x30, 0x00, 0x7F, 0xF0, 0x00, 0x7F, 0xF0, 0x70, 0x40, 0x30, 0x38, 0x40, 0x30, 0x08, 0xFF,
           0xF0, 0x00, 0xFF, 0xF0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0xFF, 0xF8, 0x09, 0x89, 0x98,
           0x19, 0x89, 0x98, 0x19, 0x89, 0x98, 0x11, 0x89, 0x98, 0x31, 0x89, 0x98, 0x31, 0x89, 0x98, 0x67,
           0xFF, 0xFE, 0x07, 0xFF, 0xFE, 0x00, 0x00, 0x00),

    "至": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0xFF, 0xF8, 0x1F, 0xFF, 0xF8, 0x00,
           0x20, 0x00, 0x00, 0x70, 0x00, 0x00, 0xE1, 0x00, 0x00, 0xC1, 0x80, 0x01, 0x80, 0xC0, 0x07, 0x00,
           0x60, 0x0F, 0xFF, 0xF0, 0x04, 0x18, 0x10, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x08, 0x18, 0x10,
           0x0F, 0xFF, 0xF0, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x3F,
           0xFF, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),

    "最": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xFF, 0xE0, 0x06, 0x00, 0x60, 0x07,
           0xFF, 0xE0, 0x06, 0x00, 0x60, 0x06, 0x00, 0x60, 0x07, 0xFF, 0xE0, 0x00, 0x00, 0x00, 0x3F, 0xFF,
           0xFC, 0x3F, 0xFF, 0xFC, 0x0C, 0x20, 0x00, 0x0F, 0xEF, 0xF0, 0x0F, 0xEF, 0xF0, 0x0C, 0x26, 0x30,
           0x0F, 0xE2, 0x20, 0x0F, 0xE3, 0x60, 0x0C, 0x39, 0x40, 0x0F, 0xF9, 0xC0, 0x3F, 0x21, 0xF0, 0x20,
           0x27, 0x3C, 0x00, 0x3C, 0x08, 0x00, 0x00, 0x00),

    "高": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x3F, 0xFF, 0xFC, 0x00,
           0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xFF, 0xC0, 0x06, 0x00, 0x40, 0x06, 0x00, 0x40, 0x07, 0xFF,
           0xC0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF, 0xFC, 0x30, 0x00, 0x0C, 0x30, 0x00, 0x0C,
           0x31, 0xFF, 0x8C, 0x31, 0x81, 0x8C, 0x31, 0x81, 0x8C, 0x31, 0xFF, 0x8C, 0x30, 0x00, 0x0C, 0x30,
           0x00, 0x3C, 0x30, 0x00, 0x38, 0x00, 0x00, 0x00),

    "低": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x00, 0x10, 0x06, 0x01, 0xF8, 0x06, 0x7F, 0xE0, 0x0C,
           0x41, 0x00, 0x0C, 0x41, 0x00, 0x1C, 0x41, 0x00, 0x1C, 0x41, 0x00, 0x3C, 0x41, 0x00, 0x3C, 0x7F,
           0xFC, 0x6C, 0x7F, 0xFC, 0x2C, 0x41, 0x80, 0x0C, 0x41, 0x80, 0x0C, 0x41, 0x80, 0x0C, 0x40, 0x80,
           0x0C, 0x44, 0xC0, 0x0C, 0x4C, 0xC0, 0x0C, 0x5C, 0xC4, 0x0C, 0x78, 0x66, 0x0C, 0xEC, 0x36, 0x0C,
           0x46, 0x3C, 0x0C, 0x02, 0x1C, 0x00, 0x00, 0x00),

    " ": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),

    # 风力
    "东": (0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x30, 0x00, 0x00, 0x30, 0x00, 0x00, 0x60, 0x00, 0x00,
           0x60, 0x00, 0x1F, 0xFF, 0xF8, 0x01, 0xC0, 0x00, 0x01, 0x80, 0x00, 0x03, 0x0C, 0x00, 0x07, 0x0C,
           0x00, 0x0E, 0x0C, 0x00, 0x1F, 0xFF, 0xF8, 0x0F, 0xFF, 0xF8, 0x00, 0x0C, 0x00, 0x00, 0x0C, 0x00,
           0x03, 0x0C, 0x40, 0x03, 0x0C, 0xE0, 0x06, 0x0C, 0x70, 0x0C, 0x0C, 0x38, 0x18, 0x0C, 0x1C, 0x30,
           0x7C, 0x08, 0x00, 0x78, 0x00, 0x00, 0x00, 0x00),

    "南": (0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x3F, 0xFF, 0xFE, 0x30,
           0x18, 0x02, 0x00, 0x10, 0x00, 0x00, 0x30, 0x00, 0x3F, 0xFF, 0xFC, 0x30, 0x00, 0x0C, 0x30, 0x82,
           0x08, 0x30, 0xC3, 0x08, 0x30, 0x46, 0x08, 0x32, 0x06, 0x08, 0x33, 0xFF, 0xC8, 0x30, 0x18, 0x08,
           0x30, 0x18, 0x08, 0x37, 0xFF, 0xE8, 0x30, 0x18, 0x08, 0x30, 0x18, 0x08, 0x30, 0x18, 0x08, 0x30,
           0x18, 0x78, 0x30, 0x00, 0x38, 0x00, 0x00, 0x00),

    "西": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF, 0xFC, 0x3F, 0xFF, 0xFC, 0x00,
           0x66, 0x00, 0x00, 0x66, 0x00, 0x00, 0x66, 0x00, 0x0F, 0xFF, 0xF0, 0x0F, 0xFF, 0xF0, 0x08, 0x46,
           0x10, 0x08, 0x46, 0x10, 0x08, 0x46, 0x10, 0x08, 0xC6, 0x10, 0x08, 0xC6, 0x10, 0x09, 0x83, 0xD0,
           0x0B, 0x83, 0xD0, 0x09, 0x00, 0x10, 0x08, 0x00, 0x10, 0x08, 0x00, 0x10, 0x0F, 0xFF, 0xF0, 0x08,
           0x00, 0x10, 0x08, 0x00, 0x10, 0x00, 0x00, 0x00),

    "北": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC6, 0x00, 0x00, 0xC6, 0x00, 0x00, 0xC6, 0x00, 0x00,
           0xC6, 0x00, 0x00, 0xC6, 0x00, 0x00, 0xC6, 0x0C, 0x00, 0xC6, 0x1C, 0x3F, 0xC6, 0x78, 0x3F, 0xC7,
           0xE0, 0x00, 0xC7, 0x80, 0x00, 0xC6, 0x00, 0x00, 0xC6, 0x00, 0x00, 0xC6, 0x00, 0x00, 0xC6, 0x00,
           0x00, 0xC6, 0x00, 0x00, 0xC6, 0x00, 0x0F, 0xC6, 0x04, 0x7E, 0xC6, 0x06, 0x30, 0xC3, 0x0E, 0x00,
           0xC3, 0xFC, 0x00, 0xC0, 0x00, 0x00, 0x00, 0x00),

    "风": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0F, 0xFF, 0xE0, 0x0F, 0xFF, 0xE0, 0x0C, 0x00, 0x60, 0x0C,
           0x00, 0x60, 0x0C, 0x00, 0x60, 0x0C, 0x83, 0x60, 0x0D, 0xC6, 0x60, 0x0C, 0xC6, 0x60, 0x0C, 0x64,
           0x60, 0x0C, 0x3C, 0x60, 0x08, 0x38, 0x60, 0x08, 0x18, 0x60, 0x08, 0x3C, 0x60, 0x08, 0x7C, 0x60,
           0x18, 0x66, 0x20, 0x18, 0xC3, 0x30, 0x1B, 0x83, 0x34, 0x31, 0x00, 0x36, 0x30, 0x00, 0x3E, 0x70,
           0x00, 0x1E, 0x60, 0x00, 0x0C, 0x00, 0x00, 0x00),

    "级": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x06, 0x7F, 0xF0, 0x0C, 0x7F, 0xF0, 0x0C,
           0x08, 0x20, 0x18, 0xC8, 0x60, 0x31, 0x88, 0x60, 0x31, 0x88, 0x60, 0x7F, 0x08, 0x40, 0x22, 0x08,
           0xFC, 0x06, 0x0C, 0x08, 0x0C, 0x0C, 0x18, 0x18, 0x1E, 0x18, 0x3F, 0x9A, 0x10, 0x3F, 0x9B, 0x30,
           0x20, 0x11, 0xB0, 0x00, 0xB1, 0xE0, 0x0F, 0xA0, 0xE0, 0x3E, 0x61, 0xE0, 0x20, 0xC3, 0xB0, 0x01,
           0x8F, 0x1C, 0x00, 0x1C, 0x0C, 0x00, 0x00, 0x00),

    "月": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xFF, 0xF0, 0x06, 0x00, 0x30, 0x06,
           0x00, 0x30, 0x06, 0x00, 0x30, 0x06, 0x00, 0x30, 0x07, 0xFF, 0xF0, 0x07, 0xFF, 0xF0, 0x06, 0x00,
           0x30, 0x06, 0x00, 0x30, 0x06, 0x00, 0x30, 0x07, 0xFF, 0xF0, 0x07, 0xFF, 0xF0, 0x06, 0x00, 0x30,
           0x06, 0x00, 0x30, 0x04, 0x00, 0x30, 0x0C, 0x00, 0x30, 0x0C, 0x00, 0x30, 0x18, 0x00, 0x60, 0x38,
           0x03, 0xE0, 0x30, 0x01, 0xC0, 0x00, 0x00, 0x00),

    "日": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xFF, 0xF0, 0x07, 0xFF, 0xF0, 0x06, 0x00, 0x30, 0x06,
           0x00, 0x30, 0x06, 0x00, 0x30, 0x06, 0x00, 0x30, 0x06, 0x00, 0x30, 0x06, 0x00, 0x30, 0x07, 0xFF,
           0xF0, 0x07, 0xFF, 0xF0, 0x06, 0x00, 0x30, 0x06, 0x00, 0x30, 0x06, 0x00, 0x30, 0x06, 0x00, 0x30,
           0x06, 0x00, 0x30, 0x06, 0x00, 0x30, 0x06, 0x00, 0x30, 0x07, 0xFF, 0xF0, 0x06, 0x00, 0x30, 0x06,
           0x00, 0x30, 0x06, 0x00, 0x30, 0x00, 0x00, 0x00),
    '一': (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
           0x08, 0x7F, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,),
    "二": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0F,
           0xFF, 0xF0, 0x0F, 0xFF, 0xF0, 0x0F, 0xFF, 0xF0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x7F, 0xFF, 0xFE, 0x7F, 0xFF, 0xFE, 0x00,
           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),

    "三": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0xFF, 0xF8, 0x1F,
           0xFF, 0xF8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
           0x00, 0x07, 0xFF, 0xE0, 0x07, 0xFF, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7F, 0xFF, 0xFE, 0x7F,
           0xFF, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),

    "四": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF, 0xFC, 0x3F, 0xFF, 0xFC, 0x30,
           0x66, 0x08, 0x30, 0x66, 0x08, 0x30, 0x66, 0x08, 0x30, 0x46, 0x08, 0x30, 0x46, 0x08, 0x30, 0xC6,
           0x08, 0x30, 0xC6, 0x08, 0x31, 0x86, 0x08, 0x31, 0x86, 0x08, 0x33, 0x07, 0xC8, 0x36, 0x00, 0x08,
           0x30, 0x00, 0x08, 0x30, 0x00, 0x08, 0x30, 0x00, 0x08, 0x3F, 0xFF, 0xF8, 0x3F, 0xFF, 0xFC, 0x30,
           0x00, 0x0C, 0x30, 0x00, 0x0C, 0x00, 0x00, 0x00),

    "五": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0xFF, 0xF8, 0x00,
           0x30, 0x00, 0x00, 0x30, 0x00, 0x00, 0x30, 0x00, 0x00, 0x20, 0x00, 0x00, 0x20, 0x00, 0x0F, 0xFF,
           0xE0, 0x0F, 0xFF, 0xC0, 0x00, 0x60, 0x40, 0x00, 0x60, 0x40, 0x00, 0x60, 0xC0, 0x00, 0x60, 0xC0,
           0x00, 0x40, 0xC0, 0x00, 0xC0, 0xC0, 0x00, 0xC0, 0xC0, 0x00, 0xC0, 0xC0, 0x3F, 0xFF, 0xFE, 0x3F,
           0xFF, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),

    "六": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x70, 0x00, 0x00, 0x38, 0x00, 0x00,
           0x18, 0x00, 0x00, 0x1C, 0x00, 0x00, 0x10, 0x00, 0x3F, 0xFF, 0xFC, 0x3F, 0xFF, 0xFC, 0x00, 0x00,
           0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0xC3, 0x80, 0x01, 0xC1, 0x80, 0x01, 0x81, 0xC0,
           0x03, 0x80, 0xE0, 0x07, 0x00, 0x70, 0x0E, 0x00, 0x30, 0x1C, 0x00, 0x38, 0x1C, 0x00, 0x1C, 0x38,
           0x00, 0x08, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00),

    "周": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0F, 0xFF, 0xF8, 0x0C, 0x00, 0x18, 0x0C,
           0x18, 0x18, 0x0C, 0x18, 0x18, 0x0D, 0xFF, 0x98, 0x0C, 0x18, 0x18, 0x0C, 0x18, 0x18, 0x0F, 0xFF,
           0xD8, 0x0F, 0xFF, 0xD8, 0x0C, 0x00, 0x18, 0x08, 0x00, 0x18, 0x08, 0xFF, 0x18, 0x18, 0xC1, 0x18,
           0x18, 0xC1, 0x18, 0x18, 0xC1, 0x18, 0x18, 0xFF, 0x18, 0x30, 0xFF, 0x18, 0x30, 0x00, 0x18, 0x70,
           0x00, 0xF8, 0x20, 0x00, 0xF0, 0x00, 0x00, 0x00),

    "实": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x1F,
           0xFF, 0xFC, 0x18, 0x00, 0x1C, 0x18, 0x04, 0x1C, 0x19, 0x86, 0x1C, 0x01, 0xC6, 0x00, 0x00, 0x76,
           0x00, 0x0C, 0x26, 0x00, 0x0F, 0x06, 0x00, 0x03, 0x86, 0x00, 0x01, 0x06, 0x00, 0x3F, 0xFF, 0xFC,
           0x3F, 0xFF, 0xFC, 0x00, 0x0C, 0x00, 0x00, 0x19, 0x00, 0x00, 0x73, 0xC0, 0x01, 0xE0, 0xF0, 0x0F,
           0x80, 0x3C, 0x1E, 0x00, 0x1C, 0x10, 0x00, 0x00),

    "时": (0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x30, 0x00, 0x00, 0x30, 0x3F, 0x80, 0x30, 0x31,
           0x80, 0x30, 0x31, 0x80, 0x30, 0x31, 0xBF, 0xFE, 0x31, 0x80, 0x30, 0x31, 0x80, 0x30, 0x3F, 0x80,
           0x30, 0x31, 0x8C, 0x30, 0x31, 0x8C, 0x30, 0x31, 0x86, 0x30, 0x31, 0x86, 0x30, 0x31, 0x80, 0x30,
           0x3F, 0x80, 0x30, 0x3F, 0x80, 0x30, 0x31, 0x80, 0x30, 0x31, 0x80, 0x30, 0x30, 0x00, 0x30, 0x00,
           0x00, 0xF0, 0x00, 0x00, 0xE0, 0x00, 0x00, 0x00),

    "今": (0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x18, 0x00, 0x00, 0x38, 0x00, 0x00, 0x3C, 0x00, 0x00,
           0x66, 0x00, 0x00, 0xC3, 0x00, 0x01, 0x81, 0x80, 0x03, 0x01, 0xC0, 0x06, 0x30, 0xE0, 0x0C, 0x38,
           0x78, 0x38, 0x1C, 0x1E, 0x30, 0x08, 0x0C, 0x00, 0x00, 0x00, 0x07, 0xFF, 0xF0, 0x07, 0xFF, 0xF0,
           0x00, 0x00, 0xE0, 0x00, 0x01, 0xC0, 0x00, 0x01, 0x80, 0x00, 0x03, 0x00, 0x00, 0x06, 0x00, 0x00,
           0x0E, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x04, 0x00),

    "天": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0F, 0xFF, 0xF0, 0x00, 0x18, 0x00, 0x00,
           0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x3F, 0xFF, 0xFC, 0x3F, 0xFF,
           0xFC, 0x00, 0x18, 0x00, 0x00, 0x3C, 0x00, 0x00, 0x3C, 0x00, 0x00, 0x36, 0x00, 0x00, 0x66, 0x00,
           0x00, 0xE3, 0x00, 0x01, 0xC1, 0x80, 0x03, 0x81, 0xC0, 0x07, 0x00, 0xF0, 0x1E, 0x00, 0x3C, 0x7C,
           0x00, 0x1C, 0x30, 0x00, 0x04, 0x00, 0x00, 0x00),

    "气": (0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x03, 0x00, 0x00, 0x03, 0x00, 0x00, 0x07, 0xFF, 0xF8, 0x0E,
           0x00, 0x08, 0x0C, 0x00, 0x00, 0x18, 0x00, 0x00, 0x3B, 0xFF, 0xE0, 0x30, 0x00, 0x00, 0x00, 0x00,
           0x00, 0x1F, 0xFF, 0xE0, 0x1F, 0xFF, 0xE0, 0x00, 0x00, 0x60, 0x00, 0x00, 0x60, 0x00, 0x00, 0x60,
           0x00, 0x00, 0x60, 0x00, 0x00, 0x60, 0x00, 0x00, 0x64, 0x00, 0x00, 0x66, 0x00, 0x00, 0x7E, 0x00,
           0x00, 0x3C, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00),

    "转": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x01, 0x80, 0x0C, 0x01, 0x80, 0x0C, 0x01, 0x00, 0x7F,
           0xDF, 0xFC, 0x7F, 0xDF, 0xFC, 0x18, 0x03, 0x00, 0x1B, 0x03, 0x00, 0x13, 0x22, 0x02, 0x33, 0x3F,
           0xFE, 0x63, 0x06, 0x00, 0x7F, 0xC6, 0x00, 0x23, 0x04, 0x00, 0x03, 0x0F, 0xF8, 0x03, 0x00, 0x38,
           0x03, 0xC0, 0x30, 0x7F, 0x80, 0x60, 0x63, 0x0C, 0xC0, 0x03, 0x07, 0x80, 0x03, 0x03, 0xC0, 0x03,
           0x00, 0xE0, 0x03, 0x00, 0x60, 0x00, 0x00, 0x00),

    "到": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x08, 0x3F, 0xFC, 0x0C, 0x01, 0x80, 0x0C, 0x01,
           0x80, 0x8C, 0x02, 0x00, 0x8C, 0x04, 0x30, 0x8C, 0x08, 0x18, 0x8C, 0x1F, 0xFC, 0x8C, 0x19, 0x8C,
           0x8C, 0x01, 0x84, 0x8C, 0x01, 0x80, 0x8C, 0x01, 0x88, 0x8C, 0x3F, 0xFC, 0x8C, 0x01, 0x80, 0x8C,
           0x01, 0x80, 0x8C, 0x01, 0x80, 0x8C, 0x01, 0x84, 0x0C, 0x01, 0xF8, 0x0C, 0x1F, 0x00, 0x0C, 0x38,
           0x00, 0x78, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00),

    "晴": (0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x01, 0x80, 0x00, 0x3F, 0xFC, 0x3F, 0x3F, 0xFC, 0x23,
           0x01, 0x80, 0x23, 0x3F, 0xFC, 0x23, 0x3F, 0xFC, 0x23, 0x01, 0x80, 0x23, 0x7F, 0xFE, 0x3F, 0x7F,
           0xFE, 0x3F, 0x00, 0x00, 0x23, 0x1F, 0xF8, 0x23, 0x10, 0x08, 0x23, 0x10, 0x08, 0x23, 0x1F, 0xF8,
           0x23, 0x10, 0x08, 0x3F, 0x10, 0x08, 0x23, 0x1F, 0xF8, 0x23, 0x1F, 0xF8, 0x20, 0x10, 0x08, 0x00,
           0x10, 0x18, 0x00, 0x10, 0x38, 0x00, 0x00, 0x00),

    "阴": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xCF, 0xFC, 0x30, 0xCC, 0x08, 0x30,
           0x8C, 0x08, 0x31, 0x8C, 0x08, 0x31, 0x8C, 0x08, 0x31, 0x0F, 0xF8, 0x33, 0x0F, 0xF8, 0x33, 0x0C,
           0x08, 0x33, 0x0C, 0x08, 0x31, 0x8C, 0x08, 0x31, 0x8F, 0xF8, 0x30, 0xCF, 0xF8, 0x30, 0xCC, 0x08,
           0x30, 0xC8, 0x08, 0x37, 0x98, 0x08, 0x33, 0x18, 0x08, 0x30, 0x30, 0x08, 0x30, 0x70, 0x08, 0x30,
           0x60, 0x78, 0x30, 0xC0, 0x78, 0x00, 0x00, 0x00),

    "雨": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF, 0xFE, 0x00, 0x18, 0x00, 0x00,
           0x18, 0x00, 0x00, 0x18, 0x00, 0x1F, 0xFF, 0xFC, 0x1F, 0xFF, 0xFC, 0x18, 0x18, 0x0C, 0x19, 0x19,
           0x0C, 0x19, 0x99, 0x8C, 0x18, 0xD8, 0xCC, 0x18, 0x18, 0x4C, 0x18, 0x18, 0x0C, 0x19, 0x18, 0x0C,
           0x1B, 0x99, 0x8C, 0x19, 0xD9, 0xCC, 0x18, 0x98, 0x0C, 0x18, 0x18, 0x0C, 0x18, 0x18, 0x0C, 0x18,
           0x18, 0x3C, 0x18, 0x00, 0x38, 0x00, 0x00, 0x00),

    "雷": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0xFF, 0xF8, 0x18, 0x18, 0x18, 0x00, 0x18, 0x00, 0x7F,
           0xFF, 0xFE, 0x7F, 0xFF, 0xFE, 0x60, 0x18, 0x06, 0x67, 0x9B, 0xE6, 0x00, 0x18, 0x00, 0x07, 0x99,
           0xE0, 0x07, 0x99, 0xE0, 0x00, 0x18, 0x00, 0x0F, 0xFF, 0xF0, 0x0F, 0xFF, 0xF0, 0x0C, 0x18, 0x30,
           0x0C, 0x18, 0x30, 0x0F, 0xFF, 0xF0, 0x0C, 0x18, 0x30, 0x0C, 0x18, 0x30, 0x0C, 0x18, 0x30, 0x0F,
           0xFF, 0xF0, 0x0C, 0x00, 0x30, 0x00, 0x00, 0x00),

    "阵": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x3F, 0x07, 0x00, 0x33, 0x06, 0x00, 0x33,
           0x7F, 0xFC, 0x32, 0x7F, 0xFC, 0x36, 0x0C, 0x00, 0x36, 0x08, 0x00, 0x34, 0x19, 0x80, 0x36, 0x31,
           0x80, 0x32, 0x31, 0x80, 0x33, 0x7F, 0xFC, 0x31, 0x31, 0x80, 0x31, 0x81, 0x80, 0x31, 0x81, 0x80,
           0x3F, 0x01, 0x80, 0x36, 0x7F, 0xFE, 0x30, 0x7F, 0xFE, 0x30, 0x01, 0x80, 0x30, 0x01, 0x80, 0x30,
           0x01, 0x80, 0x30, 0x01, 0x80, 0x00, 0x00, 0x00),

    "多": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0xC0, 0x00, 0x01, 0xFF, 0xE0, 0x03,
           0x00, 0xC0, 0x0E, 0x00, 0xC0, 0x1C, 0xC3, 0x80, 0x00, 0x67, 0x00, 0x00, 0x3C, 0x00, 0x00, 0x3A,
           0x00, 0x01, 0xE7, 0x00, 0x3F, 0x8F, 0xFC, 0x18, 0x1F, 0xFC, 0x00, 0x70, 0x18, 0x01, 0xF0, 0x18,
           0x07, 0x98, 0x30, 0x06, 0x0C, 0x60, 0x00, 0x07, 0xC0, 0x00, 0x07, 0x80, 0x00, 0x1E, 0x00, 0x07,
           0xF8, 0x00, 0x1F, 0xC0, 0x00, 0x00, 0x00, 0x00),

    "云": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xFF, 0xF0, 0x07, 0xFF, 0xF0, 0x00,
           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF,
           0xFC, 0x00, 0x40, 0x00, 0x00, 0x70, 0x00, 0x00, 0x60, 0x00, 0x00, 0xC0, 0x00, 0x01, 0xC1, 0x80,
           0x01, 0x81, 0x80, 0x03, 0x00, 0xC0, 0x06, 0x00, 0x60, 0x0E, 0x00, 0xF0, 0x1F, 0xFF, 0xF8, 0x0F,
           0xC0, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),

    "小": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00,
           0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x07, 0x18, 0xC0, 0x06, 0x18, 0xE0, 0x06, 0x18,
           0x60, 0x0E, 0x18, 0x70, 0x0C, 0x18, 0x30, 0x0C, 0x18, 0x38, 0x18, 0x18, 0x18, 0x18, 0x18, 0x1C,
           0x38, 0x18, 0x0C, 0x10, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00,
           0xF8, 0x00, 0x00, 0x70, 0x00, 0x00, 0x00, 0x00),

    "大": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x00,
           0x18, 0x00, 0x00, 0x18, 0x00, 0x00, 0x18, 0x00, 0x3F, 0xFF, 0xFC, 0x3F, 0xFF, 0xFC, 0x00, 0x18,
           0x00, 0x00, 0x38, 0x00, 0x00, 0x3C, 0x00, 0x00, 0x3C, 0x00, 0x00, 0x66, 0x00, 0x00, 0x67, 0x00,
           0x00, 0xC3, 0x00, 0x01, 0xC1, 0x80, 0x03, 0x80, 0xC0, 0x0F, 0x00, 0xF0, 0x1E, 0x00, 0x38, 0x78,
           0x00, 0x1C, 0x30, 0x00, 0x08, 0x00, 0x00, 0x00),

    "暴": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xFF, 0xE0, 0x04, 0x00, 0x20, 0x04, 0x00, 0x20, 0x07,
           0xFF, 0xE0, 0x04, 0x00, 0x20, 0x07, 0xFF, 0xE0, 0x00, 0xC3, 0x00, 0x00, 0xC3, 0x00, 0x1F, 0xFF,
           0xF8, 0x00, 0xC3, 0x00, 0x00, 0xC3, 0x00, 0x3F, 0xFF, 0xFC, 0x01, 0x81, 0x80, 0x07, 0x18, 0xE0,
           0x3D, 0x18, 0xBC, 0x33, 0x9D, 0xCC, 0x00, 0xFF, 0x00, 0x03, 0xDB, 0xC0, 0x1F, 0x18, 0xF0, 0x08,
           0x78, 0x30, 0x00, 0x30, 0x10, 0x00, 0x00, 0x00),

    "雾": (0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x07, 0xFF, 0xE0, 0x00, 0x18, 0x00, 0x0F, 0xFF, 0xF8, 0x10,
           0x18, 0x08, 0x13, 0xDB, 0xD0, 0x00, 0x18, 0x00, 0x03, 0xDB, 0xC0, 0x00, 0x80, 0x00, 0x01, 0xFF,
           0x80, 0x02, 0x81, 0x80, 0x0C, 0x62, 0x00, 0x10, 0x1C, 0x00, 0x00, 0xE7, 0xFE, 0x1F, 0x20, 0x78,
           0x20, 0x10, 0x00, 0x07, 0xFF, 0xE0, 0x00, 0x20, 0x40, 0x00, 0x60, 0x40, 0x00, 0xC0, 0x80, 0x03,
           0x07, 0x80, 0x1C, 0x03, 0x00, 0x00, 0x00, 0x00),

    "雪": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x0F, 0xFF, 0xF0, 0x00, 0x10, 0x00, 0x10,
           0x10, 0x00, 0x1F, 0xFF, 0xFC, 0x10, 0x10, 0x08, 0x37, 0xD3, 0xF0, 0x20, 0x10, 0x00, 0x00, 0x10,
           0x00, 0x07, 0xD3, 0xE0, 0x00, 0x10, 0x20, 0x0F, 0xFF, 0xF0, 0x00, 0x00, 0x20, 0x00, 0x00, 0x20,
           0x00, 0x00, 0x20, 0x07, 0xFF, 0xE0, 0x00, 0x00, 0x20, 0x00, 0x00, 0x20, 0x1F, 0xFF, 0xE0, 0x00,
           0x00, 0x20, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00),

    "夹": (0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x18, 0x00, 0x00, 0x10, 0x00, 0x00, 0x10, 0x00, 0x1F,
           0xFF, 0xF0, 0x00, 0x10, 0x00, 0x00, 0x10, 0x00, 0x04, 0x10, 0xC0, 0x02, 0x10, 0x80, 0x03, 0x11,
           0x80, 0x01, 0x11, 0x00, 0x01, 0x32, 0x08, 0x7F, 0xFF, 0xFC, 0x00, 0x24, 0x00, 0x00, 0x24, 0x00,
           0x00, 0x62, 0x00, 0x00, 0x42, 0x00, 0x00, 0x81, 0x80, 0x01, 0x00, 0xC0, 0x06, 0x00, 0x70, 0x18,
           0x00, 0x1E, 0x60, 0x00, 0x08, 0x00, 0x00, 0x00),

    "℃": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x24, 0x00, 0x00, 0x24, 0x03, 0x00, 0x24,
          0x1F, 0xE0, 0x18, 0x38, 0x70, 0x00, 0x60, 0x18, 0x00, 0xC0, 0x1C, 0x00, 0xC0, 0x00, 0x00, 0xC0,
          0x00, 0x00, 0x80, 0x00, 0x01, 0x80, 0x00, 0x01, 0x80, 0x00, 0x01, 0x80, 0x00, 0x00, 0xC0, 0x00,
          0x00, 0xC0, 0x0C, 0x00, 0xC0, 0x18, 0x00, 0x60, 0x38, 0x00, 0x38, 0xF0, 0x00, 0x1F, 0xE0, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),

    "％": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x0F,
          0x80, 0x18, 0x18, 0xC0, 0x30, 0x18, 0xC0, 0x60, 0x18, 0x40, 0xC0, 0x18, 0xC3, 0x80, 0x18, 0xC7,
          0x00, 0x0D, 0x8E, 0x00, 0x07, 0x1C, 0x00, 0x00, 0x39, 0xF0, 0x00, 0x73, 0x10, 0x00, 0xE3, 0x18,
          0x01, 0xC2, 0x18, 0x03, 0x02, 0x18, 0x06, 0x03, 0x18, 0x0C, 0x03, 0x10, 0x08, 0x01, 0xF0, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),

}

hanzi_16x16_dict = {
    "确": (
        0x0, 0x70, 0x7f, 0x7f, 0x7f, 0xfe, 0x19, 0xce, 0x1b, 0xff, 0x3e, 0xff, 0x3e, 0xd9, 0x76, 0xff, 0xf6, 0xff, 0xf6,
        0xd9, 0x76, 0xff, 0x3e, 0xff, 0x3f, 0xd9, 0x37, 0x9f, 0x37, 0x9f, 0x3, 0x1f,),
    "诊": (
        0x0, 0x70, 0x30, 0x70, 0x38, 0xf0, 0x38, 0xd8, 0x19, 0xdc, 0xf3, 0xaf, 0xff, 0x77, 0xf6, 0xe9, 0x33, 0xdc, 0x33,
        0xb8, 0x31, 0x76, 0x35, 0xef, 0x3f, 0xdc, 0x3c, 0x78, 0x3b, 0xf0, 0x3, 0xc0,),
    "新": (
        0xe, 0x0, 0xe, 0x3f, 0x7f, 0xff, 0x7f, 0xb0, 0x3b, 0xb0, 0x5b, 0x3f, 0x7f, 0xff, 0x6c, 0xbf, 0x7f, 0xf6, 0x7f,
        0xf6, 0x3f, 0x66, 0x3f, 0xe6, 0x7d, 0xe6, 0xfd, 0xe6, 0x1d, 0xc6, 0x18, 0xc6,),
    "增": (
        0x38, 0xe6, 0x38, 0x6e, 0x3b, 0xff, 0x3b, 0xff, 0xff, 0xdf, 0xff, 0xff, 0x3b, 0xfd, 0x3b, 0xff, 0x3b, 0xff,
        0x39, 0xff, 0x3f, 0xff, 0x7f, 0xff, 0xfd, 0xff, 0x61, 0xff, 0x1, 0xff, 0x1, 0x83,),
    "无": (
        0x1f, 0xfe, 0x1f, 0xfe, 0x11, 0xc2, 0x1, 0x80, 0x1, 0x80, 0x7f, 0xff, 0x7f, 0xff, 0x1, 0xe0, 0x3, 0xe0, 0x3,
        0x60, 0x7, 0x60, 0xe, 0x63, 0x1c, 0x63, 0x78, 0x7f, 0x70, 0x3f, 0x0, 0x0,),
    "症": (
        0x0, 0x60, 0x1f, 0xff, 0x1f, 0xff, 0x7c, 0x0, 0x7c, 0x0, 0x7f, 0xff, 0x7f, 0xff, 0x1c, 0x38, 0x7f, 0xbf, 0x7d,
        0xbf, 0x59, 0xb9, 0x19, 0xb8, 0x39, 0xb8, 0x37, 0xff, 0x77, 0xff, 0x20, 0x0,),
    "状": (
        0xc, 0x30, 0xc, 0x34, 0xc, 0x3e, 0x6c, 0x37, 0x7c, 0x36, 0x3f, 0xff, 0x3f, 0xff, 0xc, 0x70, 0x1c, 0x70, 0x3c,
        0x78, 0xfc, 0x78, 0x6c, 0xfc, 0x4c, 0xce, 0xd, 0xcf, 0xf, 0x87, 0xd, 0x2,),
    " ": (
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,),
    "期": (
        0x39, 0xbf, 0x7f, 0xff, 0x7f, 0xf3, 0x7f, 0xf3, 0x3f, 0xbf, 0x3f, 0xbf, 0x39, 0xb3, 0x3f, 0xb3, 0x3f, 0xbf,
        0x39,
        0xbf, 0xff, 0xff, 0xff, 0xf3, 0x3b, 0xe3, 0x73, 0xe3, 0x61, 0xcf, 0x0, 0xc7,),
    "日": (
        0x3f, 0xfe, 0x30, 0xe, 0x30, 0xe, 0x30, 0xe, 0x30, 0xe, 0x3f, 0xfe, 0x3f, 0xfe, 0x3f, 0xfe, 0x30, 0xe, 0x30,
        0xe,
        0x30, 0xe, 0x30, 0xe, 0x3f, 0xfe, 0x3f, 0xfe, 0x30, 0xe, 0x30, 0xc,)
}
