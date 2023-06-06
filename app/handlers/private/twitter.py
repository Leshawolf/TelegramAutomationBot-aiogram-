import asyncio
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart
from app.keyboard import start_kb
from app.classes.account import Account 
from app.classes.twitter_key import TwitterKey 

from app.loader import MYSQL_POOL, dp
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from app.utils.Twitter.parse_twitter import main_api_search
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from app.utils.Twitter import parse_twitter


@dp.callback_query_handler(text="start_main_start")
async def callback_function_twitter_bot(clbk:types.CallbackQuery):
    try:
        list_account_twitter=await TwitterKey.check_user_active_key_twitter(clbk.from_user.id,MYSQL_POOL)
        for account in list_account_twitter:
            if(len(list_account_twitter)!=0):
                if(account[3]!='' or account[4]!='' or account[5]!='' or account[6]!='' or account[7]!=''):                                    
                    await clbk.message.answer(f"Bot activated account {account[2]}")
                    for i in range(40):
                        await asyncio.sleep(30)
                        check = await main_api_search(account[8],account[0],clbk.from_user.id)
                        if check != 0:
                            print(f"Bot committed {check} subscriptions")
                    await clbk.message.answer("The bot completed the circle of subscriptions and was deactivated")
                else:
                    await clbk.message.answer("Before starting the bot, you must fill in the account keys")
            else:
                await clbk.message.answer("Check that there is at least one activated account")
    except Exception as e:
        print("Error twitter.py in callback_function_twitter_bot")
        print(e)