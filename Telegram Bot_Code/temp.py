import pandas as pd
from datetime import datetime, timedelta
import holidays

us_holidays = holidays.UnitedStates()

def split_minute_time(row):
    new_row = row
    timestamp = row['localminute']
    new_row['weekday'] = timestamp.weekday()
    holiday_name = us_holidays.get(timestamp)
    if (holiday_name == None):
        new_row['is_holiday'] = 0
    else:
        new_row['is_holiday'] = 1

    if (new_row['weekday'] >= 5):
        new_row['is_weekday'] = 0
    else:
        new_row['is_weekday'] = 1

    if (timestamp.hour >= 9 and timestamp.hour <= 17):
        new_row['is_office_hour'] = 1
    else:
        new_row['is_office_hour'] = 0

    if (timestamp.hour >= 0 and timestamp.hour <= 9):
        new_row['is_sleeping'] = 1
    else:
        new_row['is_sleeping'] = 0

    new_row['month'] = timestamp.month
    new_row['year'] = timestamp.year
    new_row['date'] = timestamp.day
    new_row['hour'] = timestamp.hour

    return new_row

now = datetime.now()
end = now+timedelta(days=1)


vals = pd.date_range(now, end, freq='H')

df = pd.DataFrame(vals, columns=['localminute'])

new_df = df.apply(lambda x : split_minute_time(x), axis=1)

print(new_df)