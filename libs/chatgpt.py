import asyncio
import datetime
import os

from pyrogram.errors.exceptions.bad_request_400 import (
    MessageNotModified,
    MessageTooLong,
)
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.types import Message
from revChatGPT.V1 import AsyncChatbot as GPTChatbot

gptBot = GPTChatbot(
    config={
        "email": os.environ.get("OPENAI_EMAIL"),
        "password": os.environ.get("OPENAI_PASSWORD"),
    }
)


async def ChatGPT(_, message: Message):
    if not message.reply_to_message:
        gptBot.reset_chat()
    prev_text: str = ""
    msg = await message.reply_text("Wait...", reply_to_message_id=message.id)
    last_edit = datetime.datetime.now().timestamp() * 1000
    msg_full = False
    response = gptBot.ask(message.text)
    async for data in response:
        bot_message = data["message"][len(prev_text) :]

        if bot_message:
            if datetime.datetime.now().timestamp() * 1000 - last_edit > 500:
                try:
                    if not msg_full:
                        msg = await msg.edit_text(
                            prev_text + bot_message, disable_web_page_preview=True
                        )
                        prev_text = ""
                    else:
                        msg = await message.reply_text(
                            bot_message,
                            disable_web_page_preview=True,
                            reply_to_message_id=msg.id,
                        )
                        msg_full = False
                        prev_text = ""
                except MessageNotModified:
                    prev_text = ""
                except MessageTooLong:
                    prev_text = bot_message
                    msg_full = True
                except FloodWait as e:
                    print(f"FloodWait Occured: {e.value}")
                    await asyncio.sleep(e.value)
                    prev_text += bot_message
                last_edit = datetime.datetime.now().timestamp() * 1000
            else:
                prev_text += bot_message
    # Remaning text
    if prev_text and prev_text != msg.text:
        try:
            await msg.edit_text(prev_text, disable_web_page_preview=True)
        except MessageTooLong:
            await message.reply_text(
                prev_text.removeprefix(msg.text),
                disable_web_page_preview=True,
                reply_to_message_id=msg.id,
            )
        except MessageNotModified:
            pass
