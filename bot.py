# (c) EDM115 - 2022

import os
import logging
import re
from pyrogram import Client, errors, filters
from pyrogram.types import BotCommand, Message
from pyrogram.errors import FloodWait, RPCError
import pyromod.listen
from config import *

texttourl = Client(
        "TextToUrl-bot",
        api_id = Config.API_ID,
        api_hash = Config.API_HASH,
        bot_token = Config.BOT_TOKEN,
        sleep_threshold = 10
    )

await texttourl.set_bot_commands([
    BotCommand("start", "Useless"),
    BotCommand("urlize", "Create text with link inside"),
    BotCommand("urlize2", "Same as above, but URL preview is disabled"),
    BotCommand("log", "Send you the logs, in case it's needed")])

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler('logs.txt'), logging.StreamHandler()],
    format="%(asctime)s - %(levelname)s - %(name)s - %(threadName)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARN)

url_regex = "((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

@texttourl.on_message(filters.command("start"))
async def start_bot(_, message: Message):
    await message.reply_text(text="**Hello {} 👋**\n\nI'm TextToUrl-bot, a bot made for creating texts with links inside.\nDo **/urlize** to start __(or **/urlize2** to do same without link preview)__".format(message.from_user.mention), disable_web_page_preview=True)

@texttourl.on_message(filters.command("log"))
async def send_logs(_, message: Message):
    with open('logs.txt', 'rb') as doc_f:
        try:
            await texttourl.send_document(
                chat_id=message.chat.id,
                document=doc_f,
                file_name=doc_f.name,
                reply_to_message_id=message.id
            )
            LOGGER.info(f"Log file sent to {message.from_user.id}")
        except FloodWait as e:
            sleep(e.x)
        except RPCError as e:
            message.reply_text(e, quote=True)
            LOGGER.warn(f"Error in /log : {e}")

@texttourl.on_message(filters.command(["urlize","urlize2"]))
async def urlize(_, message: Message):
    asking1 = await texttourl.ask(message.chat.id, "**Send me the text you wanna transform into a link :**")
    text = asking1.text
    asking2 = await texttourl.ask(message.chat.id, "**Now, send me the link you wanna put into that text :**")
    url = asking2.text
    preview = True if message.command[0]=="urlize2" else False
    if re.match(url_regex, url):
        try:
            await message.reply_text(f"[{text}]({url})",disable_web_page_preview=preview)
        except FloodWait as f:
            asyncio.sleep(f.x)
        except:
            try:
                await texttourl.send_message(chat_id=message.from_user.id, text=f"[{text}]({url})",disable_web_page_preview=preview)
            except Exception as e:
                LOGGER.error(str(e))
                await texttourl.send_message(chat_id=message.from_user.id, text="An unknown error happened 😔")
    else:
        await message.reply_text("That link is not valid 💀")


LOGGER.info("Bot started")
texttourl.run()
