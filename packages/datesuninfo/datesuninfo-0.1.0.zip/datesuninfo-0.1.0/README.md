# datesuninfo

Mimics PHPs `date_sun_info()` using python and `ephem`.

Sunrise, solar noon, sunset, and twilight start/end times for a given location and datetime.

## Example

```python
import datetime
import pytz
from datesuninfo import date_sun_info

# Get the current time in utc and assign it the pytz utc time zone
calc_date = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
# Shift the calc_date to Central time zone
calc_date = calc_date.astimezone(pytz.timezone('US/Central'))
# Get the date_sun_info for Moore, OK using the current time in the central time zone.
sun_info = date_sun_info(latitude='35.3484055', longitude='-97.48163', calc_date=calc_date)

print('Sunrise: {0}'.format(sun_info['sunrise']))
print('Solar Noon: {0}'.format(sun_info['transit']))
print('Sunset: {0}'.format(sun_info['sunset']))
print(sun_info.keys())
```
outputs:
```
Sunrise: 2016-02-26 07:03:57.190347-06:00
Solar Noon: 2016-02-26 12:42:50.328314-06:00
Sunset: 2016-02-26 18:22:14.118211-06:00
['civil_twilight_end', 'nautical_twilight_end', 'transit', 'previous_sunset', 'sunset', 'next_sunrise', 'astronomical_twilight_begin', 'astronomical_twilight_end', 'civil_twilight_begin', 'sunrise', 'nautical_twilight_begin']
```

## History

This is a functional work-in-progress.  I use it for personal projects; that is the purpose it serves.

The last time this project saw love was early April 2016.