import os
import random

from pyrogram import Client, filters
from pyrogram.types import Message

from libs.bingai import BingAI
from libs.chatgpt import ChatGPT

app = Client(
    "TGBOT",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=os.environ.get("API_ID"),
    api_hash=os.environ.get("API_HASH"),
)

CHAT_MODE = "gpt"
AUTHORIZED_USERS = os.environ.get("AUTHORIZED_USERS").split(",")


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


@app.on_message()
async def chatbot(client, message: Message):
    match CHAT_MODE:
        case "bing":
            await BingAI(client, message)
        case "gpt":
            await ChatGPT(client, message)
        case _:
            pass


def start():
    app.run()
