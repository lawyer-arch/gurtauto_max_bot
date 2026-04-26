import asyncio
import logging

from maxapi import Bot, Dispatcher
from maxapi.types import BotStarted

from config import settings
from handlers.user import menu, start, lead_form

logging.basicConfig(level=logging.INFO)


bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

dp.include_routers(start.router)
dp.include_routers(menu.router)
dp.include_routers(lead_form.router)


# Ответ бота при нажатии кнопки "Начать"
@dp.bot_started()
async def bot_started(event: BotStarted):
    await bot.send_message(
        chat_id=event.chat_id,
        text='Привет! отправь мне /start'
    )


async def main():
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        print("Polling cancelled, exiting...")


if __name__ == '__main__':
    asyncio.run(main())
