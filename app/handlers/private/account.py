from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart
from app.keyboard import account_kb, start_kb
from app.classes.account import Account 
from app.classes.twitter_key import TwitterKey
from app.loader import MYSQL_POOL, dp
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

class FSMTwitterApiKey(StatesGroup):
    load_api_key=State()

class FSMTwitterApiSecret(StatesGroup):
    load_api_secret=State()
    
class FSMTwitterBearerKey(StatesGroup):
    load_bearer_key=State()  
     
class FSMTwitterAccessKey(StatesGroup):
    load_access_key=State() 
    
class FSMTwitterAccessSecret(StatesGroup):
    load_access_secret=State() 

class FSMTwitterNameAccount(StatesGroup):
    load_name_account=State()

class FSMTwitterKeywordAccount(StatesGroup):
    load_keyword_account=State()
    
async def twitter_key_kb(id_key,state:FSMContext):
    try:
        twitter_keys=await TwitterKey.check_keys_in_id(id_key,MYSQL_POOL)
        name='-'
        consumer_key='-'
        consumer_secret = '-'
        bearer_key = '-'
        access_token='-'
        access_secret='-'
        keyword='-'
        status='✅ON✅'
        status_int=1
        if(str(twitter_keys[2])!=''):
            name=f'{twitter_keys[2]}'
        if(str(twitter_keys[3]) != ''):
            consumer_key = f'{twitter_keys[3]}'
        if(str(twitter_keys[4]) != ''):
            consumer_secret = f'{twitter_keys[4]}'  
        if(str(twitter_keys[5]) != ''):
            bearer_key = f'{twitter_keys[5]}'
        if(str(twitter_keys[6])!=''):
            access_token=f'{twitter_keys[6]}'
        if(str(twitter_keys[7])!=''):
            access_secret=f'{twitter_keys[7]}'
        if(str(twitter_keys[8])!=''):
            keyword=f'{twitter_keys[8]}'
        if(str(twitter_keys[9])!='1'):
            status=f'❌OFF❌'
            status_int=0
        key_twitter_markup = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text=('Name: {name}').format(name = name), callback_data=f"key_twitter_{id_key}_name")
                ],
                [
                    InlineKeyboardButton(text=('API Key: {consumer_key}').format(consumer_key = consumer_key), callback_data=f"key_twitter_{id_key}_api")
                ],
                [
                    InlineKeyboardButton(text=('API Key Secret: {consumer_secret}').format(consumer_secret=consumer_secret), callback_data=f"key_twitter_{id_key}_apisecret")
                ],
                [
                    InlineKeyboardButton(text=('Bearer Token: {bearer_key}').format(bearer_key=bearer_key), callback_data=f"key_twitter_{id_key}_bearer")
                ],
                [
                    InlineKeyboardButton(text=('Access Token: {access_token}').format(access_token=access_token), callback_data=f"key_twitter_{id_key}_access")
                ],
                [
                    InlineKeyboardButton(text=('Access Token Secret: {access_secret}').format(access_secret=access_secret), callback_data=f"key_twitter_{id_key}_accesssecret")
                ],
                [
                    InlineKeyboardButton(text=('🔑Keyword🔑: {keyword}').format(keyword=keyword), callback_data=f"key_twitter_{id_key}_keyword")
                ],
                [
                    InlineKeyboardButton(text=('Condition: {status}').format(status=status), callback_data=f"key_twitter_{id_key}_status_{status_int}")
                ],
                [
                    InlineKeyboardButton(text=('Delete Account 🗑'), callback_data=f"delete_twitter_account_{id_key}")
                ],
                [
                    InlineKeyboardButton(text=('Back in menu'), callback_data="back_start_menu")
                ]
            ]
        )
        return key_twitter_markup
    except Exception as e:
        print(f"{e}\n File:handler/private/account.py - def twitter_key_kb")
        await state.finish()
        
async def twitter_account_key_kb(tgID):
    try:
        twitter_keys=await TwitterKey.check_user_account_twitter(tgID,MYSQL_POOL)
        if(str(twitter_keys) != None):    
            keyboard = types.InlineKeyboardMarkup()
            for item in twitter_keys:
                inline_button = types.InlineKeyboardButton(text=f"{item[2]}", callback_data=f'twit_account_key_{item[0]}')
                keyboard.add(inline_button)
            keyboard.add(InlineKeyboardButton(text="Create new account", callback_data=f'create_new_account_twitter')).add(InlineKeyboardButton(text="Back in menu", callback_data=f'back_start_menu'))
        return keyboard
    except Exception as e:
        print(f"{e}\n File:handler/private/account.py - def twitter_account_key_kb/")

@dp.callback_query_handler(text="start_main_profile")
async def callback_function_bot(clbk:types.CallbackQuery):
    try:
        await clbk.message.edit_reply_markup()
        await clbk.message.edit_text("What social networks do you want to fill in?",reply_markup=account_kb.type_add_social_key)
    except Exception as e:
        print("Error start.py in callback_function_bot")
        print(e)

@dp.callback_query_handler(lambda query: query.data.startswith("account_key_"))
async def callback_function_bot(clbk:types.CallbackQuery):
    try:
        await clbk.message.edit_reply_markup()
        social = clbk.data.split('_')[2]
        if(social=="twitter"):
            await clbk.message.edit_text("Select a key to change/add:",reply_markup=await twitter_account_key_kb(clbk.from_user.id))
        elif(social=="instagram"):
            await clbk.message.edit_text("Скоро заполнение ключей для instagram появятся:")
        elif(social=="facebook"):
            await clbk.message.edit_text("Скоро заполнение ключей для facebook появится:")
    except Exception as e:
        print("Error callback_function_bot.py in message_function_bot")
        print(e)
       
       
@dp.callback_query_handler(lambda query: query.data.startswith("twit_account_key_"))
async def callback_function_account_key_twit (clbk:types.CallbackQuery,state:FSMContext):
    try:
        id_key = clbk.data.split('_')[3]
        await clbk.message.edit_text("Select a key to change/add:",reply_markup=await twitter_key_kb(id_key,state))
    except Exception as e:
        print("Error callback_function_bot.py in callback_function_account_key_twit")
        print(e)        
        
@dp.callback_query_handler(lambda query: query.data.startswith("key_twitter_"))
async def callback_function_bot(clbk:types.CallbackQuery,state:FSMContext):
    try:
        type_key = clbk.data.split('_')[3:]
        await state.update_data(id_key_account=clbk.data.split('_')[2])
        if(type_key[0]=="api"):
            await clbk.message.edit_text("Enter your API Key:")
            await FSMTwitterApiKey.load_api_key.set()
        elif(type_key[0]=="apisecret"):
            await clbk.message.edit_text("Enter your API Key Secret:")
            await FSMTwitterApiSecret.load_api_secret.set()
        elif(type_key[0]=="bearer"):
            await clbk.message.edit_text("Enter your Bearer Token:")
            await FSMTwitterBearerKey.load_bearer_key.set()
        elif(type_key[0]=="access"):
            await clbk.message.edit_text("Enter your Access Token:")
            await FSMTwitterAccessKey.load_access_key.set()
        elif(type_key[0]=="accesssecret"):
            await clbk.message.edit_text("Enter your Access Token Secret:")
            await FSMTwitterAccessSecret.load_access_secret.set()
        elif(type_key[0]=="name"):
            await clbk.message.edit_text("Enter your Name Account:")
            await FSMTwitterNameAccount.load_name_account.set()
        elif(type_key[0]=="keyword"):
            await clbk.message.edit_text("Enter your Keyword Account:")
            await FSMTwitterKeywordAccount.load_keyword_account.set()
        elif(type_key[0]=="status"):
            await clbk.message.edit_reply_markup()
            await TwitterKey.update_twitter_key(clbk.from_user.id,clbk.data.split('_')[2],"status",type_key[1],MYSQL_POOL)
            await clbk.message.edit_text("Choose Keys for Twitter",reply_markup=await twitter_key_kb(clbk.data.split('_')[2],state))
            await state.reset_state (with_data = False)
    except Exception as e:
        print("Error callback_function_bot.py in message_function_bot")
        print(e)
        
 

@dp.callback_query_handler(lambda query: query.data.startswith("delete_twitter_account_"))
async def callback_function_bot(clbk:types.CallbackQuery,state:FSMContext):
    try:
        id_account_twitter = clbk.data.split('_')[3]
        keyboard = types.InlineKeyboardMarkup()
        inline_button = types.InlineKeyboardButton(text="Yes", callback_data=f"account_twitter_delete_{id_account_twitter}_yes")
        inline_button1 = types.InlineKeyboardButton(text="No", callback_data=f"account_twitter_delete_{id_account_twitter}_no")
        keyboard.add(inline_button)
        keyboard.add(inline_button1)
        await clbk.message.edit_text("Select a key to change/add:",reply_markup= keyboard)
    except Exception as e:
        print("Error callback_function_bot.py in message_function_bot")
        print(e)
        
@dp.callback_query_handler(lambda query: query.data.startswith("account_twitter_delete_"))
async def callback_function_bot(clbk:types.CallbackQuery,state:FSMContext):
    try:
        yes_or_no = clbk.data.split('_')[4]
        id=clbk.data.split('_')[3]
        if(yes_or_no=="yes"):
            await TwitterKey.delete_account_twitter(clbk.from_user.id,id,MYSQL_POOL)
            await clbk.message.edit_text("Account successfully deleted ✅\nSelect a key to change/add:",reply_markup= await twitter_account_key_kb(clbk.from_user.id))
        else:
            await clbk.message.edit_text("Select a key to change/add:",reply_markup= await twitter_account_key_kb(clbk.from_user.id))
    except Exception as e:
        print("Error callback_function_bot.py in message_function_bot")
        print(e) 
          
@dp.callback_query_handler(lambda query: query.data.startswith("create_new_account_twitter"))
async def callback_function_bot(clbk:types.CallbackQuery,state:FSMContext):
    try:
        count=await TwitterKey.check_user_account_twitter(clbk.from_user.id,MYSQL_POOL)
        await TwitterKey.create_new_account_twitter(clbk.from_user.id,len(count),MYSQL_POOL)
        await clbk.message.edit_text("Select a key to change/add:",reply_markup=await twitter_account_key_kb(clbk.from_user.id))
    except Exception as e:
        print("Error callback_function_bot.py in message_function_bot")
        print(e)
                      
@dp.message_handler(state=FSMTwitterApiKey.load_api_key)
async def message_function_bot(msg: types.Message, state: FSMContext):
    try:
        data=await state.get_data()
        id=data.get(f'id_key_account')
        await TwitterKey.update_twitter_key(msg.from_user.id,id,"api",msg.text,MYSQL_POOL)
        await msg.answer("Choose Keys for Twitter",reply_markup=await twitter_key_kb(id,state))
        await state.reset_state (with_data = False)
    except Exception as e:
        print("Error account.py in message_function_bot")
        print(e)
        
@dp.message_handler(state=FSMTwitterApiSecret.load_api_secret)
async def message_function_bot(msg: types.Message, state: FSMContext):
    try:
        data=await state.get_data()
        id=data.get(f'id_key_account')
        await TwitterKey.update_twitter_key(msg.from_user.id,id,"api_secret",msg.text,MYSQL_POOL)
        await msg.answer("Choose Keys for Twitter",reply_markup=await twitter_key_kb(id,state))
        await state.reset_state (with_data = False)
    except Exception as e:
        print("Error account.py in message_function_bot")
        print(e)

@dp.message_handler(state=FSMTwitterBearerKey.load_bearer_key)
async def message_function_bot(msg: types.Message, state: FSMContext):
    try:
        data=await state.get_data()
        id=data.get(f'id_key_account')
        await TwitterKey.update_twitter_key(msg.from_user.id,id,"bearer",msg.text,MYSQL_POOL)
        await msg.answer("Choose Keys for Twitter",reply_markup=await twitter_key_kb(id,state))
        await state.reset_state (with_data = False)
    except Exception as e:
        print("Error account.py in message_function_bot")
        print(e)

@dp.message_handler(state=FSMTwitterAccessKey.load_access_key)
async def message_function_bot(msg: types.Message, state: FSMContext):
    try:
        data=await state.get_data()
        id=data.get(f'id_key_account')
        await TwitterKey.update_twitter_key(msg.from_user.id,id,"access",msg.text,MYSQL_POOL)
        await msg.answer("Choose Keys for Twitter",reply_markup=await twitter_key_kb(id,state))
        await state.reset_state (with_data = False)
    except Exception as e:
        print("Error account.py in message_function_bot")
        print(e)

@dp.message_handler(state=FSMTwitterAccessSecret.load_access_secret)
async def message_function_bot(msg: types.Message, state: FSMContext):
    try:
        data=await state.get_data()
        id=data.get(f'id_key_account')
        await TwitterKey.update_twitter_key(msg.from_user.id,id,"access_secret",msg.text,MYSQL_POOL)
        await msg.answer("Choose Keys for Twitter",reply_markup=await twitter_key_kb(id,state))
        await state.reset_state (with_data = False)
    except Exception as e:
        print("Error account.py in message_function_bot")
        print(e)

@dp.message_handler(state=FSMTwitterNameAccount.load_name_account)
async def message_function_bot(msg: types.Message, state: FSMContext):
    try:
        data=await state.get_data()
        id=data.get(f'id_key_account')
        await TwitterKey.update_twitter_key(msg.from_user.id,id,"name",msg.text,MYSQL_POOL)
        await msg.answer("Choose Keys for Twitter",reply_markup=await twitter_key_kb(id,state))
        await state.reset_state (with_data = False)
    except Exception as e:
        print("Error account.py in message_function_bot")
        print(e)
        
@dp.message_handler(state=FSMTwitterKeywordAccount.load_keyword_account)
async def message_function_bot(msg: types.Message, state: FSMContext):
    try:
        data=await state.get_data()
        id=data.get(f'id_key_account')
        await TwitterKey.update_twitter_key(msg.from_user.id,id,"keyword",msg.text,MYSQL_POOL)
        await msg.answer("Choose Keys for Twitter",reply_markup=await twitter_key_kb(id,state))
        await state.reset_state (with_data = False)
    except Exception as e:
        print("Error account.py in message_function_bot")
        print(e)