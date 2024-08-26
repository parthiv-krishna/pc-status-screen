import adafruit_adt7410
import board
import busio
import displayio
import json
import supervisor
import time

CONFIG_PATH = "./main_config.json"

# onboard temperature sensor for case air temp
def airtemp_init():
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    adt = adafruit_adt7410.ADT7410(i2c_bus, address=0x48)
    adt.high_resolution = True
    return adt

def display_on(display):
    display.brightness = 1

def display_off(display):
    display.brightness = 0

def display_init(config):
    display = board.DISPLAY
    display.rotation = config["display_ROTATION"]

    display_on(display)

    return board.DISPLAY

def display_update(display, stats, config):
    display_on(display)

def main(config):
    display = display_init(config["CPU_CORES"])
    airtemp_sensor = init_airtemp()

    last_update = time.time()
    while True:
        curr_time = time.time()

        if supervisor.runtime.serial_bytes_available:
            # receive data from serial
            stats_bytes = input().strip()
            print(f"Received: {value}\n")
            stats = json.loads(stats)

            # read the temperature sensor
            stats["TEMP_AIR"] = airtemp_sensor.temperature

            display_update(display, stats, config)

            last_update = curr_time

        if (curr_time - last_update).total_seconds > config["TIMEOUT_SECONDS"]:
            # timeout: haven't heard from driver in a while
            display_off(display)

if __name__ == "__main__":
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    main(config)
