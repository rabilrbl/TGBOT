from pyrogram import Client, filters
import os, random, re, asyncio, datetime, aiohttp
from EdgeGPT import Chatbot as BingChatbot
from pyrogram.types import Message
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageNotModified,
    MessageTooLong,
)
from pyrogram.errors.exceptions.flood_420 import FloodWait
from revChatGPT.V1 import AsyncChatbot as GPTChatbot

app = Client(
    "TGBOT",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=os.environ.get("API_ID"),
    api_hash=os.environ.get("API_HASH"),
)

CHAT_MODE = "gpt"

edgeGPT = BingChatbot(cookiePath="cookies.json")
gptBot = GPTChatbot(config={"email": os.environ.get("OPENAI_EMAIL"), "password": os.environ.get("OPENAI_PASSWORD")})

AUTHORIZED_USERS = os.environ.get("AUTHORIZED_USERS").split(",")

STICKERS = [
    "CAACAgIAAxkBAAIXKmP_wt57GT92DcaU43nQw8S5xyTdAAKvJQACm6JwS7g5xX27XghmHgQ",
    "CAACAgUAAxkBAAIXLGP_wv0azEjRsGMJJES1bqC0vHIIAALIBwACTDaYV8VOMbFmOAf2HgQ",
    "CAACAgUAAxkBAAIXLmP_wweokBARXWU5T8m02Kky7RwPAAIaCgAC-lRxVyvUncXmz-R4HgQ",
    "CAACAgIAAxkBAAIXMGP_wxPyQ9jwmZwAAf2k3X1N3oARMAACzQEAAhZCawrL2Zt7FoIvuB4E",
    "CAACAgIAAxkBAAIXMmP_wx_lpTs1LDq2iK_8Bd-OWSfYAAKfAQACFkJrCmWMf9oXSSAlHgQ",
    "CAACAgIAAxkBAAIXNGP_wygbuIU3iFs_5R8NIR5NO2X_AAJyEgACRuWpSPJMG0U-1wNRHgQ",
    "CAACAgIAAxkBAAIXNmP_wyw5u4x66TVRbUdnB0JoYkNaAAKjDgAC1rIwSRpDkGil29d8HgQ",
    "CAACAgIAAxkBAAIXOGP_wz2I2KijIQWGQZuySPYAAV81WwACRAADKA9qFFts_7_cyqtAHgQ",
    "CAACAgIAAxkBAAIXOmP_w0exI9_75n2sZ0BpzRbgYVA4AAIEAQAC9wLIDyAPdzvpq8hJHgQ",
    "CAACAgQAAxkBAAIXPGP_w00ySHSQBgjOiKWJxSu7clOjAALqCwACbCIRU61ZQKi3F88DHgQ",
    "CAACAgQAAxkBAAIXPmP_w1c-meLecHvVteL0IqUUmvxoAAK9CQACelwRUzpqVCTmeOrfHgQ",
]


# Create a middleware to check if users username is in the authorized users list
@app.on_message(filters.private & ~filters.me & ~filters.user(AUTHORIZED_USERS))
async def auth(client, message: Message):
    await message.reply_text("You are not authorized to use this bot.")
    await message.stop_propagation()


@app.on_message(filters.command("start"))
async def start(client, message):
    welcome_text = "Welcome to TG-BOT"
    await message.reply_text(welcome_text)


@app.on_message(filters.command("help"))
async def help(client, message):
    help_text = """**Help**
"""
    await message.reply_text(help_text)


@app.on_message(filters.command("ping"))
async def ping(client, message):
    await message.reply_text("Pong")


@app.on_message(filters.command("echo"))
async def echo(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /echo [text]")
        return
    text = message.text.split(None, 1)[1]
    await message.reply_text(text)


@app.on_message(filters.command("info"))
async def info(client, message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = message.from_user
    text = f"""
**Your ID**: `{user.id}`
**Chat ID**: `{message.chat.id}`
"""
    await message.reply_text(text)


# Command /cm to change chat mode
@app.on_message(filters.command("cm"))
async def chat_mode(client, message):
    global CHAT_MODE
    if len(message.command) < 2:
        await message.reply_text("Current chat mode: " + CHAT_MODE)
        return
    mode = message.text.split(None, 1)[1]
    if mode not in ["bing", "gpt"]:
        await message.reply_text("Invalid mode")
        return
    CHAT_MODE = mode
    await message.reply_text(f"Chat mode changed to `{mode}`")



# Command to delete a message
@app.on_message(filters.command("del"))
async def delete(client, message: Message):
    if message.reply_to_message:
        msg_id = message.reply_to_message.id
    else:
        msg_id = message.text.split(None, 1)[1]
    try:
        await client.delete_messages(message.chat.id, msg_id)
    except Exception as e:
        await message.reply_text(str(e))
        return
    await message.delete()


# Command to give details of replied message
@app.on_message(filters.command("msginfo"))
async def msginfo(client, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a message to get details")
        return
    msg = message.reply_to_message
    text = f"""
**Message ID**: `{msg.id}`
**From**: `{msg.from_user.id}`
**Chat ID**: `{msg.chat.id}`
**Date**: `{msg.date}`
"""
    await message.reply_text(text)


@app.on_message(filters.create(lambda _, __, m: m.text and m.text.startswith("/")))
async def unknown(client, message):
    # Generate random funny response
    random_responses = [
        "I don't know that command",
        "What?",
        "Excuse me?",
        "I don't understand",
        "What are you talking about?",
        "I don't know what you mean",
        "I don't know what to say",
        "Go away",
        "Fall in a hole",
        "I don't care",
        "I'm not listening",
        "Are you talking to me?",
    ]
    await message.reply_text(random.choice(random_responses))


# For any sticker sent to the bot, reply with sticked id
@app.on_message(filters.sticker)
async def sticker(client, message: Message):
    await message.reply_text(message.sticker.file_id)


async def BingAI(client, message: Message):
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
        if datetime.datetime.now().timestamp() * 1000 - last_edit > 300:
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


async def GPTAI(client, message: Message):
    if not message.reply_to_message:
        gptBot.reset_chat()
    prev_text = ""
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
                        msg = await msg.edit_text(prev_text + bot_message, disable_web_page_preview=True)
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
                last_edit = datetime.datetime.now().timestamp() * 1000
            else:
                prev_text += bot_message
    # Remaning text
    if prev_text:
        try:
            await msg.edit_text(msg.text + prev_text, disable_web_page_preview=True)
        except MessageTooLong:
            await message.reply_text(prev_text.removeprefix(msg.text), disable_web_page_preview=True, reply_to_message_id=msg.id)             


@app.on_message()
async def chatbot(client, message: Message):
    match CHAT_MODE:
        case "bing":
            await BingAI(client, message)
        case "gpt":
            await GPTAI(client, message)
        case _:
            pass


app.run()
