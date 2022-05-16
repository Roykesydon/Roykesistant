import logging
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
from utils.database import get_connection
from utils.security_guard import SecurityGuard

# print(telegram.__version__) # 13.11


class Roykesistant:
    def __init__(self):
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

        self.dispatcher.add_handler(CommandHandler("subscribe", self.subscribe))
        self.dispatcher.add_handler(CommandHandler("help", self.help))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.reply))

        """
        Startup the bot
        """
        self.updater.start_polling()

        """
        Notify all subscribers that the service has just restarted
        """

        """
        Get connection with subscribers
        """
        client = get_connection()
        db = client["telegram_bot_db"]
        subscribers_collection = db["subscriber"]

        for subscriber_data in subscribers_collection.find():
            chat_id = subscriber_data["chat_id"]
            self.dispatcher.bot.send_message(
                chat_id=f"{chat_id}", text="The service has just restarted"
            )

    def is_legal_user(self, username: str) -> bool:
        if username in self.config["username_white_list"]:
            return True
        return False

    def reply(self, update: Update, context: CallbackContext) -> None:
        """
        It is used to reply to the general message of the user.
        This function has not been implemented for the time being.
        """
        update.message.reply_text(text="Reply function hasn't implemented.")

    def help(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(
            text="help - View all instruction descriptions.\n\n\
subscribe - If you subscribe, you can receive messages from the bot broadcast to all subscribed users until the bot shuts down."
        )

    def subscribe(self, update: Update, context: CallbackContext) -> None:
        """
        If the person who sent the message is on the whitelist,
        Add username and chat_id to database as a member who receives messages from the bot
        """
        message = update["message"]
        sender_data = message["from_user"]
        username = str(sender_data["username"])
        chat_id = sender_data["id"]

        if not self.is_legal_user(username):
            update.message.reply_text(text="Permission denied")
            return

        """
        Get connection with subscribers
        """
        client = get_connection()
        db = client["telegram_bot_db"]
        subscribers_collection = db["subscriber"]

        """
        Check if the data is already in the database
        """
        if subscribers_collection.find_one({"username": username}) is not None:
            update.message.reply_text(text="You have already subscribed")
            return

        data = {"username": str(username), "chat_id": str(chat_id)}
        subscribers_collection.insert_one(data)

        update.message.reply_text(
            text=f"Subscribe Success!\n{sender_data['first_name']} {sender_data['last_name']}"
        )

    def shutdown(self) -> None:
        """
        Get connection with subscribers
        """
        client = get_connection()
        db = client["telegram_bot_db"]
        subscribers_collection = db["subscriber"]

        for subscriber_data in subscribers_collection.find():
            chat_id = subscriber_data["chat_id"]
            self.dispatcher.bot.send_message(
                chat_id=f"{chat_id}", text="The bot is going to shut down"
            )

    def send_message(self, message: str, usernames: List[str] = None) -> None:
        """
        Send a message to all chats in chat_list.
        If there are specific usernames, send a message to them instead of all users in chat_list.
        """

        """
        Get connection with subscribers
        """
        client = get_connection()
        db = client["telegram_bot_db"]
        subscribers_collection = db["subscriber"]

        for subscriber_data in subscribers_collection.find():
            chat_id = subscriber_data["chat_id"]
            self.dispatcher.bot.send_message(chat_id=f"{chat_id}", text=message)
