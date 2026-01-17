# UNO Q GPIO Direct Access Python Library

Python library allowing controlling digital ports of Arduino Uno Q from python script without need to communicate messages between MPU and MCU.

## Installation

Install library using following command:

```
pip3 install git+https://github.com/misaz/unoqgpio
```

## Example

```
from unoqgpio import *
from time import sleep

pinMode(LED4_G, OUTPUT)

while True:
	sleep(0.5)
	digitalWrite(LED4_G, LOW)
	sleep(0.5)
	digitalWrite(LED4_G, HIGH)
```

## Using in Arduino App Lab

Currently it do not work in Arduino App Lab, because App Lab runs python programs in docker and containerized programs do not have access to /dev/gpiochip1 which is used under the hood. You can run it directly in terminal instead. If Arduino adds support for passing /dev/gpiochip devices to containers, it will become possible to use it inside App Lab. It will still require some *hacks* though. 

## Notes

You should use every output pin exclusively from one side (Sketch vs Python). Never use single output pin in both scripts. Input pins you can safely read from both sketch and script. Also, if you use other peripheral on pins (for example, I2C sensor using Wire library), do not use these pins on Python side.

## Internals
I briefly described internals of this library and how it works in [blog at Element14 community](https://community.element14.com/products/arduino/b/blog/posts/arduino-uno-q-drive-mcu-pins-directly-from-mpu).