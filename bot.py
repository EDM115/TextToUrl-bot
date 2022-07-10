# (c) EDM115 - 2022

import os
import logging
import time
from pyrogram import Client, errors, filters, idle
from pyrogram.types import Message, ChatMember
from pyrogram.errors import FloodWait, RPCError
import pyromod.listen
from config import *

# Initialize the client here
texttourl = Client(
        "TextToUrl-bot",
        api_id = Config.API_ID,
        api_hash = Config.API_HASH,
        bot_token = Config.BOT_TOKEN,
        sleep_threshold = 10
    )

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler('logs.txt'), logging.StreamHandler()],
    format="%(asctime)s - %(levelname)s - %(name)s - %(threadName)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARN)

# handle /start with a cute message
@texttourl.on_message(filters.command("start"))
async def start_bot(_, message: Message):
    await message.reply_text(text="**Hello {} 👋**\n\nI'm TextToUrl-bot, a bot made for creating texts with links inside.\nDo **/urlize** to start".format(message.from_user.mention), disable_web_page_preview=True)

# Added /log for bug tracking
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

@texttourl.on_message(filters.command("urlize"))
async def urlize(_, message: Message):
    asking1 = await texttourl.ask(message.chat.id, "**Send me the text you wanna transform into a link :**")
    text = asking1.text
    asking2 = await texttourl.ask(message.chat.id, "**Now, send me the link you wanna put into that text :**")
    url = asking2.text
            try:
                await _.copy_message(
                    chat_id=dest,
                    from_chat_id=target,
                    message_id=id 
                )
            except FloodWait as f:
                asyncio.sleep(f.x)
                id-=1
            except Exception:
                continue
    except Exception as e:
        await message.reply_text(str(e))
    await message.reply_text("Done Forwarding")

# Run the bot
LOGGER.info("We start captain !")
texttourl.run()
