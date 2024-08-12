import discord
from discord.ext import commands
from scrapers.dotabuff_scraper import DotabuffScraper
import os
import logging

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

    async def recent_matches(self, interaction: discord.Interaction, player_id: str, num_matches: int = 5):
        await interaction.response.defer()  # Acknowledge the command and show loading state

        scraper = DotabuffScraper(player_id)
        try:
            overview = scraper.get_data('overview')
            matches = scraper.get_data('recent_matches')

            if overview:
                response = (
                    f"Player: {overview.get('name', 'Unknown')}\n"
                    f"Rank: {overview.get('rank', 'Unknown')}\n"
                    f"Profile Image: {overview.get('profile_image', 'Unknown')}\n"
                    "--------------------\n"
                )
            else:
                response = "Overview data not found.\n--------------------\n"

            if matches:
                for match in matches[:num_matches]:  # Select only the specified number of matches
                    response += (
                        f"Hero: {match['hero']}\n"
                        f"Role: {match['role']}\n"  # Include the parsed role
                        f"Result: {match['result']}\n"
                        f"Type: {match['type']}\n"
                        f"Duration: {match['duration']}\n"
                        f"KDA: {match['kda']}\n"
                        f"Lobby Bracket: {match['lobby_bracket']}\n"
                        f"Date: {match['date']}\n"
                        "--------------------\n"
                    )
            else:
                response += f"No matches found for account {player_id}."
        except Exception as e:
            response = f"Error: {str(e)}"

        return response

async def setup(bot):
    await bot.add_cog(MatchCog(bot))