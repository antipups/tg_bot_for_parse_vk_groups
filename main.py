import threading
import time
import telebot
import config
import vk

bot = telebot.TeleBot(token=config.tg_token)


@bot.message_handler(commands=['add',])
def add_group(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton(text='Отмена'))
    bot.send_message(chat_id=config.my_chat_id, text='ID группы: ', reply_markup=markup)


# @bot.message_handler(commands=['start',])
# def get_id(message):
#     print(message)


@bot.callback_query_handler(func=lambda call: True)
def callback(obj):
    for news in config.dict_of_data_about_post:
        if news.get('id') == int(obj.data):
            bot.send_media_group(chat_id=config.my_chat_id,
                                 media=(telebot.types.InputMediaPhoto(news.get('attachments')[0], caption=news.get('text')),
                                        *(telebot.types.InputMediaPhoto(media) for media in news.get('attachments')[1:])))


def change_menu(news):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Да', callback_data=news))
    return markup


def parse():
    while True:
        for news in vk.parse_group():
            config.dict_of_data_about_post.append(news)
            bot.send_photo(chat_id=config.my_chat_id,
                           photo=news.get('attachments')[0],
                           caption=news.get('text'),
                           reply_markup=change_menu(news.get('id')))
        time.sleep(60)


if __name__ == '__main__':
    threading.Thread(target=parse).start()
    bot.infinity_polling()
