from regrambot.telegram.TelegramBot import TelegramBot
import asyncio
def run():
    
    bot = TelegramBot()
    asyncio.run(bot.run())
    
