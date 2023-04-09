from telegram.ext import CommandHandler, MessageHandler, filters
import random
from regrambot.utils import Utils


class Handlers:
    def __init__(self, reddit, data_handler) -> None:
        self.reddit = reddit
        self.data_handler = data_handler
        self.logger = Utils.get_logger(__name__)
    async def start(self, update, context):
        user_id = update.message.from_user.id
        self.data_handler.load_data()
        admins = self.data_handler.get_admins()
        channels = self.data_handler.get_channels()
        bot_id = context.bot.id
        if not any(admin["id"] == user_id for admin in admins):
            update.message.reply_text("You are not an admin")
            return

        for channel in channels:
            if not any(
                user_id == _.user.id
                for _ in await context.bot.get_chat_administrators(channel["id"])
            ):
                update.message.reply_text(f"You are not admin in {channel['name']}")
                return
            if not any(
                bot_id == _.user.id
                for _ in await context.bot.get_chat_administrators(channel["id"])
            ):
                update.message.reply_text(f"Bot is not admin in {channel['name']}")
                return

            await self.send_post(update, context, channel)

    async def send_post(self, update, context, channel):
        self.data_handler.load_data()
        subreddit = random.choice(
            self.data_handler.get_channel_subs_to_scrape(channel["id"])
        )
        self.logger.info(f"Sending post from {subreddit} to {channel['name']}")
        imported_posts = self.data_handler.get_imported_posts(channel["id"])
        post = self.reddit.get_random_top_post(subreddit)
        if post in imported_posts or not post.url.endswith((".jpg", ".png", ".gif")):
            await self.send_post(update, context, channel)
            return
        self.logger.info(f"Sending post {post.title} to {channel['name']}")

        self.data_handler.add_imported_post(channel["id"], post.url)
        self.data_handler.save_data()
        link = channel["link"]
        link_text = channel["caption"]
        title = Utils.format_title(post.title)
        caption = f"<b>{title}\n\n<a href='{link}'>{link_text}</a></b>"
        if post.url.endswith(".jpg") or post.url.endswith(".png"):
            await self.send_photo(context, caption, channel, post)
        else:
            await self.send_gif(context, caption, channel, post)
        

    async def send_photo(self, context, caption, channel, post):
        await context.bot.send_photo(
            chat_id=channel["id"],
            photo=post.url,
            caption=caption,
            parse_mode="HTML",
        )


    async def send_gif(self, context, caption, channel, post):
        await context.bot.send_animation(
            chat_id=channel["id"],
            animation=post.url,
            caption=caption,
            parse_mode="HTML",
        )

    def get_handlers(self):
        return [
            CommandHandler("start", self.start),
        ]
