from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
    
language_kb=InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text="🇷🇺 Русский язык 🇷🇺", callback_data="start_lng_ru")
            ],
            [
                InlineKeyboardButton(text="🇬🇧 English language 🇬🇧", callback_data="start_lng_an")
            ]
        ]
    )
    
start_kb = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text="Profile", callback_data="start_main_profile")
            ],
            [
                InlineKeyboardButton(text="Start bot", callback_data="start_main_start")
            ]
        ]
    )
profile_kb = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text="Profile", callback_data="start_main_profile")
            ]
        ]
    )