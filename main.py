import os 
import discord
from dotenv import load_dotenv

load_dotenv() # load all the variables from the env file
bot = discord.Bot()


bot.run(os.getenv('TOKEN')) # run the bot with the token