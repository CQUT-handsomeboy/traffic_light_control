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

**最初的版本**，直接使用IO口驱动电路板，没有考虑到红绿灯的工作电压与IO口数量的问题。

### `Traffic_Light_Control_Upper`

交通信号灯上位机MQTT通信协议验证程序。


## `02_Hardwares`

~~**硬件工程**，第四版成功搞坏了一个ESP32C3。~~

![](./.asset/img1.png)

**由于PCB不管怎么焊接都会出现差错，为了快速成型，使用面包板与杜邦线方案，不再设计PCB。**

## `03_Documents`

**所有文档**。原理图与PCB，其中报废版本与过渡版本省略未传。