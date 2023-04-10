from telegram.ext import CommandHandler, MessageHandler, filters
import random
import schedule
import time
from regrambot.utils import Utils


class Handlers:
    def __init__(self, reddit, data_handler) -> None:
        self.reddit = reddit
        self.data_handler = data_handler
        self.logger = Utils.get_logger(__name__)
        self.state = "idle"

    async def start(self, update, context):
        self.logger.info("Start command received")
        if self.state == "idle":
            self.state = "running"
            while True:  
                try:
                    user_id = update.message.from_user.id
                    self.data_handler.load_data()
                    admins = self.data_handler.get_admins()
                    channels = self.data_handler.get_channels()
                    bot_id = context.bot.id
                    if not any(admin["id"] == user_id for admin in admins):
                        update.message.reply_text("You are not an admin")
                        return

                    for channel in channels:
                        try:
                            chat_admins = await context.bot.get_chat_administrators(channel["id"])
                            if not any(user_id == _.user.id for _ in chat_admins):
                                update.message.reply_text(
                                    f"You are not admin in {channel['name']}")
                                continue
                            if not any(bot_id == _.user.id for _ in chat_admins):
                                update.message.reply_text(
                                    f"Bot is not admin in {channel['name']}")
                                continue

                            await self.send_post(update, context, channel)
                            time.sleep(10)
                        except Exception as e:
                            self.logger.exception(
                                f"Error occurred while fetching chat administrators for channel {channel['name']}: {str(e)}")
                            time.sleep(10)
                        
                
                except Exception as e:
                    self.logger.exception(
                        f"Error occurred while starting the bot: {str(e)}")
                    time.sleep(10)
        else:
            await update.message.reply_text("Bot is already running")
            return
    async def send_post(self, update, context, channel):
        try:
            # Load data from the data handler
            self.data_handler.load_data()

            # Choose a subreddit randomly from the list of subreddits to scrape for the channel
            subreddits = self.data_handler.get_channel_subs_to_scrape(channel["id"])
            if subreddits == []:
                self.logger.info(f"No subreddits to scrape for {channel['name']}")
                return
            
            subreddit = random.choice(subreddits)
            
            # Get the list of imported posts from the data handler for the channel
            imported_posts = self.data_handler.get_imported_posts(channel["id"])

            # Get a random top post from the chosen subreddit
            post = await self.reddit.get_random_hot_post(subreddit)
            self.logger.info(post.url)
            # If the post has already been imported or is not an image or gif, try again
            if post.url in imported_posts or (not post.url.endswith(".jpg") and not post.url.endswith(".png") and not post.url.endswith(".gif")):
                self.logger.info(f"Post {post.title} has already been imported or is not an image or gif")
                await self.send_post(update, context, channel)
                return

            self.logger.info(f"Sending post {post.title} to {channel['name']}")

            # Add the URL of the imported post to the list of imported posts for the channel
            self.data_handler.add_imported_post(channel["id"], post.url)

            # Save the data in the data handler
            self.data_handler.save_data()

            # Get the link and link text for the channel
            link = channel["link"]
            link_text = channel["caption"]

            # Format the post title
            title = Utils.format_title(post.title)

            # Format the caption with the post title, link, and link text
            caption = f"<b>{title}\n\n<a href='{link}'>{link_text}</a></b>"

            if post.url.endswith(".jpg") or post.url.endswith(".png"):
                await self.send_photo(context, caption, channel, post)
            else:
                await self.send_gif(context, caption, channel, post)
        except Exception as e:
            if str(e) == "recieved 403 HTTP response":
                self.logger.error(
                    f"Error occurred while sending post: No such subreddit {subreddit} or you are banned from it")
                return
            self.logger.error(f"Error occurred while sending post: {str(e)}")

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
