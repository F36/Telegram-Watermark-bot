# -*- coding: utf-8 -*-
import telebot
import config
import random
import os
import time
from tools.tools import getting_ready

bot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hi, Send or Forward me a PHOTO!')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Send /start or /help')


@bot.message_handler(content_types=["photo"])
def send_watermark(message):
    chat_id = message.chat.id
    sent_message = bot.reply_to(message, 'Downloading...')
    message_id = sent_message.message_id
    file = bot.get_file(message.photo[0].file_id)
    downloaded_file = bot.download_file(file.file_path)
    bot.edit_message_text(f'Downloaded!\n\nNow, Genarating Watermarks...\n\ncurrent watermark: {config.WATERMARK}', chat_id=chat_id, message_id=message_id)
    __path = 'images/' + str(random.randint(100000, 999999)) + '.tmp'
    with open(__path, 'wb') as f:
        f.write(downloaded_file)
    fname = getting_ready(__path)
    os.remove(__path)
    time.sleep(2)
    bot.edit_message_text('Now, Uploading...', chat_id=chat_id, message_id=message_id)
    for i in ('black', 'white'):
        __file = 'images/out/{}/{}'.format(i, fname)
        __photo = open(__file, 'rb')
        bot.send_photo(message.chat.id, __photo, reply_to_message_id=message.message_id)
        os.remove(__file)
    bot.delete_message(chat_id=chat_id, message_id=message_id)


print('watermark bot started successfully!')
bot.polling()