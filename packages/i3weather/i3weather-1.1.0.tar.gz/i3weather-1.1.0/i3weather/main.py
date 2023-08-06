import argparse
import configparser
import json
import os
import pyowm
import string
import sys

from i3weather.log import logger


DEFAULT_FORMAT = '{short_status} - {temp} F - {wind_speed} Mph'


def error(message, *args):
    logger.critical('ERROR: ' + message, *args)
    sys.exit(1)


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


def get_weather(info, owm, location, str_format, unit):
    obs = owm.weather_at_place(location)
    weather = obs.get_weather()
    wind = weather.get_wind()
    loc = obs.get_location()
    values = {
        'temp': weather.get_temperature(unit)['temp'],
        'temp_unit': unit,
        'pressure': weather.get_pressure()['press'],
        'status': string.capwords(weather.get_detailed_status()),
        'short_status': string.capwords(weather.get_status()),
        'wind_dir': wind['deg'],
        'wind_speed': wind['speed'],
        'location': loc.get_name(),
    }

    return {
        'name': 'weather',
        'full_text': str_format.format(**values)
    }
    return info


def loop_weather(owm, location, str_format, unit, position):
    # Version line
    print_line(read_line())
    # Line starting infinite json array
    print_line(read_line())

    while True:
        line, prefix = read_line(), ''
        if line.startswith(','):
            line, prefix = line[1:], ','

        j = json.loads(line)
        weather = get_weather(j, owm, location, str_format, unit)
        j.insert(position, weather)
        print_line(prefix + json.dumps(j))


def get_value(config, section, key, default=None):
    try:
        return config.get(section, key)
    except (configparser.NoOptionError, configparser.NoSectionError) as ex:
        if default is not None:
            return default
        raise ex


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
        location = config.get('owm', 'location')
    except configparser.NoOptionError:
        error('No location set in config')

    str_format = get_value(config, 'i3weather', 'format', DEFAULT_FORMAT)
    temp_unit = get_value(config, 'owm', 'temp_unit', 'fahrenheit').lower()
    if temp_unit not in ('fahrenheit', 'celsius'):
        error('Invalid temperature unit %s', temp_unit)

    position = int(get_value(config, 'i3weather', 'position', 0))
    loop_weather(owm, location, str_format, temp_unit, position)
