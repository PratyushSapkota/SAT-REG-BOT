from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, filters, Application
import os
from dotenv import load_dotenv
from selenium_check import run_check
import asyncio
load_dotenv()


TOKEN = os.getenv("bot_token")
CHECKING = False
CHECK_INTERVAL = 15 * 60


async def send_message(chat_id, message):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=chat_id, text=message)


async def start(update: Update, context: CallbackContext):
    global CHECKING
    await update.message.reply_text("Bot Started")
    CHECKING = True
    await start_checking(update.message.chat_id)


async def stop(update: Update, context: CallbackContext):
    global CHECKING
    await update.message.reply_text("Stopped the bot")
    CHECKING = False

async def check(chat_id):
    while CHECKING:
        res = await run_check(where="NP", when="NOV-2")
        if (res != ""):
            await send_message(chat_id=chat_id, message=f"Centers Available: {res[:-1]}")

    await asyncio.sleep(CHECK_INTERVAL)


async def start_checking(chat_id):
    asyncio.create_task(check(chat_id=chat_id))


async def return_status(update: Update, context: CallbackContext):
    await update.message.reply_text(f"{'Checking' if CHECKING else 'Idle'}")

async def quick_check(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /quick_check <month>")
        return
    
    date = ""
    
    if (context.args[0]).lower() == "nov":
        date = "NOV-2"
    elif (context.args[0]).lower() == "dec":
        date = "DEC-7"
    else:
        await update.message.reply_text("Invalid month")
        return

    await update.message.reply_text(f"Checking dates for {date}")
    res = await run_check(where="NP", when=date)
    await update.message.reply_text(f"Centers Available for {date}: {res[:-1]}")


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("status", return_status))
    application.add_handler(CommandHandler("quick_check", quick_check))

    print("Bot started")
    application.run_polling()


# asyncio.run(main())
main()
