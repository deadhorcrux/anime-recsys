import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters import Command,  CommandObject
from aiogram.types import Message
from aiogram.utils.markdown import hbold

import rec

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6370729345:AAEj3lyvU4bhZdfCqCKUY6LSoLQb-M2dQDM"

bot = Bot(token=TOKEN)
# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
#router = Router()
#router.message.register(pers_rec, Command("pers"))

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Персональные рекомендации"),
            types.KeyboardButton(text="Рекомендации к тайтлам")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ "
    )
    await message.answer("""
Привет, я телегарм бот, который рекомендует аниме\\
Ты можешь выбрать два вида рекомендаци:
 1 Персональный рекомендации пользователям сайта [shikimori](https://shikimori.me/)
Для этого отправь сообщение в формате `/name твой_ник_на_shikimori`
 2 Рекомендации к твоему аниме\
Для этого отправь сообщение в формате `/anime название_аниме`
Ты можешь вводить название как на русском так и на английском \\ 
Для более точных рекомендаций используете оригинальное название на английском 
""", parse_mode='MarkdownV2', reply_markup=keyboard)

@dp.message(F.text.lower() == 'персональные рекомендации')
async def person(message: types.Message):
    await message.reply('Введите /name ВАШ_НИК_на_shikimori')


@dp.message(F.text.lower() == 'рекомендации к тайтлам')
async def person(message: types.Message):
    await message.reply('Введите /anime НАЗВАНИЕ_anime')



@dp.message(Command('anime'))
async def sim_rec_name(message: types.Message, command: CommandObject):
    try:
        title = command.args
        answer_message = rec.get_similitary_rec(title)
        # ans = str('\n')
        # for idx, item in enumerate(sim_recs.values()):
        #     if idx == 10:
        #         break
        #     ans += f"• {item} \n"
    except:
        await message.answer(str('Пожалуйста, введите /anime Название_аниме'))
        return 
    await message.answer(answer_message)

@dp.message(Command("name"))
async def cmd_name(message: types.Message, command: CommandObject):
    if command.args:
        user_name = command.args
        recs = rec.get_user_rec(user_name)
        ans = str('\n')
        for idx, item in enumerate(recs):
            if idx == 10:
                break
            ans += f"• {item} \n"
        await message.answer(ans)
    else:
        await message.answer("Пожалуйста, укажи своё имя после команды /name!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
