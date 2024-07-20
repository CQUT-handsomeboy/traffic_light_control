from machine import Pin, SPI


# WIFI
WIFI_SSID = "cxs"
WIFI_PASSWORD = "@12345678"
WIFI_RETRY_COUNT = 100
PORT = 12345

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
    ADDR = wlan.ifconfig()[0]
    print(ADDR)
else:
    pass


import socket
import json

from machine import UART

data_handler = None

red_pin = Pin(10,Pin.OUT)
yellow_pin = Pin(20,Pin.OUT)
green_pin = Pin(21,Pin.OUT)

uart = UART(1,115200,rx=9,tx=10)

while (1):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((ADDR, PORT))
        data, addr = s.recvfrom(1024)
        data_handler = json.loads(data)
        if data_handler["color"] == "red":
            red_pin.value(1)
            yellow_pin.value(0)
            green_pin.value(0)

            uart.write("red")

        elif data_handler["color"] == "green":
            green_pin.value(1)
            red_pin.value(0)
            yellow_pin.value(0)

            uart.write("green")

            
        elif data_handler["color"] == "yellow":
            yellow_pin.value(1)
            red_pin.value(0)
            green_pin.value(0)
        
            uart.write("yellow")
        
    finally:
        s.close()