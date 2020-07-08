import time

import telebot
import config
import vk

bot = telebot.TeleBot(token=config.tg_token)


# @bot.message_handler(commands=['start',])
# def get_id(message):
#     print(message)


def parse():
    while True:
        result = vk.parse_group()
        if result.get('attachments'):
            bot.send_media_group(chat_id=config.my_chat_id, media=(telebot.types.InputMediaPhoto(result.get('attachments')[0], caption=result.get('text')),
                                                                   *(telebot.types.InputMediaPhoto(media) for media in result.get('attachments')[1:])))
        else:
            bot.send_message(chat_id=config.my_chat_id, text=result.get('text'))
        time.sleep(60)


if __name__ == '__main__':
    parse()
    # bot.infinity_polling()