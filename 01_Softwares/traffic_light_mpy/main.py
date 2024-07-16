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
    # tft.fill(gc9a01.BLACK)


def center_display1(s,clear=False):
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


def center_display2(s,clear=False):
    if clear:
        tft.fill(gc9a01.BLACK)
    screen = tft.width()
    width = tft.write_len(noto_sans, s)
    if width and width < screen:
        col = tft.width() // 2 - width // 2
    else:
        col = 0

    row = tft.height() // 2
    tft.write(noto_sans, s, col, row, gc9a01.WHITE)


tft_init()
center_display1("TFT init",clear=True)

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
    center_display1("wifi connected",clear=True)
    sleep(1)
    ADDR = wlan.ifconfig()[0]
    center_display2(ADDR)
    sleep(1)
else:
    center_display1("wifi error",clear=True)

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind((ADDR, PORT))

center_display1(f"waiting",clear=True)
center_display2(f"{ADDR}:{PORT}")

try:
    data, addr = s.recvfrom(1024)
finally:
    s.close()

# while True:
#     data, addr = s.recvfrom(1024)
#     print(f"recv from {addr}-> {data}")
