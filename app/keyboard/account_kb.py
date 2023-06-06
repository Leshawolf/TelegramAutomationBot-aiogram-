from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
    
type_add_social_key=InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text="Key Twitter", callback_data="account_key_twitter")
            ],
            [
                InlineKeyboardButton(text="Back", callback_data="back_start_menu")
            ]
        ]
    )

if_delete_acc_twit_kb=InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text="Yes", callback_data="account_twitter_delete_yes")
            ],
            [
                InlineKeyboardButton(text="No", callback_data="account_twitter_delete_no")
            ]
        ]
    )
    