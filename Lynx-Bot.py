import requests
import json

from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler,
)


TOKEN = "<TELEGRAM BOT API TOKEN HERE>"
BOT_USERNAME = "<@BOTNAME HERE>"

api_key = "<CHATGPT API TOKEN HERE"
api_url = "https://api.openai.com/v1/chat/completions"


# Functions
def chat_with_gpt(prompt):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": f"You are a {expertise} expert assistant."},
            {"role": "user", "content": f"{prompt}"},
        ],
        "temperature": 1.0,
        "top_p": 1.0,
        "n": 1,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 0,
    }

    response = requests.post(api_url, headers=headers, json=data)
    # print(response.status_code)
    # print(json.dumps(response.json(), indent=2))
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error occurred while communicating with GPT."


# expertise = "astronomer"
# prompt = "The odds of mars colliding with earth"
# response = chat_with_gpt(prompt)
# print(response)


# Command 1 - Start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await update.message.reply_text("Hello! Thanks for chatting with me! Pouncing Lynx here!")
    keyboard = [
        [
            InlineKeyboardButton("Ai Chat", callback_data="1"),
            InlineKeyboardButton("NA", callback_data="2"),
        ],
        [InlineKeyboardButton("NA", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Hello\n Please choose a feature:", reply_markup=reply_markup
    )
    # Doesn't work
    # await update.message.reply_text(f"{callback_data}")


'''
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")
'''


# Command 3 - unused
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("An Ai to answer your queries! Just type away!")


# Command 4 - custom
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(response)


# Responses


def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "hello" in processed:
        return "Hey there!"

    if "how are you" in processed:
        return "I am good!"

    return "I don't understand"


# Take care of response from user
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Starting bot..")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    # app.add_handler(CommandHandler(CallbackQueryHandler(button)))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    # Messages

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
