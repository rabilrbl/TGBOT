import os
import random

import uvloop
from pyrogram import Client, filters
from pyrogram.types import Message

from tgbot.libs.bingai import BingAI
from tgbot.libs.chatgpt import ChatGPT
from pyrogram import enums

uvloop.install()

app = Client(
    "TGBOT",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=os.environ.get("API_ID"),
    api_hash=os.environ.get("API_HASH"),
)

# Create a middleware to check if environment variables are set 
# if not, bot will ask to set them
@app.on_message(filters.private & ~filters.me)
async def check_env(client, message: Message):
    if not os.environ.get("AUTHORIZED_USERS"):
        await message.reply_text("AUTHORIZED_USERS is not set. Please send /setvar AUTHORIZED_USERS")
        await message.stop_propagation()
    if not os.environ.get("BING_COOKIES"):
        await message.reply_text("BING_COOKIES is not set. Please send /setvar BING_COOKIES")
        await message.stop_propagation()
    if not os.environ.get("OPENAI_EMAIL"):
        await message.reply_text("OPENAI_EMAIL is not set. Please send /setvar OPENAI_EMAIL")
        await message.stop_propagation()
    if not os.environ.get("OPENAI_PASSWORD"):
        await message.reply_text("OPENAI_PASSWORD is not set. Please send /setvar OPENAI_PASSWORD")
        await message.stop_propagation()


@app.on_message(filters.command("setvar"))
async def setvar(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /setvar [variable name]")
        return
    var = message.command[1]
    value = client.ask(message.chat.id, f"Enter value for {var}")
    os.environ[var] = value


CHAT_MODE = "gpt"
AUTHORIZED_USERS = os.environ.get("AUTHORIZED_USERS").split(",")

@app.on_message(filters.private & ~filters.me & ~filters.command("ping"))
async def set_typing_status(client, message: Message):
    """Set typing status while processing a message."""
    # Set typing status
    await client.send_chat_action(message.chat.id, enums.chat_action.ChatAction.TYPING)
    # Continue processing current message
    await message.continue_propagation()
    # Set typing status to False after processing current message
    await client.send_chat_action(message.chat.id, enums.chat_action.ChatAction.CANCEL)


# Create a middleware to check if users username is in the authorized users list
@app.on_message(filters.private & ~filters.me & ~filters.user(AUTHORIZED_USERS))
async def auth(_, message: Message):
    await message.reply_text("You are not authorized to use this bot.")
    await message.stop_propagation()


@app.on_message(filters.command("start"))
async def start(_, message):
    welcome_text = "Welcome to TG-BOT"
    await message.reply_text(welcome_text)


@app.on_message(filters.command("help"))
async def help(_, message):
    help_text = """**Help**
"""
    await message.reply_text(help_text)


@app.on_message(filters.command("ping"))
async def ping(_, message):
    await message.reply_text("Pong")


@app.on_message(filters.command("echo"))
async def echo(_, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /echo [text]")
        return
    text = message.text.split(None, 1)[1]
    await message.reply_text(text)


@app.on_message(filters.command("info"))
async def info(_, message):
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
async def chat_mode(_, message):
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
async def msginfo(_, message):
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
async def unknown(_, message):
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
async def sticker(_, message: Message):
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


app.run()
