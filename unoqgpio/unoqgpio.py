import subprocess
import os

INPUT = 0
OUTPUT = 1
LOW = 0
HIGH = 1

LED3_R = 1000
LED3_G = 1001
LED3_B = 1002

LED4_R = 2000
LED4_G = 2001
LED4_B = 2002

pins = {
    0: "PB7",
    1: "PB6",
    2: "PB3",
    3: "PB0",
    4: "PA12",
    5: "PA11",
    6: "PB1",
    7: "PB2",
    8: "PB4",
    9: "PB8",
    10: "PB9",
    11: "PB15",
    12: "PB14",
    13: "PB13",
    14: "PA4",
    15: "PA5",
    16: "PA6",
    17: "PA7",
    18: "PC1",
    19: "PC0",
    20: "PB11",
    21: "PB10",
    LED3_R: "PH10",
    LED3_G: "PH11",
    LED3_B: "PH12",
    LED4_R: "PH13",
    LED4_G: "PH14",
    LED4_B: "PH15",
}

def __openocd(cmd):
    return subprocess.run([
        "/opt/openocd/bin/openocd",
        "-d0",
        "-s", "/opt/openocd/",
        "-f", "openocd_gpiod.cfg",
        "-c", "init",
        "-c", cmd,
        "-c", "exit"
    ], capture_output=True, shell=False)
        
def __peribase(pin):
    mapped = pins[pin]
    return 0x42020000 + 0x400 * (ord(mapped[1]) - ord('A'))
    
def __pinnum(pin):
    mapped = pins[pin]
    return int(mapped[2:])

def pinMode(pin, state):
    reg = str(__peribase(pin))
    num = str(__pinnum(pin))
    if state == OUTPUT:
        __openocd('halt; write_memory ' + reg + ' 32 [ expr "([read_memory ' + reg + ' 32 1] & ~(0x3 << (2 * ' + num + '))) | (0x1 << (2 * ' + num + '))" ]; continue')
    else:
        __openocd('halt; write_memory ' + reg + ' 32 [ expr "([read_memory ' + reg + ' 32 1]) | (0x3 << (2 * ' + num + '))" ]; continue')

def digitalWrite(pin, value):
    reg = str(__peribase(pin) + 0x18)
    num = str(__pinnum(pin))
    if value == LOW:
        __openocd('write_memory ' + reg + ' 32 [ expr "1 << (' + num + ' + 16)" ]')
    else:
        __openocd('write_memory ' + reg + ' 32 [ expr "1 << (' + num + ' + 0)" ]')
    
def digitalRead(pin):
    reg = str(__peribase(pin) + 0x10)
    out = __openocd('read_memory ' + reg + ' 32 1')
    val = out.stderr.splitlines()[-1]
    val_int = int(val[2:], 16)
    return int(val_int & (1 <<  __pinnum(pin)) != 0)
