from datetime import datetime, timedelta
import logging
from constant import *
import pandas as pd
import telegram
import time
import matplotlib.pyplot as plt
import seaborn as sns
import holidays
from sqlalchemy.engine.create import create_engine

sns.set_theme()
plt.ioff()

us_holidays = holidays.UnitedStates()
password_list = pd.read_csv('password_list.csv')
engine = create_engine(DB_URL)

# Gets the USER ID of the telegram user
def get_telegram_user(update):
    if update.message is not None:
        return update.message.from_user.id
    elif update.callback_query is not None:
        return update.callback_query.from_user.id
    return -1
    
# TODO
# Currently mapped to household 739
# Each telegram user will be mapped to a household
def get_household_user(telegram_id):
    try :
        df = pd.read_sql_table(telegram_id, con=engine)
    except Exception:
        return -1 
        
    return df.iloc['dataid']

# Gets the nearest day
def nearest_day():
    now = datetime.now()
    updated_time = now.replace(second=0, microsecond=0, minute=0, hour=now.hour)+timedelta(hours=24-now.hour)
    logging.info(f'\nTime now : {now}\nTime in nearest h: {updated_time}')
    return now, updated_time

# Gets one day from now
def one_day_from_now():
    now = datetime.now()
    updated_time = now.replace(second=0, microsecond=0)+timedelta(hours=24)
    logging.info(f'\nTime now : {now}\nTime in 1 h: {updated_time}')
    return now, updated_time

# Gets the nearest week 
def nearest_week():
    now = datetime.now()
    updated_time = now.replace(second=0, microsecond=0, minute=0, hour=0)+timedelta(days=7-now.weekday())
    logging.info(f'\nTime now : {now}\nTime in nearest week: {updated_time}')
    return now, updated_time

# Gets one week from now
def one_week_from_now():
    now = datetime.now()
    updated_time = now.replace(second=0, microsecond=0)+timedelta(days=7)
    logging.info(f'\nTime now : {now}\nTime in 1 week: {updated_time}')
    return now, updated_time

# TODO
# Gets nearest month
def nearest_month():
    now = datetime.now()
    updated_time = now.replace(second=0, microsecond=0, minute=0, hour=0)+timedelta(days=7-now.weekday())
    logging.info(f'\nTime now : {now}\nTime in nearest week: {updated_time}')
    return now, updated_time

# TODO
# Gets one month from now
def one_month_from_now():
    now = datetime.now()
    updated_time = now.replace(second=0, microsecond=0)+timedelta(days=7)
    logging.info(f'\nTime now : {now}\nTime in 1 week: {updated_time}')
    return now, updated_time

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

# TODO
# Creates a dataframe from start to end with the sampling interval
def get_samples(start, end, sampling_period=None):
    if (sampling_period == DAY):
        time_series = pd.date_range(start, end, freq='H')
        df = pd.DataFrame(time_series, columns=['localminute'])    
    elif (sampling_period == WEEK):
        time_series = pd.date_range(start, end, freq='D')
        df = pd.DataFrame(time_series, columns=['localminute'])    
    elif (sampling_period == MONTH):
        time_series = pd.date_range(start, end, freq='D')
        df = pd.DataFrame(time_series, columns=['localminute'])    
    else:
        logging.info("Did not input sampling period")
        return None
    
    df = df.apply(lambda x : split_minute_time(x), axis=1)
    return df
    

# Gets the chat ID of the conversation
def get_chat_id(update, context):
    chat_id = -1
    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id][1]

    return chat_id

# Adds a delay function to the message to look realistic
def add_typing(update, context):
    if not LOCAL:
        context.bot.send_chat_action(
            chat_id=get_chat_id(update, context),
            action=telegram.ChatAction.TYPING,
            timeout=1,
        )
        time.sleep(1)
    else:
        return

# Plots the past consumption
def plot_consumption(df, save_path):
    plt.scatter(df['localminute'], df['meter_value'])
    plt.xlabel('Date')
    plt.ylabel('Gas Consumption')
    plt.title('Your household gas consumption')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')

def plot_prediction(df, save_path):
    plt.scatter(df['localminute'], df['predicted_meter_value'])
    plt.xlabel('Date')
    plt.ylabel('Predicted Gas Consumption')
    plt.title('Your predicted household gas consumption')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
