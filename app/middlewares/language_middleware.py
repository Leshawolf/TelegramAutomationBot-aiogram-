from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import types
from app.classes.account import Account
from config import I18N_DOMAIN, LOCALES_DIR



class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action, args):
        user = types.User.get_current()
        return await Account.get_lang(user.id) or user.locale


def setup_middleware(dp):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n