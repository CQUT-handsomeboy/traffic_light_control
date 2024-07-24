from machine import Pin, SPI
from micropython import const

# import gc9a01  # type:ignore
# from truetype import NotoSans_32 as noto_sans  # type:ignore

# 所有常量

WIFI_SSID = const("cxs")
WIFI_PASSWORD = const("@12345678")

UDP_PORT = const(12345)

TX_PIN_NUM = const(21)
RX_PIN_NUM = const(20)

RED_PIN_NUM = const(1)
GREEN_PIN_NUM = const(2)
YELLOW_PIN_NUM = const(3)

import network
from time import sleep

def log(info):
    """
    打印日志
    """
    info = str(info)
    print(info)

def connect_wifi():
    global wlan
    wlan = network.WLAN(network.STA_IF)

    wlan.active(False)
    wlan.active(True)

    if wlan.isconnected():
        return True

    wlan.active(False)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    log("connecting wifi...")
    sleep(5)
    log("check")

    if wlan.isconnected():
        return True
    else:
        return False


ret = connect_wifi()

if ret:
    ADDR = wlan.ifconfig()[0]
    log(ADDR)
else:
    from sys import exit

    log("[ERROR]wifi is not connected!")
    exit(-1)


import socket
import json

from machine import UART

data_handler = None

red_pin = Pin(RED_PIN_NUM, Pin.OUT)
yellow_pin = Pin(YELLOW_PIN_NUM, Pin.OUT)
green_pin = Pin(GREEN_PIN_NUM, Pin.OUT)

uart = UART(1, 115200, rx=RX_PIN_NUM, tx=TX_PIN_NUM)

"""
0xFF 0xFF 为协议头
紧接着是后面的有效字节位数
然后是数据
"""

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ADDR, UDP_PORT))
    while 1:
        data, addr = s.recvfrom(1024)
        try:
            data_handler = json.loads(data)
        except ValueError:  # json包无效格式
            info = "Invalid JSON package format"
            back_string = json.dumps(
                {"error": True, "info": info}
            )
            s.sendto(back_string + "\r\n", addr)  # 向遥控端回传错误信息
            continue

        if "color" not in data_handler:  # json包无效键
            info = "Invalid key in JSON package"
            back_string = json.dumps(
                {
                    "error": True,
                    "info": info,
                }
            )
            log(info)
            s.sendto(back_string + "\r\n", addr)  # 向遥控端回传错误信息
            continue

        if data_handler["color"] == "red":
            red_pin.value(1)
            yellow_pin.value(0)
            green_pin.value(0)
            log("red")

            uart.write("red")
            # uart.write(bytes([0xFF,0xFF,0x01,0x0]))

        elif data_handler["color"] == "green":
            green_pin.value(1)
            red_pin.value(0)
            yellow_pin.value(0)
            log("green")

            uart.write("green")
            # uart.write(bytes([0xFF,0xFF,0x01,0x1]))

        elif data_handler["color"] == "yellow":
            yellow_pin.value(1)
            red_pin.value(0)
            green_pin.value(0)
            log("yellow")

            uart.write("yellow")
            # uart.write(bytes([0xFF,0xFF,0x01,0x2]))
        elif data_handler["color"] == "ping":  # 保留位,用于测试连接
            pass
        else:
            info = "JSON package valid key, invalid value"
            back_string = json.dumps(
                {
                    "error": True,
                    "info": info,
                }
            )
            log(info)
            s.sendto(back_string + "\r\n", addr)  # json包有效键，无效值

            continue

        back_string = json.dumps(
            {
                "error": False,
            }
        )
        s.sendto(back_string + "\r\n", addr)
finally:
    s.close()
