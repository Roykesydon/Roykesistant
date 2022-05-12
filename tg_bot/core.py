import string
import time
from re import A
from tokenize import String
from typing import List

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from utils.config import get_config
from utils.SecurityGuard import SecurityGuard

# print(telegram.__version__) # 13.11


class Roykesistant:
    def __init__(self):

        self.chat_list = []

        """
        Get token
        """
        self.config = get_config()
        self.token = self.config["token"]

        """
        Initialize bot
        """
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_handler(CommandHandler("start", self.start))

        """
        Startup the bot
        """
        self.updater.start_polling()

    def is_legal_user(self, username: str):
        if username in self.config["username_white_list"]:
            return True
        return False

    def start(self, update: Update, context: CallbackContext):
        """
        If the person who sent the message is on the whitelist,
        Add chat id to chat_list as a member who receives messages from the bot
        """
        message = update["message"]
        sender_data = message["from_user"]
        username = str(sender_data["username"])
        chat_id = sender_data["id"]

        if not self.is_legal_user(username):
            update.message.reply_text(text="permission denied")
            return

        if (username, chat_id) not in self.chat_list:
            self.chat_list.append((username, chat_id))

        update.message.reply_text(
            text=f"Hi! {sender_data['first_name']} {sender_data['last_name']}"
        )

    def shutdown(self):
        for username, chat_id in self.chat_list:
            self.dispatcher.bot.send_message(
                chat_id=f"{chat_id}", text="The bot is going to shut down."
            )

    def send_message(self, message: str, usernames: List[str] = None):
        """
        Send a message to all chats in chat_list.
        If there are specific usernames, send a message to them instead of all users in chat_list.
        """
        for username, chat_id in self.chat_list:
            self.dispatcher.bot.send_message(chat_id=f"{chat_id}", text=message)
