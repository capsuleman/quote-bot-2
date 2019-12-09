#!./venv/bin/python3

from dao import DAO
from bot import BotThread
from config import token_bot, chat_id

dao = DAO()
botThread = BotThread(dao, token_bot, chat_id)

botThread.start()

print('running')
