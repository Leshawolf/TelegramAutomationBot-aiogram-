import asyncio
from aiogram import Dispatcher
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app import utils, config
from app.loader import MYSQL_POOL, dp,bot
from app.classes.twitter_key import TwitterKey
from app.utils.Twitter import parse_twitter
from app.utils.default_commands import setup_default_commands
from app import middlewares, handlers,classes

async def check_shedule(bot):
    try:
        list_id_user=await TwitterKey.check_twitter_time(MYSQL_POOL)

        for item in list_id_user:
            keys_users=await TwitterKey.check_user_key_twitter(item[1],item[2],MYSQL_POOL)
            check_folowing_user=await parse_twitter.is_follower(keys_users[3],keys_users[4],keys_users[6],keys_users[7],item[4])
            if(check_folowing_user==False):              
                await parse_twitter.unfollow_user(keys_users[3],keys_users[4],keys_users[6],keys_users[7],item[4])
                await parse_twitter.unlike_all_tweets(keys_users[3],keys_users[4],keys_users[6],keys_users[7],item[4])
                await TwitterKey.update_twitter_sub_status(item[4],MYSQL_POOL)
    except Exception as e:
        print(f"file: __main__ hand:check_shedule\nError: {e}")
        
async def on_startup(dispatcher: Dispatcher):
    await setup_default_commands(dispatcher)
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(check_shedule, trigger='interval', seconds=60,kwargs={'bot': bot})
    scheduler.start()

if __name__ == '__main__':
    utils.setup_logger("INFO", ["aiogram.bot.api"])
    executor.start_polling(
        dp,on_startup=on_startup,skip_updates=config.SKIP_UPDATES
    )