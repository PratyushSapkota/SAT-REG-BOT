from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, filters, Application
import os
from dotenv import load_dotenv
from selenium_check import run_check, run_try
import asyncio
from datetime import datetime
from file import clearFile, getFileName, writeLine

load_dotenv()
TOKEN = os.getenv("bot_token")
CHECKING = False
CHECK_INTERVAL = 15 * 60
cleanDate = datetime.now().date().day

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
        if cleanDate != datetime.now().date().day:
            clearFile()
        res = await run_try(where="NP", when="DEC-7")
        if "Failed" in res:
            return await send_message(res)
        if res != "":
            await send_message(
                chat_id=chat_id, message=f"Centers Available: {res[:-1]}"
            )

        await asyncio.sleep(CHECK_INTERVAL)



async def start_checking(chat_id):
    asyncio.create_task(check(chat_id=chat_id))


async def return_status(update: Update, context: CallbackContext):
    await update.message.reply_text(f"{'Checking' if CHECKING else 'Idle'}")


async def quick_check(update: Update, context: CallbackContext):
    inputData = context.args[0]
    if len(context.args) != 1 or len(inputData) != 2:
        await update.message.reply_text("Usage: /quick_check <countryCode>")
        return

    countries = ["NP", "IN"]
    countryName = ["Nepal", "India"]

    if inputData.upper() in countries:
        country = (context.args[0]).upper()
    else:
        await update.message.reply_text(f"Invalid Country. Try: {countries}")
        return

    await update.message.reply_text(
        f"Checking centers for {countryName[countries.index(inputData.upper())]}."
    )
    res = await run_try(where=country, when="DEC-7")
    if ("Failed" in res):
        await update.message.reply_text(res)
    else:
        await update.message.reply_text(
            f"Centers Available in {countryName[countries.index(inputData.upper())]}: {res}"
        )

async def upload_logs(update: Update, context: CallbackContext):
    fileName = getFileName()
    with open(fileName, "rb") as file:    
        await update.message.reply_document(document=file, filename=fileName)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("status", return_status))
    application.add_handler(CommandHandler("quick_check", quick_check))
    application.add_handler(CommandHandler("logs", upload_logs))

    print("Bot started")
    application.run_polling()


# asyncio.run(main())
main()
