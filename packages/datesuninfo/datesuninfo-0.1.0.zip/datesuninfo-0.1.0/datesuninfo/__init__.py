from __future__ import print_function

import datetime

import ephem  # pip install pyephem
import pytz


__all__ = ['date_sun_info']


def date_sun_info(latitude=None, longitude=None, calc_date=None):
    """Given a location and date, returns dict of sunrise/sunset/etc times.

    Args:
        latitude: A string containing the latitude (between -90.0 and 90.0)
        longitude: A string containing the longitude (between -180.0 and 180.0)
        calc_date: A timezone aware datetime object. Use `pytz` to set timezone.

    Returns:
        A dict of timezone aware datetime objects representing various sunrise/sunset events.

        >>> print(result.keys())
        ['civil_twilight_end', 'nautical_twilight_end', 'transit', 'previous_sunset',
         'sunset', 'next_sunrise', 'astronomical_twilight_begin', 'astronomical_twilight_end',
         'civil_twilight_begin', 'sunrise', 'nautical_twilight_begin']
    """

    # Initialize the location
    latitude = latitude or '35.3484055'  # Moore, OK, USA  @35.3484055,-97.48163
    longitude = longitude or '-97.48163'

    # No calc_date given? Start fresh with utcnow (shifted to US/Central to match lat,lon)
    if calc_date is None:
        calc_date = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Central'))
    # Convert any date objects to datetime.
    if isinstance(calc_date, datetime.date) and not isinstance(calc_date, datetime.datetime):
        calc_date = datetime.datetime(calc_date.year, calc_date.month, calc_date.day)
    # No time zone? assume UTC
    if calc_date.tzinfo is None or calc_date.tzinfo.utcoffset(calc_date) is None:
        calc_date = calc_date.replace(tzinfo=pytz.utc)

    # Find the first second of the day of calc_date
    start_date = datetime.datetime(calc_date.year, calc_date.month, calc_date.day, 0, 0, 0)
    # Set the start_date time zone to match the calc_date time zone
    start_date = calc_date.tzinfo.localize(start_date)

    results = dict()

    # Create an ephem observer object with our location and date
    observer = ephem.Observer()
    observer.lat = latitude
    observer.lon = longitude
    observer.date = start_date.astimezone(pytz.utc)  # shift start_date to utc for use with ephem

    # Set pressure to 0.0 to match the U.S. Naval Observatory calculation procedure
    observer.pressure = 0.0  # Defaults to 1010.0

    # Find the Sun transit time (solar noon) and update observer date for future calculations
    results['transit'] = observer.next_transit(ephem.Sun()).datetime()
    observer.date = results['transit']

    # Calculate sunrise, sunset (horizon '-0:34')
    observer.horizon = '-0:34'
    results['previous_sunset'] = observer.previous_setting(ephem.Sun()).datetime()
    results['sunrise'] = observer.previous_rising(ephem.Sun()).datetime()
    results['sunset'] = observer.next_setting(ephem.Sun()).datetime()
    results['next_sunrise'] = observer.next_rising(ephem.Sun()).datetime()

    # Calculate civil twilight (horizon @ -6)
    observer.horizon = '-6'
    results['civil_twilight_begin'] = observer.previous_rising(ephem.Sun(), use_center=True).datetime()
    results['civil_twilight_end'] = observer.next_setting(ephem.Sun(), use_center=True).datetime()

    # Calculate nautical twilight (horizon @ -12)
    observer.horizon = '-12'
    results['nautical_twilight_begin'] = observer.previous_rising(ephem.Sun(), use_center=True).datetime()
    results['nautical_twilight_end'] = observer.next_setting(ephem.Sun(), use_center=True).datetime()

    # Calculate astronomical twilight (horizon @ -18) (Earliest and latest light visible)
    observer.horizon = '-18'
    results['astronomical_twilight_begin'] = observer.previous_rising(ephem.Sun(), use_center=True).datetime()
    results['astronomical_twilight_end'] = observer.next_setting(ephem.Sun(), use_center=True).datetime()

    for key in results:
        # Everything ephem does is in utc, so add the time zone to the results
        results[key] = results[key].replace(tzinfo=pytz.utc)
        # Shift the results to match the time zone provided by calc_date
        results[key] = results[key].astimezone(calc_date.tzinfo)

    return results


def main():
    print('DateSunInfo:')
    print(date_sun_info())
