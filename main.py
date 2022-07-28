from ast import Call
import logging
from tkinter import PhotoImage
from turtle import update
import random 
import requests
import re

from telegram import Update, Chat
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, PicklePersistence

from settings import BOT_TOKEN, SUPER_ADMIN_ID, DEBUG

logger        = logging.getLogger(__name__)
command_regex = r"s[\/](.+)[\/](.+)"

def recognize_text(photo_data) -> str:
    return "NOT IMPLEMENTED"

def replace_text_on_photo(photo: bytearray, text: str) -> bytearray:
    # NOT IMPLEMENTED
    return photo


def error(update, context):
    logger.warning('Пошел я нахуй. Update "%s" caused error "%s"', update, context.error)

def message_handler(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    
    if not message.reply_to_message or not message.reply_to_message.photo:
        message.reply_text("Reply to a photo to use the bot")
        return
    
    photo_id   = message.reply_to_message.photo[-1].file_id
    photo_file = context.bot.get_file(photo_id)
    photo      = requests.get(photo_file.file_path, stream=True).content
    photo_text = recognize_text(photo)
    
    if not photo_text or len(photo_text) == 0:
        message.reply_text("Cannot recognize any test from the photo")
        return
    
    match = re.search(command_regex, message.text)
    
    text_replace_from = match.group(1)
    text_replace_to   = match.group(2)
    
    if DEBUG:
        logger.info("Replacing '%s' to '%s'" % (text_replace_to, text_replace_from))
        
    updated_text = photo_text.replace(text_replace_from, text_replace_to)
    
    updated_photo = replace_text_on_photo(photo, updated_text)
    
    if updated_photo:
        message.reply_photo(updated_photo)
    else:
        message.reply_text("Something went wrong")
        
    return
    
def any_message(update, context):
    pass


def main() -> None:
    updater = Updater(BOT_TOKEN)

    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command & Filters.reply & Filters.regex(command_regex),
        message_handler
    ))
    
    dispatcher.add_handler(MessageHandler(Filters.all, any_message))
    dispatcher.add_error_handler(error)

    logger.info(f"Start Polling...")
    updater.start_polling()
    
    updater.idle()


if __name__ == '__main__':
    main()
