import threading
import time
import telebot
import config
import util
import vk

bot = telebot.TeleBot(token=config.tg_token)


@bot.message_handler(commands=['addgroup', ])
def add_group(message):
    """
        Функция на добавление групп
    :param message:
    :return:
    """
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(telebot.types.KeyboardButton(text='Отмена'))
    msg = bot.send_message(chat_id=config.my_chat_id, text='ID группы: ', reply_markup=markup)
    bot.register_next_step_handler(msg, setup_group)


def setup_group(msg):
    """
        Функция на добавление группы в БД
    :param msg:
    :return:
    """
    if msg.text == 'Отмена':
        return
    result_of_add = util.setup_new_group(msg.text)
    bot.send_message(chat_id=config.my_chat_id, text=result_of_add)


@bot.message_handler(commands=['addpost', ])
def add_post(message):
    """
        Функция на вывод меню добавления поста
    :param message:
    :return:
    """
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=True)
    markup.add(telebot.types.KeyboardButton(text='Отмена'))
    msg = bot.send_message(chat_id=config.my_chat_id,
                           text='Создадите пост и отправьте его мне: ',
                           reply_markup=markup)
    bot.register_next_step_handler(msg, get_post)


def get_post(message):
    """
        Функция на вывод добавленного админом поста в группы
    :param message:
    :return:
    """
    if message.text == 'Отмена':
        return
    if message.content_type == 'text':
        bot.send_message(chat_id=config.channel_id,
                         text=message.text + '\n\n<a href=ВАША ССЫЛКА">ВАШЕ НАЗВАНИЕ КАНАЛА</a>',
                         parse_mode='html')
    elif message.content_type == 'photo':
        bot.send_photo(chat_id=config.channel_id,
                       photo=message.json.get('photo')[-1].get('file_id'),
                       caption=message.caption + '\n\n<a href=ВАША ССЫЛКА">ВАШЕ НАЗВАНИЕ КАНАЛА</a>',
                       parse_mode='html')
    elif message.content_type == 'document':
        bot.send_document(chat_id=config.channel_id,
                          data=message.json.get('document').get('file_id'),
                          caption=(message.caption if message.caption else '')  + '\n\n<a href=ВАША ССЫЛКА">ВАШЕ НАЗВАНИЕ КАНАЛА</a>',
                          parse_mode='html')
    elif message.content_type == 'poll':
        dict_of_poll = message.json.get('poll')
        bot.send_poll(chat_id=config.channel_id,
                      question=dict_of_poll.get('question'),
                      options=tuple(option.get('text') for option in dict_of_poll.get('options')))


@bot.channel_post_handler(commands=['start', ])
def get_id(message):
    """
        Для получения id-шника
    :param message:
    :return:
    """
    # print(message)
    threading.Thread(target=parse).start()


@bot.callback_query_handler(func=lambda call: True)
def callback(obj):
    """
        Для одобрения админу
    :param obj:
    :return:
    """
    if obj.data.find('del') > -1:
        bot.delete_message(config.my_chat_id, obj.data[obj.data.find(' ') + 1:obj.data.rfind(' ')])
        for news in config.dict_of_data_about_post:
            if news.get('id') == int(obj.data[obj.data.rfind(' '):]):
                config.dict_of_data_about_post.remove(news)
        return

    for news in config.dict_of_data_about_post:
        if news.get('id') == int(obj.data):
            if news.get('attachments') and len(news.get('attachments')) > 1:
                bot.send_media_group(chat_id=config.channel_id,
                                     media=(telebot.types.InputMediaPhoto(news.get('attachments')[0], caption=news.get('text'),
                                            *(telebot.types.InputMediaPhoto(media) for media in news.get('attachments')[1:])),))
            elif news.get('attachments') and len(news.get('attachments')) == 1:
                bot.send_photo(chat_id=config.channel_id,
                               photo=news.get('attachments')[0],
                               caption=news.get('text') + '\n\n<a href=ВАША ССЫЛКА">ВАШЕ НАЗВАНИЕ КАНАЛА</a>',
                               parse_mode='html',)
            else:
                bot.send_message(chat_id=config.channel_id,
                                 text=news.get('text') + '\n\n<a href=ВАША ССЫЛКА">ВАШЕ НАЗВАНИЕ КАНАЛА</a>',
                                 parse_mode='html')
            config.dict_of_data_about_post.remove(news)
            return


def change_menu(news, message_id):
    """
        Менюшка на вывод да
    :param news:
    :return:
    """
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Да', callback_data=news),
               telebot.types.InlineKeyboardButton(text='Нет', callback_data='del ' + str(message_id) + ' ' + str(news)))
    return markup


def parse():
    """
        Ежесекундный парс
    :return:
    """
    while True:
        for news in vk.parse_group():
            config.dict_of_data_about_post.append(news)
            msg = bot.send_message(chat_id=config.my_chat_id,
                                   text='.')
            if news.get('attachments'):
                bot.send_photo(chat_id=config.my_chat_id,
                               photo=news.get('attachments')[0],
                               caption=news.get('text'),
                               reply_markup=change_menu(news.get('id'), msg.message_id + 1))
            else:
                bot.send_message(chat_id=config.my_chat_id,
                                 text=news.get('text'),
                                 reply_markup=change_menu(news.get('id'), msg.message_id + 1))
            bot.delete_message(config.my_chat_id, msg.message_id)
        time.sleep(60)


if __name__ == '__main__':
    threading.Thread(target=parse).start()
    bot.infinity_polling()
    # pass