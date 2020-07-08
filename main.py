import telebot
import requests
import re
import config
import pprint


bot = telebot.TeleBot(token=config.tg_token)


@bot.message_handler(commands=['start',])
def get_id(message):
    print(message)


# def parse():
#     bot.send_message()


if __name__ == '__main__':
    # parse()
    bot.infinity_polling()