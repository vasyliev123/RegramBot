from telegram.ext import ApplicationBuilder
from regrambot.config import TELEGRAM_BOT_TOKEN
from regrambot.reddit.RedditAPI import RedditAPI
from regrambot.telegram.handlers.Handlers import Handlers
from regrambot.data.DataHandler import DataHandler
from regrambot.utils import Utils

class TelegramBot:
    def __init__(self):
        # initialize the bot's components and attributes

        self.app = None
        self.handlers = None
        self.data_handler = DataHandler()
        self.reddit = RedditAPI()
        self.logger = Utils.get_logger(__name__)
        # initialize the bot's Telegram application
        self._init()
        self.logger.info("Telegram bot initialized")
    def _init(self):
        # build the Telegram application and add the bot's handlers to it
        self.app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        self.handlers = Handlers(self.reddit, self.data_handler).get_handlers()
        self.app.add_handlers(self.handlers)

    def run(self):
        # run the bot's Telegram application
        self.app.run_polling()
