from praw import Reddit
from regrambot.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, REDDIT_PASSWORD, REDDIT_USERNAME
import random
class RedditAPI:
    
    def __init__(self):
        
        self.reddit = Reddit(client_id=REDDIT_CLIENT_ID,
                             client_secret=REDDIT_CLIENT_SECRET,
                             password=REDDIT_PASSWORD,
                             user_agent=REDDIT_USER_AGENT,
                             username=REDDIT_USERNAME,)

    def get_reddit(self):
        return self.reddit
    
    def get_subreddit(self, subreddit_name):
        return self.reddit.subreddit(subreddit_name)
    
    def get_subreddit_hot(self, subreddit_name):
        return self.get_subreddit(subreddit_name).hot(limit=10)
    
    def get_random_hot_post(self, subreddit_name):
        return random.choice(list(self.get_subreddit_hot(subreddit_name)))
    
    
    def get_subreddit_new(self, subreddit_name):
        return self.get_subreddit(subreddit_name).new(limit=10)
    
    def get_subreddit_top(self, subreddit_name):
        return self.get_subreddit(subreddit_name).top(limit=20)
    
    def get_random_top_post(self, subreddit_name):
        return random.choice(list(self.get_subreddit_top(subreddit_name)))
    
    def get_subreddit_rising(self, subreddit_name):
        return self.get_subreddit(subreddit_name).rising(limit=10)
    