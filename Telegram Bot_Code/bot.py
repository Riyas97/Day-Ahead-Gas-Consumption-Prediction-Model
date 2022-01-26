import logging
import logging.config
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters
)

from constant import *
from misc import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


past_consumption = pd.read_csv('Question_2_dataset.csv', index_col='localminute', parse_dates=True, date_parser=lambda col: pd.to_datetime(col, utc=True))


def check_consumption(update, context):
    telegram_id = get_telegram_user(update)
    house_id = get_household_user(telegram_id)
    temp_file_save_path=f"./images/{house_id}.png"
    
    household_consumption = past_consumption[past_consumption['dataid'] == house_id]
    household_consumption = household_consumption.reset_index()

    plot_consumption(household_consumption, temp_file_save_path)
    context.bot.send_photo(chat_id=telegram_id, photo=open(temp_file_save_path, 'rb'))


def get_daily_forecast(update, context):
    telegram_id = get_telegram_user(update)
    house_id = get_household_user(telegram_id)
    temp_file_save_path=f"./images/{house_id}.png"
    # model_path = f'./models/{house_id}.sav'
    # model = pickle.load(open(model_path, 'rb'))

    now, future = nearest_day()
    test_df = get_samples(now, future, sampling_period=DAY)
    # test_df['predicted_meter_value'] = model.predict(test_df)
    # plot_prediction(test_df, temp_file_save_path)
    # context.bot.send_photo(chat_id=telegram_id, photo=open(temp_file_save_path, 'rb'))



def get_next_day_forecast(update, context):
    telegram_id = get_telegram_user(update)
    house_id = get_household_user(telegram_id)
    temp_file_save_path=f"./images/{house_id}.png"
    # model_path = f'./models/{house_id}.sav'
    # model = pickle.load(open(model_path, 'rb'))

    now, future = one_day_from_now()
    test_df = get_samples(now, future, sampling_period=DAY)
    # test_df['predicted_meter_value'] = model.predict(test_df)
    # plot_prediction(test_df, temp_file_save_path)
    # context.bot.send_photo(chat_id=telegram_id, photo=open(temp_file_save_path, 'rb'))


def get_weekly_forecast(update, context):
    telegram_id = get_telegram_user(update)
    house_id = get_household_user(telegram_id)
    temp_file_save_path=f"./images/{house_id}.png"
    
    model_path = f'./models/{house_id}.sav'
    model = pickle.load(open(model_path, 'rb'))

    now, future = nearest_week()
    test_df = get_samples(now, future, sampling_period=WEEK)
    test_df['predicted_meter_value'] = model.predict(test_df)
    plot_prediction(test_df, temp_file_save_path)
    context.bot.send_photo(chat_id=telegram_id, photo=open(temp_file_save_path, 'rb'))


def get_next_week_forecast(update, context):
    telegram_id = get_telegram_user(update)
    house_id = get_household_user(telegram_id)
    temp_file_save_path=f"./images/{house_id}.png"
    model_path = f'./models/{house_id}.sav'
    
    model = pickle.load(open(model_path, 'rb'))

    now, future = one_week_from_now()
    test_df = get_samples(now, future, sampling_period=WEEK)
    test_df['predicted_meter_value'] = model.predict(test_df)
    plot_prediction(test_df, temp_file_save_path)
    context.bot.send_photo(chat_id=telegram_id, photo=open(temp_file_save_path, 'rb'))


def get_monthly_forecast(update, context):
    telegram_id = get_telegram_user(update)
    house_id = get_household_user(telegram_id)
    temp_file_save_path=f"./images/{house_id}.png"
    model_path = f'./models/{house_id}.sav'
    
    model = pickle.load(open(model_path, 'rb'))
    now, future = nearest_month()
    test_df = get_samples(now, future, sampling_period=MONTH)
    test_df['predicted_meter_value'] = model.predict(test_df)
    plot_prediction(test_df, temp_file_save_path)
    context.bot.send_photo(chat_id=telegram_id, photo=open(temp_file_save_path, 'rb'))

    update.message.reply_text('Feature has not been implemented!',
                              reply_markup=COMMANDS_KEYBOARD)

def get_next_month_forecast(update, context):
    telegram_id = get_telegram_user(update)
    house_id = get_household_user(telegram_id)
    temp_file_save_path=f"./images/{house_id}.png"
    model_path = f'./models/{house_id}.sav'
    
    model = pickle.load(open(model_path, 'rb'))
    now, future = one_month_from_now()
    test_df = get_samples(now, future, sampling_period=MONTH)
    test_df['predicted_meter_value'] = model.predict(test_df)
    plot_prediction(test_df, temp_file_save_path)
    context.bot.send_photo(chat_id=telegram_id, photo=open(temp_file_save_path, 'rb'))

    update.message.reply_text('Feature has not been implemented!',
                              reply_markup=COMMANDS_KEYBOARD)

def report_problem(update, context):
    telegram_id = get_telegram_user(update)
    house_id = get_household_user(telegram_id)
    
    update.message.reply_text('Feature has not been implemented!',
                              reply_markup=COMMANDS_KEYBOARD)
    pass


def message_handler(update, conßßtext):
    user = get_telegram_user(update)
    user_answer = update.message.text
    house_id = get_household_user(telegram_id)
    if (house_id == -1):
    ß
    else:
    
def login_handler(update, context):
    telegram_id = get_telegram_user(update)
    house_id = get_household_user(telegram_id)
    if (house_id != -1):
        update.message.reply_text("Hey there, you are already logged in!")
    else:
        update.message.reply_text("Hey there, what is your house id?")
def help_handler(update, context):
    update.message.reply_text('Check out the various functions below to start your Smart Home Experience!',
                              reply_markup=COMMANDS_KEYBOARD)
    

def error_handler(update, context):
    error = f'Update {update} caused error {context.error}'
    logger.warning(error)


def main():
    if (LOCAL):
        updater = Updater(LOCAL_TOKEN, use_context=True)
    else:
        updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("login", login_handler))
    dp.add_handler(CommandHandler("start", help_handler))
    dp.add_handler(CommandHandler("help", help_handler))
    dp.add_handler(CommandHandler("check_consumption", check_consumption))
    dp.add_handler(CommandHandler("get_daily", get_daily_forecast))
    dp.add_handler(CommandHandler("get_next_day", get_next_day_forecast))
    dp.add_handler(CommandHandler("get_weekly", get_weekly_forecast))
    dp.add_handler(CommandHandler("get_next_week", get_next_week_forecast))
    dp.add_handler(CommandHandler("get_monthly", get_monthly_forecast))
    dp.add_handler(CommandHandler("get_next_month", get_next_month_forecast))
    dp.add_handler(CommandHandler("report_problem", report_problem))
    dp.add_handler(MessageHandler(Filters.text, message_handler))
    dp.add_error_handler(error_handler)

    if (LOCAL):
        updater.start_polling()
    else:
        updater.start_webhook(listen="0.0.0.0",
                              port=int(PORT),
                              url_path=TOKEN,
                              webhook_url=f'https://cikgu-jamal-bot.herokuapp.com/{TOKEN}')

    updater.idle()


main()
