import os
from dotenv import load_dotenv
from telegram import (
    Update,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
    CommandHandler
)

from gptconnector import get_response

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    menu = update.message.text
    if menu == '/menu':
        keyboard = [
            ["Track my Order"],
            ["Ask about a Product"],
            ["Provide a Feedback"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Please choose an option:",
            reply_markup=reply_markup
        )
    

async def msg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    print(f"Received message: {message}")
    
async def msg_llm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    reply_text = get_response(message)
    await update.message.reply_text(reply_text)

async def cmd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command = update.message.text
    print(f"Received command: {command}")
    if command == '/start':
        user_first_name = update.message.from_user.first_name if update.message.from_user else "there"
        reply_text = f"Hello {user_first_name}! Welcome to Quack Duck Bot."
        await update.message.reply_text(reply_text)


def main():
    load_dotenv()
    tbot_token = os.getenv('QUACK_DUCK_BOT_TOKEN')
    if tbot_token is None:
        raise ValueError("QUACK_DUCK_BOT_TOKEN environment variable is not set")

    tbot_application = Application.builder().token(tbot_token).build()

    # tbot_application.add_handler(MessageHandler(~filters.COMMAND, msg_handler))
    tbot_application.add_handler(MessageHandler(~filters.COMMAND, msg_llm_handler))
    # tbot_application.add_handler(MessageHandler(filters.COMMAND, cmd_handler))
    tbot_application.add_handler(MessageHandler(filters.COMMAND, menu_handler))
    tbot_application.add_handler(MessageHandler(filters.Regex("^(Track my Order|Ask about a Product|Provide a Feedback)$"), menu_handler))

    tbot_application.run_polling()

if __name__ == '__main__':
    main()
