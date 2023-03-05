#!/usr/bin/env python3

import time
import lgpio
#from gpiozero import OutputDevice


ON_THRESHOLD = 75  # (degrees Celsius) Fan kicks on at this temperature.
OFF_THRESHOLD = 55  # (degress Celsius) Fan shuts off at this temperature.
SLEEP_INTERVAL = 5  # (seconds) How often we check the core temperature.
GPIO_PIN = 18  # Which GPIO pin you're using to control the fan.


def get_temp():
    """Get the core temperature.

    Read file from /sys to get CPU temp in temp in C *1000

    Returns:
        int: The core temperature in thousanths of degrees Celsius.
    """
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        temp_str = f.read()

    try:
        return int(temp_str) / 1000
    except (IndexError, ValueError,) as e:
        raise RuntimeError('Could not parse temperature output.') from e

if __name__ == '__main__':
    # Validate the on and off thresholds
    if OFF_THRESHOLD >= ON_THRESHOLD:
        raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

    h = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_output(h, GPIO_PIN)
    is_enabled = False

    while True:
        temp = get_temp()
        print(temp)

        # Start the fan if the temperature has reached the limit and the fan
        # isn't already running.
        # NOTE: `fan.value` returns 1 for "on" and 0 for "off"
        if temp > ON_THRESHOLD and not is_enabled:
            #fan.on()
            lgpio.gpio_write(h, GPIO_PIN, 1)
            is_enabled = True
            print("On")

        # Stop the fan if the fan is running and the temperature has dropped
        # to 10 degrees below the limit.
        elif is_enabled and temp < OFF_THRESHOLD:
            #fan.off()
            lgpio.gpio_write(h, GPIO_PIN, 0)
            is_enabled = False
            print("Off")

        time.sleep(SLEEP_INTERVAL)
