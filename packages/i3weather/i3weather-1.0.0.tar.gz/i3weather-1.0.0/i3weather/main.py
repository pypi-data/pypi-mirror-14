import argparse
import configparser
import json
import pyowm
import string
import os
import sys

from i3weather.log import logger


def error(message, *args):
    logger.critical('ERROR: ' + message, *args)
    sys.exit(1)


def inject_weather(info, owm, location, str_format):
    obs = owm.weather_at_place(location)
    weather = obs.get_weather()
    wind = weather.get_wind()
    loc = obs.get_location()
    values = {
        'temp': weather.get_temperature('fahrenheit')['temp'],
        'pressure': weather.get_pressure()['press'],
        'status': string.capwords(weather.get_detailed_status()),
        'short_status': string.capwords(weather.get_status()),
        'wind_dir': wind['deg'],
        'wind_speed': wind['speed'],
        'location': loc.get_name(),
    }

    info.insert(0, {
        'name': 'weather',
        'full_text': str_format.format(**values)
    })
    return info


def print_line(message):
    sys.stdout.write(message + '\n')
    sys.stdout.flush()


def read_line():
    try:
        line = sys.stdin.readline().strip()
        if not line:
            sys.exit(3)
        return line
    except KeyboardInterrupt:
        sys.exit()


def loop_weather(owm, location, str_format):
    # Version line
    print_line(read_line())
    # Line starting infinite json array
    print_line(read_line())

    while True:
        line, prefix = read_line(), ''
        if line.startswith(','):
            line, prefix = line[1:], ','

        line = inject_weather(json.loads(line), owm, location, str_format)
        print_line(prefix + json.dumps(line))


def main():
    parser = argparse.ArgumentParser(
        'Adds OpenWeatherMap information to i3status'
    )
    parser.add_argument('--config', default='~/.i3weather')
    args = parser.parse_args()

    try:
        with open(os.path.expanduser(args.config)) as fh:
            config = configparser.SafeConfigParser()
            config.read_file(fh)
    except FileNotFoundError:
        error('Could not find configuration file at %s', args.config)

    try:
        api_key = config.get('owm', 'api_key')
    except configparser.NoOptionError:
        error('API key is not set in config')

    owm = pyowm.OWM(api_key)
    try:
        owm.is_API_online()
    except pyowm.exceptions.api_call_error.APICallError:
        error('Invalid API key in config')

    try:
        str_format = config.get('i3weather', 'format')
    except configparser.NoOptionError:
        str_format = '{short_status} - {temp} F - {wind_speed} Mph'

    try:
        location = config.get('owm', 'location')
    except configparser.NoOptionError:
        error('No location set in config')

    loop_weather(owm, location, str_format)
