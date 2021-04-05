from aiogram.types import ReplyKeyboardMarkup


start_spam = 'Спам'
stop_spam = 'Стоп'


def select_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(start_spam)
    markup.add(stop_spam)

    return markup
