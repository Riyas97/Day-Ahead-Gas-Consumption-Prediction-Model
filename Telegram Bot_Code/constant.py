import os
from telegram import ReplyKeyboardMarkup

LOCAL = True
PORT = int(os.environ.get('PORT', 8443))
TOKEN = '2056033712:AAHkx_bdOglX4Yo6i7DaB3_bmm1OYjEvla8'
LOCAL_TOKEN = '2136835137:AAF7tK3-8by6Yo7LUBlxRBo3xVMx0ESaZgc'

MIN_CHANCE = 1
QUESTION_SIZE = 10
PERFECT_SCORE = 1.0

COMMANDS_KEYBOARD = ReplyKeyboardMarkup([['/login', '/check_consumption'], ['/get_daily', '/get_next_day'], [
                                        '/get_weekly', '/get_next_week'], ['/get_monthly', '/get_next_month'], ['/report_problem', '/help']])

DB_URL = "postgresql+psycopg2://melcnjdvxyzmeg:ae85c0c13ad93a11b1c696de8c56b833d8c643c9ed1606eaeb03354d14f61fc8@ec2-23-23-133-10.compute-1.amazonaws.com:5432/dai15is5fdpqk8"

DAY, WEEK, MONTH = range(0, 3)