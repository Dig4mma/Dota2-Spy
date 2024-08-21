import os
import asyncio
import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    logging.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    logging.info("------")

@bot.event
async def on_command_error(ctx, error):
    logging.error(f"Error in command {ctx.command}: {error}")

@bot.event
async def on_interaction(interaction):
    logging.debug(f"Interaction received: {interaction.data}")

async def main():
    async with bot:
        await bot.load_extension("cogs.match_cog")
        await bot.load_extension("cogs.ui_cog")
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())