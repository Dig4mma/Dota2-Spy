import discord
from discord.ext import commands
from discord import app_commands
from ui.main_view import MainView
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class UICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.debug("UICog initialized")

    @app_commands.command(name="dota", description="Show the main Dota 2 bot view")
    async def dota(self, interaction: discord.Interaction):
        logger.debug("Handling /dota command")
        embed = discord.Embed(
            title="Welcome to Dota 2 Analysis Bot",
            description="Analyze your recent Dota 2 matches, view player stats, and get detailed insights into your gameplay. Click the button below to start the analysis.",
            color=discord.Color.green()
        )
        embed.set_author(name="Dota 2 Spy", icon_url="attachment://author_icon.png")
        embed.set_image(url="attachment://gif.gif")

        file1 = discord.File("assets/author_icon.png", filename="author_icon.png")
        file2 = discord.File("assets/gif.gif", filename="gif.gif")

        logger.debug("Creating MainView instance with MatchCog")
        view = MainView(match_cog=self.bot.get_cog('MatchCog'))
        logger.debug("MainView instance created")

        try:
            await interaction.response.send_message(embed=embed, view=view, files=[file1, file2])
            logger.debug("Sent message with embed and view")
        except Exception as e:
            logger.error(f"Error handling /dota command: {e}")
            await interaction.response.send_message("An error occurred while processing the command.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(UICog(bot))
    logger.debug("UICog added to bot")