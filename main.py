from loguru import logger
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Help!')


def echo(bot, update):
    update.message.reply_text(update.message.text, reply_to_message_id=update.message.message_id)


def welcome(bot, update):
    welcome_msg = "Seja bem vindo ao Grupy-RN!"
    update.message.reply_text(welcome_msg, reply_to_message_id=update.message.message_id)


def error(bot, update):
    logger.warning(f'Update {bot} caused error {update.error}')


def main():
    updater = Updater(config.BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()