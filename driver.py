import argparse
import json
import psutil
import serial
import serial.tools.list_ports
import time
import typing

BYTES_PER_GB = 2 ** 30

def get_stats(config: dict[str, typing.Any]):
    stats = {}

    # cpu usage
    cpu_percents = psutil.cpu_percent(percpu=True)
    stats["CPU_UTIL"] = cpu_percents

    # memory usage
    ram_used_b = psutil.virtual_memory().used
    ram_used_gb = round(ram_used_b / BYTES_PER_GB, 2)
    stats["RAM"] = ram_used_gb

    # hardware temperatures
    temps = psutil.sensors_temperatures()
    cpu_temp_c = temps[config["TEMP_CPU"]][0].current if config["TEMP_CPU"] in temps else 0
    gpu_temp_c = temps[config["TEMP_GPU"]][0].current if config["TEMP_GPU"] in temps else 0
    stats["TEMP_CPU"] = cpu_temp_c
    stats["TEMP_GPU"] = gpu_temp_c

    return stats

def main(config_path: str, port: str | None):
    args = parser.parse_args()
    with open(config_path, 'r') as f:
        config = json.load(f)

    if port is None:
        ports = serial.tools.list_ports.comports()
        if len(ports) != 1:
            raise RuntimeError(f"Could not auto-assign port. Detected ports: {ports}")
        port = ports[0]

    # initialize cpu_percent
    _ = psutil.cpu_percent(percpu=True)
    with(serial.Serial(port, config["BAUDRATE"])) as ser:
        while True:
            stats = get_stats(config)
            stats_bytes = json.dumps(stats).encode()
            ser.write(stats_bytes)
            time.sleep(config["REFRESH_SECONDS"])
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Path to driver_config.json", default="./driver_config.json")
    parser.add_argument("-p", "--port", help="Serial port where PyPortal is connected. If not provided, will auto-detect", default=None)

    args = parser.parse_args()
    main(args.config, args.port)
