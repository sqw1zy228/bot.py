import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties

BOT_TOKEN = "9030131409:AAFq-5oHyRV6396KlmJcGYr4Qm6W_4m5PEI"
MAIN_GROUP = "@uh_rp"

NPU_TARGET = -1003876227272
NPU_THREAD_ID = 962

COURT_TARGET = -1004445001399
COURT_THREAD_ID = 4565

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Ловимо все, де є 102 (наприклад, .102 або /102)
@dp.message(F.text.lower().contains("102"))
async def handle_npu_call(message: types.Message):
    try:
        await bot.copy_message(
            chat_id=NPU_TARGET,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            message_thread_id=NPU_THREAD_ID if NPU_THREAD_ID != 0 else None
        )
        logging.info("Виклик НПУ успішно скопійовано!")
    except Exception as e:
        logging.error(f"Помилка копіювання в НПУ: {e}")

# Ловимо все, де є суд або court
@dp.message(F.text.lower().regexp(r"(суд|court)"))
async def handle_court_call(message: types.Message):
    try:
        await bot.copy_message(
            chat_id=COURT_TARGET,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            message_thread_id=COURT_THREAD_ID if COURT_THREAD_ID != 0 else None
        )
        logging.info("Звернення до суду успішно скопійовано!")
    except Exception as e:
        logging.error(f"Помилка копіювання в Суд: {e}")

async def health_check(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await start_web_server()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
