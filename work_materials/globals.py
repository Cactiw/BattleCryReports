from telegram.ext import Updater
from config import ProductionToken, request_kwargs, psql_creditals

import pytz, tzlocal, psycopg2

updater = Updater(token=ProductionToken, request_kwargs=request_kwargs)

dispatcher = updater.dispatcher
job = updater.job_queue

conn = psycopg2.connect("dbname={0} user={1} password={2}".format(psql_creditals['dbname'], psql_creditals['user'], psql_creditals['pass']))
conn.set_session(autocommit = True)
cursor = conn.cursor()

POST_CHANNEL_ID = -1001184691738
CHAT_WARS_ID = 265204902

moscow_tz = pytz.timezone('Europe/Moscow')
try:
    local_tz = tzlocal.get_localzone()
except pytz.UnknownTimeZoneError:
    local_tz = pytz.timezone('Europe/Andorra')
