import discord
from discord.ext import commands
import os
import logging
from ui.player_view import PlayerView
from api.stratz_api import StratzAPI
from scrapers.dotabuff_scraper import DotabuffScraper

logger = logging.getLogger(__name__)

class MatchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stratz_api = StratzAPI()

    @commands.command()
    async def show_modal(self, ctx):
        from ui.modal_view import PlayerProfile  # Import here to avoid circular dependency
        custom_id = os.urandom(16).hex()
        modal = PlayerProfile(match_cog=self, custom_id=custom_id)
        await ctx.send_modal(modal)
        logger.debug(f"PlayerProfile modal sent with custom_id: {custom_id}")

    async def show_modal_interaction(self, interaction):
        from ui.modal_view import PlayerProfile  # Import here to avoid circular dependency
        custom_id = os.urandom(16).hex()
        modal = PlayerProfile(match_cog=self, custom_id=custom_id)
        await interaction.response.send_modal(modal)
        logger.debug(f"PlayerProfile modal sent with custom_id: {custom_id}")

    async def recent_matches(self, interaction: discord.Interaction, player_id: str, num_matches: int = 5):
        await interaction.response.defer()
        try:
            scraper = DotabuffScraper(player_id)
            overview = scraper.get_data('overview')
            matches = scraper.get_data('recent_matches')[:num_matches]

            if not overview or not matches:
                raise ValueError("Player does not exist")

            player_view = PlayerView(player_data=overview, matches=matches, match_cog=self)
            embeds = player_view.create_embeds()
            buttons = player_view.create_buttons()

        except Exception as e:
            logger.error(f"Exception occurred: {str(e)}")
            embeds = [discord.Embed(title="Error", description=str(e), color=discord.Color.red())]

        for i, embed in enumerate(embeds):
            if i == len(embeds) - 1:
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
                logger.debug("Search Again button clicked")
                await self.show_modal_interaction(interaction)
            elif custom_id == "go_back_button":
                from ui.main_view import MainView
                view = MainView(self)
                embed = discord.Embed(
                    title="Welcome to Dota 2 Analysis Bot",
                    description="Analyze your recent Dota 2 matches, view player stats, and get detailed insights into your gameplay. Click the button below to start the analysis.",
                    color=discord.Color.green()
                )
                embed.set_image(url="https://cdn.discordapp.com/attachments/1081285481171538063/1272574461291397210/gif.gif")
                embed.set_author(name="Dota 2 Spy", icon_url="https://cdn.discordapp.com/attachments/1081285481171538063/1272574460943405180/author_icon.png")
                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    async def find_match(self, interaction: discord.Interaction, match_id: str):
        await interaction.response.defer()  # Acknowledge the command and show loading state

        try:
            match_data = self.stratz_api.get_match_data(match_id)

            if not match_data:
                raise ValueError("Match does not exist")

            # Process match_data and create a detailed embed
            match_info = match_data.get('data', {}).get('match', {})
            did_radiant_win = match_info.get('didRadiantWin', False)
            duration = match_info.get('durationSeconds', 0)
            lobby_type = match_info.get('lobbyType', 'Unknown')
            rank = match_info.get('rank', 'Unknown')
            bracket = match_info.get('bracket', 'Unknown')

            result = "Radiant Win" if did_radiant_win else "Dire Win"
            duration_minutes = duration // 60

            embed = discord.Embed(
                title=f"Match {match_id}",
                description=f"Result: {result}\nDuration: {duration_minutes} minutes\nLobby Type: {lobby_type}\nRank: {rank}\nBracket: {bracket}",
                color=discord.Color.green() if did_radiant_win else discord.Color.red()
            )

            # Add player details to the embed
            for player in match_info.get('players', []):
                player_name = player.get('steamAccount', {}).get('name', 'Unknown Player')
                hero_name = player.get('hero', {}).get('displayName', 'Unknown Hero')
                kills = player.get('kills', 0)
                deaths = player.get('deaths', 0)
                assists = player.get('assists', 0)
                kda = f"{kills}/{deaths}/{assists}"

                embed.add_field(name=f"{player_name} ({hero_name})", value=f"KDA: {kda}", inline=False)

        except Exception as e:
            logger.error(f"Exception occurred: {str(e)}")
            embed = discord.Embed(title="Error", description=str(e), color=discord.Color.red())

        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.debug("Match data sent successfully")


async def setup(bot):
    await bot.add_cog(MatchCog(bot))