import requests
import json

from Config import allvalues
from Config import allvalues


class BotException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        if base not in allvalues:
            raise BotException(f'Валюта {base} не найдена')
        elif quote not in allvalues:
            raise BotException(f'Валюта {quote} не найдена')
        if base == quote:
            raise BotException(f'0 {base} = 0 {quote}')
        try:
            amount != float(amount) or int(amount)
        except ValueError:
            raise BotException(f'{amount} должен быть числом, '
                               '\nесли это не целое число - ставить нужно точку! (10.5, 5.2, и.т.д)')

        data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        if quote == "USD" and base == 'RUB':
            new_price = data['Valute'][quote]['Value'] * float(amount)
        elif quote == 'EUR' and base == 'RUB':
            new_price = data['Valute'][quote]['Value'] * float(amount)
        elif quote == 'RUB' and base == "USD":
            new_price = (1/(data['Valute'][base]['Value']) * float(amount))
        elif quote == 'RUB' and base == 'EUR':
            new_price = (1/(data['Valute'][base]['Value']) * float(amount))
        elif quote == 'USD' and base == "EUR":
            new_price = ((data['Valute'][base]['Value']) / (data['Valute'][quote]['Value'])) * float(amount)
        elif quote == 'EUR' and base == "USD":
            new_price = ((data['Valute'][base]['Value']) / (data['Valute'][quote]['Value'])) * float(amount)
        datetime = data['Date']
        time = 'По данным ЦБ РФ на ' + datetime[0:10]
        message = f'{time}:\n{amount} {quote} = {new_price} {base}'
        return message

