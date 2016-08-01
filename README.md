# Intel Edison-based Gateway
A gateway design based on Intel Edison, which features two 802.15.4
radios, Ethernet controller, micro SD slot, built-in Wifi and BLE radios.



<img src="https://raw.githubusercontent.com/lab11/IntelEdisonGateway/master/images/edison_front.png" alt="Gateway Edison" width="25%;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://raw.githubusercontent.com/lab11/IntelEdisonGateway/master/images/edison_case_1000x629.jpg" alt="Gateway Edison" width="35%;">

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

