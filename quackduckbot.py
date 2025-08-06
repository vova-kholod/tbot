import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

async def msg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    print(f"Received message: {message.text}")

async def cmd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command = update.message.text
    print(f"Received command: {command}")

def main():
    load_dotenv()
    token = os.getenv('QUACK_DUCK_BOT_TOKEN')
    if token is None:
        raise ValueError("QUACK_DUCK_BOT_TOKEN environment variable is not set")

    application = Application.builder().token(token).build()

    application.add_handler(MessageHandler(~filters.COMMAND, msg_handler))
    application.add_handler(MessageHandler(filters.COMMAND, cmd_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
