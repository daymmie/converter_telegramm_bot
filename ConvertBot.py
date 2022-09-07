import telebot

from Config import allvalues
from Config import API_Token
from Extensions import Converter
from Extensions import BotException

bot = telebot.TeleBot(API_Token)


@bot.message_handler(commands=['start', 'help'])
def coms_start_help(message):
    bot.send_message(message.chat.id, 'Привет, я валютный бот. Отравьте мне сообщение в виде:'
                    ' \n<Имя валюты, цену которой хотите узнать>,'
                    ' \n<Имя валюты, в которой надо узнать цену первой валюты> '
                    ' \n<Количество валюты, цену которой хотите узнать>.'
                    ' \n<Данные вводятся только большими буквами!!!.'
                    ' \n<Введите /values, чтобы увидеть список всех валют>'
                    ' \n<Введите /example, чтобы посмотреть пример правильного ввода, для работы бота'
                    ' \nПример ввода: \nRUB USD 100')


@bot.message_handler(commands=['example'])
def coms_start_help(message):
    bot.send_message(message.chat.id, 'Для того, чтобы узнать сколько рублей в 100 долларах введите:'
                                      '\nRUB USD 100')


@bot.message_handler(commands=['values'])
def coms_val(message: telebot.types.Message):
    textvalues = 'Список доступных к конвертации валют:'
    for x in allvalues:
        textvalues = '\n'.join((textvalues, x))
    bot.reply_to(message, textvalues)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) > 3:
            bot.send_message(message.chat.id, 'Введите не больше трех параметров.')
            raise BotException('Слишком много параметров')
        if len(values) <= 2:
            bot.send_message(message.chat.id, 'Введите ровно три параметра.')
            raise BotException('Слишком мало параметров')
        base, quote, amount = values
        total_base = Converter.get_price(base, quote, amount)
    except BotException as e:
        bot.send_message(message.chat.id, f"Ошибка ввода данных пользователем. \n{e}")
    except Exception as e:
        bot.send_message(message.chat.id, f'Неизвестная ошибка. \n{e}')
    else:
        text = f'{total_base}'
        bot.send_message(message.chat.id, text)


bot.infinity_polling()