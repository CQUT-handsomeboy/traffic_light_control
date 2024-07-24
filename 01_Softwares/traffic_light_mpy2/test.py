from machine import UART, Pin
from micropython import const
from time import sleep


def test_uart():
    TX_PIN_NUM = const(21)
    RX_PIN_NUM = const(20)

    uart = UART(1, 115200, rx=RX_PIN_NUM, tx=TX_PIN_NUM)

    while 1:
        uart.write("TEST\r\n")
        print("send!")
        sleep(1)


def test_pins():
    RED_PIN_NUM = const(1)
    GREEN_PIN_NUM = const(2)
    YELLOW_PIN_NUM = const(3)

    red_pin = Pin(RED_PIN_NUM, Pin.OUT)
    yellow_pin = Pin(YELLOW_PIN_NUM, Pin.OUT)
    green_pin = Pin(GREEN_PIN_NUM, Pin.OUT)

    while 1:
        red_pin.value(1)
        yellow_pin.value(0)
        green_pin.value(0)
        sleep(1)
        red_pin.value(0)
        yellow_pin.value(1)
        green_pin.value(0)
        sleep(1)
        red_pin.value(0)
        yellow_pin.value(0)
        green_pin.value(1)
        sleep(1)


def test_wifi():
    global nic
    import network

    nic = network.WLAN(network.STA_IF)

    nic.active(False)
    nic.active(True)
    

    nic.connect("cxs", "@12345678")
    
    ret = nic.isconnected()
    print(ret)


if __name__ == "__main__":
    test_wifi()
