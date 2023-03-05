import datetime
import json
import os
import re

from EdgeGPT import Chatbot as BingChatbot
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageNotModified,
    MessageTooLong,
)
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.types import Message

BING_COOKIES = json.loads(os.environ.get("BING_COOKIES"))

edgeGPT = BingChatbot(cookies=BING_COOKIES)


async def BingAI(_, message: Message):
    # If message is not a reply then create new edgeGPT chat
    if not message.reply_to_message:
        await edgeGPT.reset()
    prompt = message.text
    # time in milliseconds
    last_edit = datetime.datetime.now().timestamp() * 1000
    msg = await message.reply_text("Wait...", reply_to_message_id=message.id)
    msg_full = False
    response = edgeGPT.ask_stream(prompt)
    # Reply streaming response by chunks with editing the message, exluding the last chunk
    async for chunk in response:
        response = chunk[1]
        # for every string similar to [1]: https://www.alliedmarketresearch.com/deep-learning-market "Deep Learning Market Size, Share | Research Report - 2030"
        # Group 1: [1]:
        # Group 2: https://www.alliedmarketresearch.com/deep-learning-market
        # Group 3: "Deep Learning Market Size, Share | Research Report - 2030"
        ref_link_regex = re.compile(r"\[(\d+)\]:\s(https?:\/\/\S+)\s\"(.*)\"")
        try:
            # then remove the pattern from the response
            response = ref_link_regex.sub("", response)
            # remove annoying brackets around numbers
            response = re.sub(r"\[\^?\d+\^?\]", "", response)
        except TypeError:
            pass

        # Check if existing message is same as new message
        if response and datetime.datetime.now().timestamp() * 1000 - last_edit > 300:
            try:
                # Automatically edit the message until it exceeds max message length then send new messages
                if not msg_full:
                    msg = await msg.edit_text(response, disable_web_page_preview=True)
                else:
                    msg = await message.reply_text(
                        response,
                        disable_web_page_preview=True,
                        reply_to_message_id=message.id,
                    )
                last_edit = datetime.datetime.now().timestamp() * 1000
            except MessageTooLong:
                msg_full = True
            except MessageNotModified:
                pass
