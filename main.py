from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import api_key

# Replace 'YOUR_TOKEN_HERE' with your bot's token
TOKEN = api_key.TOKEN

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


async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Forward reply from the group to the original user who sent the message."""
    global message_map
    reply_to_message = update.message.reply_to_message

    # Check if the message is a reply to a forwarded message
    if reply_to_message and reply_to_message.message_id in message_map:
        original_chat_id = message_map[reply_to_message.message_id]
        # Send the reply to the original sender in a private chat
        await context.bot.send_message(chat_id=original_chat_id,
                                       text=f"Reply from group chat: {update.message.text}")


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_group))
    # Handler for messages, checks if the message is a reply
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE & filters.ChatType.GROUP, reply_to_user))

    application.run_polling()

if __name__ == '__main__':
    main()
