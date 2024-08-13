import discord
from discord.ext import commands
from scrapers.dotabuff_scraper import DotabuffScraper
import os
import logging
from ui.player_view import PlayerView  # Import the PlayerView class

logger = logging.getLogger(__name__)

class MatchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def show_modal(self, ctx):
        from ui.modal_view import PlayerProfile  # Import here to avoid circular dependency
        custom_id = os.urandom(16).hex()  # Generate a unique custom_id
        modal = PlayerProfile(match_cog=self, custom_id=custom_id)
        await ctx.send_modal(modal)
        logger.debug(f"PlayerProfile modal sent with custom_id: {custom_id}")

    async def show_modal_interaction(self, interaction):
        from ui.modal_view import PlayerProfile  # Import here to avoid circular dependency
        custom_id = os.urandom(16).hex()  # Generate a unique custom_id
        modal = PlayerProfile(match_cog=self, custom_id=custom_id)
        await interaction.response.send_modal(modal)
        logger.debug(f"PlayerProfile modal sent with custom_id: {custom_id}")

    async def recent_matches(self, interaction: discord.Interaction, player_id: str, num_matches: int = 5):
        await interaction.response.defer()  # Acknowledge the command and show loading state

        scraper = DotabuffScraper(player_id)
        try:
            overview = scraper.get_data('overview')
            matches = scraper.get_data('recent_matches')[:num_matches]  # Limit the number of matches

            player_view = PlayerView(player_data=overview, matches=matches, match_cog=self)  # Create an instance of PlayerView
            embeds = player_view.create_embeds()  # Create the embeds

        except Exception as e:
            logger.error(f"Exception occurred: {str(e)}")
            embeds = [discord.Embed(title="Error", description=str(e), color=discord.Color.red())]

        for i, embed in enumerate(embeds):
            if i == len(embeds) - 1:  # Last embed, add buttons
                buttons = player_view.create_buttons()
                await interaction.followup.send(embed=embed, view=buttons, ephemeral=True)
            else:
                await interaction.followup.send(embed=embed, ephemeral=True)

        logger.debug("Embeds sent successfully")

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            custom_id = interaction.data.get('custom_id')
            if custom_id == "search_again_button":
                await self.show_modal_interaction(interaction)
            elif custom_id == "go_back_button":
                from ui.main_view import MainView
                view = MainView(self)
                embed = discord.Embed(
                    title="Welcome to Dota 2 Analysis Bot",
                    description="Analyze your recent Dota 2 matches, view player stats, and get detailed insights into your gameplay. Click the button below to start the analysis.",
                    color=discord.Color.blue()
                )
                embed.set_image(url="https://cdn.discordapp.com/attachments/1081285481171538063/1272574461291397210/gif.gif")
                embed.set_author(name="Dota 2 Spy", icon_url="https://cdn.discordapp.com/attachments/1081285481171538063/1272574460943405180/author_icon.png")
                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(MatchCog(bot))