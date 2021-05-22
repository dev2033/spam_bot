from aiogram.types import ReplyKeyboardMarkup


start_spam = 'Спам'
stop_spam = 'Стоп'


def select_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(start_spam)
    markup.add(stop_spam)
    return markup


def time_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('100', '200', '300', '400', '500')
    markup.add('600', '700', '800', '900', '999')
    markup.add('Стоп')
    return markup


def threads_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('1', '2', '3', '4', '5')
    markup.add('6', '7', '8', '9', '10')
    markup.add('11', '12', '13', '14', '15')
    markup.add('16', '17', '18', '19', '20')
    markup.add('Стоп')
    return markup


def method_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('SMS', 'HTTP')
    markup.add('Стоп')
    return markup
