import discord
from discord.ext import commands
from discord import app_commands
from scrapers.dotabuff_scraper import DotabuffScraper

class MatchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="recent_matches", description="Get recent Dota 2 matches for a player")
    async def recent_matches(self, interaction: discord.Interaction, player_id: str, num_matches: int = 5):
        await interaction.response.defer()  # Acknowledge the command and show loading state

        # Create scraper instance and fetch recent matches
        scraper = DotabuffScraper(player_id)
        try:
            overview = scraper.get_data('overview')
            matches = scraper.get_data('recent_matches')

            if overview:
                response = (
                    f"Player: {overview.get('name', 'Unknown')}\n"
                    f"Rank: {overview.get('rank', 'Unknown')}\n"
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

        await interaction.followup.send(response)

async def setup(bot):
    await bot.add_cog(MatchCog(bot))