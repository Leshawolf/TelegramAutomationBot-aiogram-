from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = 'xxxxxxxxx'

"""DATABASE"""
HOST = 'xxxxxxxxx'
USER = 'xxxxxxxxx'
DATABASE = 'xxxxxxxxx'
PASS = 'xxxxxxxxx'

""" INSTAGRAM """

""" FACEBOOK """

SKIP_UPDATES = env.bool("SKIP_UPDATES", False)
WORK_PATH: Path = Path(__file__).parent.parent

""" Middleware"""
I18N_DOMAIN = "Automation" 
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
