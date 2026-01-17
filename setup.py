from setuptools import find_packages, setup

setup(
    name = 'unoqgpio',
    packages = find_packages(include=['unoqgpio']),
    version = '0.1.0',
    description ='Python library allowing controlling digital ports of Arduino Uno Q from python script without need to communicate messages between MPU and MCU.',
    author = 'misaz',
    license = 'MIT',
)