import logging
from dotenv_vault import load_dotenv 
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
import asyncio
import sys
import os 


load_dotenv() 
TOKEN = os.getenv("token") 
logging.basicConfig(level=logging.INFO) 
dp = Dispatcher()


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())