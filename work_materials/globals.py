from telegram.ext import Updater
from config import ProductionToken, request_kwargs

import pytz, tzlocal

updater = Updater(token=ProductionToken, request_kwargs=request_kwargs)

dispatcher = updater.dispatcher
job = updater.job_queue

POST_CHANNEL_ID = -1001184691738
CHAT_WARS_ID = 265204902

moscow_tz = pytz.timezone('Europe/Moscow')
try:
    local_tz = tzlocal.get_localzone()
except pytz.UnknownTimeZoneError:
    local_tz = pytz.timezone('Europe/Andorra')
