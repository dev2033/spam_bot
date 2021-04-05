from aiogram.types import ReplyKeyboardMarkup


start_spam = 'Спам'.lower()
stop_spam = 'Стоп'.lower()


def select_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(start_spam)
    markup.add(stop_spam)

    return markup
