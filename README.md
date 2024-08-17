[![SVG Banners](https://svg-banners.vercel.app/api?type=glitch&text1=Traffic🤔Light&width=900&height=200)](https://github.com/CQUT-handsomeboy/traffic_light_control)

![Static Badge](https://img.shields.io/badge/License-AGPL3-green) ![Static Badge](https://img.shields.io/badge/Language-Arduino-red) ![Static Badge](https://img.shields.io/badge/Language-Micropython-red) ![Static Badge](https://img.shields.io/badge/Author-CQUT_handsomeboy-black)

# References

![IRF520_connection_demo](http://hobbycomponents.com/images/forum/IFR520_MOSFET_Module_DC_Motor_Example.png)

![ESP32_connection](./.asset/img2.png)

[IRF520](https://forum.hobbycomponents.com/viewtopic.php?f=76&t=1872)

[ESP32S3-TOUCHLCD](https://www.waveshare.net/wiki/ESP32-S3-Touch-LCD-1.28)

# Explanations

## `01_Softwares`

**软件工程**。

### `sketch_may29a`

**最初的版本**，使用Arduino，直接使用IO口驱动电路板，没有考虑到红绿灯的工作电压与IO口数量的问题。

### `Traffic_Light_Control_Upper`

交通信号灯上位机MQTT通信协议验证程序。

### `traffic_light_mpy`

为带有TFT的ESP32S3编写的MicroPython版本，参考微雪例程。

### `traffic_light_mpy2`

为不带有TFT屏幕的ESP32编写的MicroPython版本，增加了很多异常处理机制与执行状态。


## `02_Hardwares`

转接板第五版设计完成。*（评估版）*

1. 使用PCF8574可以实现对大电流负载的灯泡的驱动能力，供电为CH340提供的3V3。
2. IO都各自引出了公母排针，方便接入不同的杜邦线。
3. CH340 TTL转USB 引出 Type-C更方便地将信息传输给上位机。
4. 添加3个按键，使用去耦电容硬件消抖。

![](./.asset/img1.png)

## `03_Documents`

**所有文档**。原理图与PCB，其中报废版本与过渡版本省略未传。