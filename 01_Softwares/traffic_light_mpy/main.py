from machine import Pin, SPI
import gc9a01  # type:ignore

from truetype import NotoSans_32 as noto_sans

WIFI_SSID = "cxs"
WIFI_PASSWORD = "@12345678"
WIFI_RETRY_COUNT = 100  # wifi重试连接次数
PORT = 12345


def tft_init():
    global tft
    tft = gc9a01.GC9A01(
        SPI(2, baudrate=80000000, polarity=0, sck=Pin(10), mosi=Pin(11)),
        240,
        240,
        reset=Pin(14, Pin.OUT),
        cs=Pin(9, Pin.OUT),
        dc=Pin(8, Pin.OUT),
        backlight=Pin(2, Pin.OUT),
        rotation=0,
        buffer_size=16 * 32 * 2,
    )

    tft.init()


def center_display(s, clear=False):
    if clear:
        tft.fill(gc9a01.BLACK)
    tft.fill(gc9a01.BLACK)
    screen = tft.width()
    width = tft.write_len(noto_sans, s)
    if width and width < screen:
        col = tft.width() // 2 - width // 2
    else:
        col = 0

    row = tft.height() // 2 - noto_sans.HEIGHT
    tft.write(noto_sans, s, col, row, gc9a01.WHITE)


tft_init()
center_display("TFT init", clear=True)

import network
from time import sleep


def connect_wifi():
    global wlan
    wlan = network.WLAN(network.STA_IF)

    wlan.active(True)

    if wlan.isconnected():
        return True

    wlan.active(False)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    count = 0
    while wlan.isconnected() == False and count < WIFI_RETRY_COUNT:
        sleep(0.5)
        count += 1

    if wlan.isconnected():
        return True
    else:
        return False


ret = connect_wifi()

if ret:
    center_display("wifi connected", clear=True)
    sleep(1)
    ADDR = wlan.ifconfig()[0]
    center_display(ADDR, clear=True)
    print(ADDR)
else:
    center_display("wifi error", clear=True)


import socket
import json

data_handler = None

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ADDR, PORT))
    data, addr = s.recvfrom(1024)
    data_handler = json.loads(data)
    

    center_display(f"recv", clear=True)
finally:
    s.close()
