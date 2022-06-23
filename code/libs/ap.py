#AP配网
from libs import global_var
import os,json,gc,re
from machine import Pin

import network
import socket
import ure
import time

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
YELLOW = (255,255,0)
DEEPGREEN = (1,179,105)

wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

server_socket = None

def send_header(conn, status_code=200, content_length=None ):
    conn.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    conn.sendall("Content-Type: text/html\r\n")
    if content_length is not None:
      conn.sendall("Content-Length: {}\r\n".format(content_length))
    conn.sendall("\r\n")

def send_response(conn, payload, status_code=200):
    content_length = len(payload)
    send_header(conn, status_code, content_length)
    if content_length > 0:
        conn.sendall(payload)
    conn.close()

#WiFi配置页面
def config_page():
    return b"""<!DOCTYPE html>
<!-- saved from url=(0014)about:internet -->
<html>
  <head>
    <title>pyClock WiFi Config</title>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
        .c,
        body {
            text-align: center;
            font-family: verdana
        }

        div,
        input {
            padding: 5px;
            font-size: 1em;
            margin: 5px 0;
            box-sizing: border-box;
                        
        }

        input,
        button,
        .msg {
            border-radius: .3rem;
            width: 100%
        }

        button,
        input[type=&amp;amp;#39;button&amp;amp;#39;],
        input[type=&amp;amp;#39;submit&amp;amp;#39;] {
            cursor: pointer;
            border: 0;
            background-color: #1fa3ec;
            color: #fff;
            line-height: 2.4rem;
            font-size: 1.2rem;
            width: 100%
        }

        input[type=&amp;amp;#39;file&amp;amp;#39;] {
            border: 1px solid #1fa3ec
        }

        .wrap {
            text-align: left;
            display: inline-block;
            min-width: 260px;
            max-width: 500px
        }

        body.invert,
        body.invert a,
        body.invert h1 {
            background-color: #606060;
            color: #fff;
        }

        body.invert .msg {
            color: #fff;
            background-color: #282828;
            border-top: 1px solid #555;
            border-right: 1px solid #555;
            border-bottom: 1px solid #555;
        }

        body.invert .q[role=img] {
            -webkit-filter: invert(1);
            filter: invert(1);
        }

        input:disabled {
            opacity: 0.5;
        }
    
</style>
  </head>
  <body class="invert">
    <div class="wrap">
      <h1>pyClock WiFi配网</h1>
      <form action="configure" method="post">
        <div>
        <label>WiFi账号</label> 
        <input type="text" name="ssid" /></div>
        <div>
        <label>WiFi密码</label> 
        <input type="password" name="password" /></div>
        <div>
        <label>城市名 (例：深圳)</label> 
        <input type="citycode" name="citycode" /></div>
        <br />
        <input type="submit" value="连接" />
      </form>
    </div>
  </body>
</html>
"""

def web_page():
    return b"""<html>
                    <head>
                        <title>pyClock Connecting!</title>
                        <meta charset="UTF-8">
                    </head>
                    <body>
                        <h1>配置完成。</h1>
                    </body>
                </html>"""

def connect_sucess(new_ip):
    return b"""<html>
                    <head>
                        <title>Connect Sucess!</title>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                    </head>
                    <body>
                        <p>Wifi Connect Sucess</p>
                        <p>IP Address: %s</p>
                        <a href="http://%s">Home</a>
                        <a href="/disconnect">Disconnect</a>
                    </body>
               </html>""" % (new_ip, new_ip)

#中文转字节字符串
_hextobyte_cache = None

def unquote(string):
    """unquote('abc%20def') -> b'abc def'."""
    global _hextobyte_cache

    # Note: strings are encoded as UTF-8. This is only an issue if it contains
    # unescaped non-ASCII characters, which URIs should not.
    if not string:
        return b''

    if isinstance(string, str):
        string = string.encode('utf-8')

    bits = string.split(b'%')
    if len(bits) == 1:
        return string

    res = [bits[0]]
    append = res.append

    # Build cache for hex to char mapping on-the-fly only for codes
    # that are actually used
    if _hextobyte_cache is None:
        _hextobyte_cache = {}

    for item in bits[1:]:
        try:
            code = item[:2]
            char = _hextobyte_cache.get(code)
            if char is None:
                char = _hextobyte_cache[code] = bytes([int(code, 16)])
            append(char)
            append(item[2:])
        except KeyError:
            append(b'%')
            append(item)

    return b''.join(res)

#从配置网页获取WiFi账号密码
def get_wifi_conf(request):
    match = ure.search("ssid=([^&]*)&password=(.*)&citycode=(.*)", request)
    if match is None:
        return None

    try:
        ssid = match.group(1).decode("utf-8").replace("%3F", "?").replace("%21", "!")
        password = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!")
        cityname = match.group(3).decode("utf-8").replace("%3F", "?").replace("%21", "!")
    except Exception:
        ssid = match.group(1).replace("%3F", "?").replace("%21", "!")
        password = match.group(2).replace("%3F", "?").replace("%21", "!")
        cityname = match.group(3).replace("%3F", "?").replace("%21", "!")

    if len(ssid) == 0 or len(cityname) == 0: #wifi名称或者城市名称为空。
        return None
    return (ssid, password,cityname)


def handle_wifi_configure(ssid, password):
    if do_connect(ssid, password):         
        new_ip = wlan_sta.ifconfig()[0]
        return new_ip
    else:
        print('connect fail')
        return None

def check_wlan_connected():
    if wlan_sta.isconnected():
        return True
    else:
        return False

def do_connect(ssid, password):
    wlan_sta.active(True)
    if wlan_sta.isconnected():
        return None
    print('Connect to %s' % ssid)
    wlan_sta.connect(ssid, password)
    for retry in range(150):
        connected = wlan_sta.isconnected()
        if connected:
            break
        time.sleep(0.1)
        print('.', end='')
    if connected:
        print('\nConnected : ', wlan_sta.ifconfig())
    else:
        print('\nFailed. Not Connected to: ' + ssid)
        wlan_sta.active(False)
    return connected

def read_profiles():
    with open(NETWORK_PROFILES) as f:
        lines = f.readlines()
    profiles = {}
    for line in lines:
        ssid, password = line.strip("\n").split(";")
        profiles[ssid] = password
    return profiles


def write_profiles(profiles):
    lines = []
    for ssid, password in profiles.items():
        lines.append("%s;%s\n" % (ssid, password))
    with open(NETWORK_PROFILES, "w") as f:
        f.write(''.join(lines))

#停止Socket服务
def stop():
    global server_socket

    if server_socket:
        server_socket.close()
        server_socket = None
        
   
#判断有无改城市
def city_judge(CityName):

    if CityName == '':
        
        return False
    
    city_name = unquote(CityName).decode("gbk") #转成中文编码

    f = open('/data/CityCode.txt', 'r')
    num = 0
    
    while True:

        text = f.readline()

        if city_name in text:

            if city_name == re.match(r'"(.+?)"',text).group(1): #城市名称完全一样

                city_code = re.match(r'"(.+?)"',text.split(': ')[1]).group(1) #"获取城市编码"

                return city_code

        elif '}' in text: #结束，没这个城市。
            
            print('No City Name!')
            return False

        num = num + 1

        if num == 300:

            gc.collect() #内存回收
            num = 0            
    f.close()
    
def startAP():
    
    global server_socket
    
    stop() #停止Socket服务
    
    print('Connect pyClock AP to Config WiFi.')

    #启动热点，名称问pyClock，不加密。
    wlan_ap.active(True)
    wlan_ap.config(essid='pyClock',authmode=0)

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 80))
    server_socket.listen(10)

    d.Picture(0,0,"/data/picture/Step1.jpg") #步骤1，连接AP热点。

    while not wlan_ap.isconnected(): #等待AP接入
        
        pass
    
    d.Picture(0,0,"/data/picture/Step2.jpg") #步骤2，登录192.168.4.1进行配网。
 
    while not wlan_sta.isconnected(): #开发板没连上路由器
        
        #等待配网设备接入
        conn, addr = server_socket.accept()
        print('Connection: %s ' % str(addr))

        try:
            conn.settimeout(3)
            request = b""

            try:
                while "\r\n\r\n" not in request:
                    request += conn.recv(2048) #增大适配多种浏览器
                
                print(request)
                    
                # url process
                try:
                    url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).decode("utf-8").rstrip("/")
                except Exception:
                    url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).rstrip("/")
                    pass
                
                print("URL is {}".format(url))

                #收到内容为空时，发送配置页面。
                if url == "": 
                    print("send config web!")
                    response = config_page()
                    send_response(conn, response)              
                    
                elif url == "configure":
                    
                    #获取配置信息，SSID,PASSWORD,CITY
                    ret = get_wifi_conf(request)
                    print(ret)
                    
                    if ret != None: #获取信息成功
                        
                        if city_judge(ret[2]): #有该城市
                        
                            d.fill(BLACK)
                            d.printStr('Connecting...', 10, 50, RED, size=2)
                            d.printStr(ret[0], 10, 110, WHITE, size=2)
                            
                            #SSID带中文处理
                            if '%' in ret[0]:
                                print('wifi chinese')
                                SSID = unquote(ret[0]).decode("gbk")
                            else:
                                SSID = ret[0]
                            
                            ret_ip = handle_wifi_configure(SSID, ret[1])
                            print(ret_ip)
                            if ret_ip is not None:
                                
                                #保存WiFi信息到wifi.txt,字典格式。
                                wifi_info = {'SSID':'','PASSWORD':''}

                                wifi_info['SSID'] = SSID
                                wifi_info['PASSWORD'] = ret[1]
                                wifi_info['CITY'] = unquote(ret[2]).decode("gbk")
                                print(wifi_info)
                                
                                f = open('wifi.txt', 'w') #以写的方式打开一个文件，没有该文件就自动新建
                                f.write(json.dumps(wifi_info)) #写入数据
                                f.close() #每次操作完记得关闭文件
                                
                                response = web_page()
                                send_response(conn, response)
                                
                            else:#连接失败
                                response = config_page()
                                send_response(conn, response)
                                d.Picture(0,0,"/data/picture/error2.jpg") #步骤2，登录192.168.4.1进行配网。
                        
                        else: #没该城市，重新配置
                            
                            response = config_page()
                            send_response(conn, response)
                            d.Picture(0,0,"/data/picture/error1.jpg") #步骤2，登录192.168.4.1进行配网。
                            
                    else : #获取信息不成功
                        
                        response = config_page()
                        send_response(conn, response)
                        d.Picture(0,0,"/data/picture/error3.jpg") #步骤2，登录192.168.4.1进行配网。
                    
                elif url == "disconnect":
                    wlan_sta.disconnect()

            except OSError:
                pass

        finally:
            conn.close()
    wlan_ap.active(False)
    stop()
    print('ap exit')
