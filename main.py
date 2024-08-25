import time
import board
import busio
import adafruit_adt7410

# rate at which to refresh the pyportal screen, in seconds
PYPORTAL_REFRESH = 2
board.DISPLAY.rotation = 90
board.DISPLAY.brightness = 1

# init. adt7410
i2c_bus = busio.I2C(board.SCL, board.SDA)
adt = adafruit_adt7410.ADT7410(i2c_bus, address=0x48)
adt.high_resolution = True

while True:
    # read the temperature sensor
    temperature = adt.temperature
    print(temperature)
    time.sleep(PYPORTAL_REFRESH)
