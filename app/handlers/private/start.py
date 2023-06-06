from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart
from app.keyboard import start_kb
from app.classes.account import Account 
from app.loader import MYSQL_POOL, dp

@dp.message_handler(commands=['start'])
async def command_start_handler(msg: types.Message):
    try:
        if(await Account.check_user(msg.from_user.id,MYSQL_POOL)==None):
            await msg.answer(f'Hello, {msg.from_user.full_name}! Choose language\nПривет, {msg.from_user.full_name}! Выберите язык',reply_markup=start_kb.language_kb)
        else:
            await msg.answer(f"Choose an action:",reply_markup=start_kb.start_kb)
    except Exception as e:
        print("Error start.py in command_start_handler")
        print(e)

@dp.callback_query_handler(text="back_start_menu")
async def callback_main_action_choice(clbk:types.CallbackQuery):
    try:
        await clbk.message.edit_text(f"Choose an action:",reply_markup=start_kb.start_kb)
    except Exception as e:
        print("Error start.py in callback_main_action_choice")
        print(e)

@dp.callback_query_handler(lambda query: query.data.startswith("start_lng_"))
async def callback_main_action_choice(clbk:types.CallbackQuery):
    try:
        await clbk.message.edit_reply_markup()
        language_user=clbk.data.split('_')[2]
        await Account.create_users(clbk.from_user.id,clbk.from_user.username,language_user,MYSQL_POOL)
        await clbk.message.edit_text(f"Choose an action:",reply_markup=start_kb.start_kb)
    except Exception as e:
        print("Error start.py in callback_main_action_choice")
        print(e)

 

