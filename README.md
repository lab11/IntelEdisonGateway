# Intel Edison-based Gateway
<!--
A gateway design based on Intel Edison, which features two 802.15.4
radios, Ethernet controller, micro SD slot, built-in Wifi and BLE radios.


<img src="https://raw.githubusercontent.com/lab11/IntelEdisonGateway/master/images/edison_front.png" alt="Gateway Edison" width="25%;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://raw.githubusercontent.com/lab11/IntelEdisonGateway/master/images/edison_case_1000x629.jpg" alt="Gateway Edison" width="35%;">
-->
Second generation of Intel Edison Gateway. The gateway supports a wide range 
of radios / connectivity including 802.15.4, Wifi, BLE, Ethernet, LTE and GPS.
The precompiled linux kernel [image](https://github.com/lab11/IntelEdisonGateway/tree/master/kernel_patch/3.10.98/kernel_image) 
(based on Intel release, version 3.10.98) comes with necessary drivers for the
cellular modem and Ethernet controller.

![Front view]<img src="https://github.com/lab11/IntelEdisonGateway/blob/master/images/edison-v3-front.png" alt="Gateway Edison" width="25%;"> ![With enclosure]<img src="https://github.com/lab11/IntelEdisonGateway/blob/master/images/edison-v3-enclosure.png" alt="Gateway Edison Enclosure" width="25%;">

The onboard cellular modem is [NimbeLink Skywire 4G LTE](http://nimbelink.com/skywire-cellular-modem-lte/),
which supports 100 Mb downlink and 50 Mb uplink and integrated GPS radio.
The cellular radio speaks Qualcomm MSM Interface (QMI), which allows the radio
to be mounted as a network adapter directly in Linux with [libqmi](https://www.freedesktop.org/wiki/Software/libqmi/).

The board is designed to fit in the off-the-shelf extruded aluminum enclosure 
[B2-080BK](http://www.boxenclosures.com/category/product_details.html?product__id=258909).


<!--
[LGSInnovations](https://github.com/LGSInnovations/Edison-Ethernet) has great
documentation of how to use LAN9512 on ubilinux.
The kernel module for smsc95xx (Ethernet controller) can be found [here](https://github.com/LGSInnovations/Edison-Ethernet/releases),
as well as the [installation guide](https://github.com/LGSInnovations/Edison-Ethernet/blob/master/guides/installation.md).

[edison_front]: https://github.com/lab11/IntelEdisonGateway/blob/master/images/edison_front.png "Front"

Pin Out
-------

Header on the left side of the PCB:

| Pin | Signal |   | Signal | Pin |
|-----|--------|---|--------|-----|
| 1   | MISO   |   | MOSI   | 2   |
| 3   | SCLK   |   | !CS1   | 4   |
| 5   | SDA    |   | SCL    | 6   |
| 7   | RX     |   | TX     | 8   |
| 9   | GP46   |   | GP45   | 10  |
| 11  | PA5    |   | GP44   | 12  |
| 13  | PA6    |   | PA3    | 14  |
| 15  | PA7    |   | PA4    | 16  |
| 17  | GND    |   | GND    | 18  |
-->


Pin Out
-------

Header on the left side of the PCB. This is changed from the previous version:

| Pin | Signal  |   | Signal  | Pin |
|-----|---------|---|---------|-----|
| 1   | VCC3.3  |   | VSYS3.9 | 2   |
| 3   | PA4     |   | PA5     | 4   |
| 5   | PA3     |   | GP46    | 6   |
| 7   | GND     |   | GND     | 8   |
| 9   | UART TX |   | UART RX | 10  |
| 11  | I2C SCL |   | I2C SDA | 12  |
| 13  | SPI CS1 |   | SPI CLK | 14  |
| 15  | MOSI    |   | MISO    | 16  |

