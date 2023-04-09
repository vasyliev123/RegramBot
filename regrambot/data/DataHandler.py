import json
from regrambot.config import DATA_FILE_PATH


class DataHandler:
    def __init__(self, file_path=DATA_FILE_PATH):
        self.file_path = file_path
        self.data = {}

    def load_data(self):
        # Load data from the file into the `data` dictionary
        with open(self.file_path, "r",encoding='utf-8') as f:
            self.data = json.load(f)

    def save_data(self):
        # Save the `data` dictionary into the file
        with open(self.file_path, "w",encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)

    def get_admins(self):
        # Return the list of admin users in the `data` dictionary
        return self.data["admins"]

    def add_admin(self, admin):
        # Add a new admin user to the `data` dictionary
        self.data["admins"].append(admin)

    def remove_admin_by_id(self, admin_id):
        # Remove an admin user with the specified ID from the `data` dictionary
        self.data["admins"] = [
            admin for admin in self.data["admins"] if admin["id"] != admin_id
        ]

    def get_channels(self):
        # Return the list of channels in the `data` dictionary
        return self.data["channels"]

    def add_channel(self, channel):
        # Add a new channel to the `data` dictionary
        self.data["channels"].append(channel)

    def remove_channel_by_id(self, channel_id):
        # Remove a channel with the specified ID from the `data` dictionary
        self.data["channels"] = [
            channel for channel in self.data["channels"] if channel["id"] != channel_id
        ]

    def get_channel_subs_to_scrape(self, channel_id):
        # Return the list of subreddits to scrape for a channel with the specified ID
        for channel in self.get_channels():
            if channel["id"] == channel_id:
                return channel["subredditsToScrape"]
        return []

    def get_imported_posts(self, channel_id):
        # Return the list of imported posts for a channel with the specified ID
        for channel in self.get_channels():
            if channel["id"] == channel_id:
                return channel["importedPosts"]
        return []

    def add_imported_post(self, channel_id, post):
        # Add a new imported post to the list of imported posts for a channel with the specified ID
        for channel in self.get_channels():
            if channel["id"] == channel_id:
                channel["importedPosts"].append(post)
                return
