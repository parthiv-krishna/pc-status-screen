# pc-status-screen

Live status of PC on an Adafruit PyPortal

## Installation
- Install CircuitPython on the PyPortal as explained in the [Adafruit guide](https://learn.adafruit.com/adafruit-pyportal/install-circuitpython)
- Install CircuitPython libraries as explained in the [Adafruit guide](https://learn.adafruit.com/adafruit-pyportal/pyportal-circuitpython-setup)
    - `adafruit_adt7410` (temperature sensor)
    - `adafruit_registers` (needed for `adafruit_adt7410`)
- Clone the repository onto the PyPortal. The directory structure should look something like: 
```
lib/
    adafruit_adt7410.mpy
    adafruit_registers/
    ...
config.json
driver.py
main.py
README.md
...
```
- Clone the repository onto the host machine
- Use `nix-shell` to get python with the appropriate libraries on the host machine
    - If not using `nix`, use `pip` or your preferred method to install `psutil` and `pyserial`

## Setup
- [main.py](./main.py) contains the code that runs on the PyPortal
- [main_config.json](./main_config.json) contains the configuration parameters for `main.py`. You will need to update these on the PyPortal to match your system. Note `"CPU_CORES"` is logical cores (i.e. threads).
    - You can leave `"BAUDRATE"` as-is; it just needs to match the value in `driver_config.json`
- [driver.py](./driver.py) contains the code that runs on the host machine
- [driver_config.json](./driver_config.json) contains the configuration parameters for `driver.py`. You will need to update these on the host machine to match your system.
    - You can leave `"BAUDRATE"` as-is; it just needs to match the value in `main_config.json`
    - `"REFRESH_SECONDS"` is how often the driver will poll hardware stats. You can probably leave this at 2.
    - For `"TEMP_CPU"` and `"TEMP_GPU"`, run the following in Python to print all hardware thermometers in your system. Populate the appropriate names into the fields.
    ```
    import psutil
    print(psutil.sensors_temperatures.keys())
    ```

