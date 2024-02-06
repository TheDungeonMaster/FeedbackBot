from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace 'YOUR_TOKEN_HERE' with your bot's token
TOKEN = '6952588526:AAH3NQ-TECU2T3R1ltzkmalEB8YfzTBe25A'

# Replace 'GROUP_CHAT_ID' with the actual chat ID of your group
GROUP_CHAT_ID = '-1002043872444'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Hi! Send me something and I will forward it to the group!')


async def forward_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Forward received message to the group."""
    await context.bot.forward_message(chat_id=GROUP_CHAT_ID,
                                      from_chat_id=update.effective_chat.id,
                                      message_id=update.message.message_id)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non-command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_group))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == '__main__':
    main()
