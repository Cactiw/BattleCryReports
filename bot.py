from telegram.ext import CommandHandler, MessageHandler, Filters

import logging
import datetime
import re


from work_materials.globals import updater, dispatcher, job, POST_CHANNEL_ID, local_tz, moscow_tz, cursor, TEST_CHANNEL_ID
from work_materials.filters.report_filters import filter_correct_report, filter_incorrect_report, filter_not_forward_report, \
    filter_not_report, filter_old_battle_cry, filter_not_pm

#   Выставляем логгироввание
console = logging.StreamHandler()
console.setLevel(logging.INFO)

log_file = logging.FileHandler(filename='error.log', mode='a')
log_file.setLevel(logging.ERROR)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO, handlers=[log_file, console])

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Привет! Кинь мне форвард репорта с сработавшим Battle cry!")

def help(bot, update):
    response = "Этот бот служит для публикования результата использования скилла Battle Cry рыцарей 50+ уровней.\n" \
               "Для работы необходимо прислать форвард ответа @ChatWarsBot на команду "\
               "/report с наличием сработавшего скилла Battle Cry."
    bot.send_message(chat_id=update.message.chat_id, text = response)

def report_handling(bot, update):
    mes = update.message
    nickname = mes.text.partition("⚔")[0][:-1]
    inspired_by = mes.text.partition("Тебя вдохновил ")[2].splitlines()[0]
    message_datetime = local_tz.localize(update.message.forward_date).astimezone(tz=moscow_tz).replace(tzinfo = None)
    time = message_datetime - message_datetime.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    if time < datetime.timedelta(hours=1):  #   Дневная битва прошлого дня
        message_datetime -= datetime.timedelta(days=1)
        battle_time = message_datetime.replace(hour = 17, minute = 0, second = 0, microsecond = 0)
    else:
        battle_time = datetime.datetime.combine(message_datetime.date(), datetime.time(hour=1))
        while message_datetime - battle_time >= datetime.timedelta(hours=8):
            battle_time += datetime.timedelta(hours = 8)
    request = "select nickname from inspirations where nickname = %s and battle_time = %s"
    cursor.execute(request, (nickname, battle_time))
    row = cursor.fetchone()
    if row is not None:
        bot.send_message(chat_id=update.message.chat_id, text="Данный репорт уже есть на канале!")
        return
    tag = re.search("\\[(\\S+)\\]", nickname)
    if tag:
        tag = tag.group(1)
        inspired_by = "[🤷🏿‍♀️/{}]{}".format(tag, inspired_by)
    response = "⚡️<b>{0}</b> was inspired by <b>{1}</b>\n\n🕒 Battle on {2}".format(nickname, inspired_by, battle_time.strftime("%D %H:%M"))
    bot.send_message(chat_id = POST_CHANNEL_ID, text = response, parse_mode = 'HTML')
    bot.send_message(chat_id = mes.chat_id, text = "Спасибо! Отправлено на канал\nМожешь кидать сюда следующие репорты")
    castle = nickname[0]
    request = "insert into inspirations(castle, nickname, inspured_by_nickname, battle_time) values (%s, %s, %s, %s)"
    cursor.execute(request, (castle, nickname, inspired_by, battle_time))

def old_battle_cry(bot, update):
    bot.send_message(chat_id = update.message.chat_id,
                     text = "В этом репорте скилл Battle Cry отображается в устаревшей версии. Невозможно определить, кто именно Вас вдохновил.")



def clear_report(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="В этом репорте нет эффекта Battle Cry!")

def not_forward_report(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Репорт должен быть форвардом с @ChatWarsBot. "
                                                          "\n\n<em>Мы никак не обрабатываем и не храним ваши статы или результаты битвы.</em>",
                     parse_mode='HTML')

def not_report(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Пожалуйста, пришлите форвард ответа @ChatWarsBot на команду "
                                                          "/report с наличием сработавшего скилла Battle Cry!")

def skip(bot, update):
    return

dispatcher.add_handler(MessageHandler(filter_not_pm, skip))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))

dispatcher.add_handler(MessageHandler(Filters.text & filter_correct_report, report_handling))

dispatcher.add_handler(MessageHandler(Filters.text & filter_old_battle_cry, old_battle_cry))
dispatcher.add_handler(MessageHandler(Filters.text & filter_incorrect_report, clear_report))
dispatcher.add_handler(MessageHandler(Filters.text & filter_not_forward_report, not_forward_report))
dispatcher.add_handler(MessageHandler(Filters.text & filter_not_report, not_report))



updater.start_polling(clean=False)

# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()