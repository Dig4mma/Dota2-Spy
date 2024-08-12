import discord
from discord.ui import Modal, TextInput
from typing import TYPE_CHECKING
import logging
import os

if TYPE_CHECKING:
    from cogs.match_cog import MatchCog

logger = logging.getLogger(__name__)

class PlayerProfile(Modal):
    def __init__(self, match_cog: 'MatchCog', *args, **kwargs) -> None:
        custom_id = kwargs.pop('custom_id', os.urandom(16).hex())
        super().__init__(title="Search for Player's Profile", custom_id=custom_id, *args, **kwargs)
        self.match_cog = match_cog

        self.add_item(TextInput(
            label="Player's Steam ID", 
            placeholder="example: 343443612", 
            required=True,
            custom_id="steam_player_id"
        ))
        self.add_item(TextInput(
            label="Number of recent matches to analyze", 
            placeholder="Enter the number of recent matches",
            default="5", 
            required=False,
            custom_id="num_recent_matches"
        ))

    async def on_submit(self, interaction: discord.Interaction):
        logger.debug(f"Entered PlayerProfile on_submit for custom_id: {self.custom_id}")
        try:
            player_id = self.children[0].value
            num_matches = self.children[1].value

            logger.debug(f"Extracted values - Player ID: {player_id}, Number of matches: {num_matches}")

            try:
                num_matches = int(num_matches)
                logger.debug(f"Validated - Number of matches is an integer: {num_matches}")
            except ValueError as e:
                logger.error(f"ValueError: {str(e)}")
                await interaction.response.send_message(f"Error: Number of recent matches must be an integer.", ephemeral=True)
                return

            # Call the match_cog function and use followup to send the response
            response = await self.match_cog.recent_matches(interaction, player_id, num_matches)
            logger.debug(f"Received response from recent_matches: {response}")

            await interaction.followup.send(response)  # Send the response using followup
            logger.debug("Response sent")
        except Exception as e:
            logger.error(f"Error in PlayerProfile on_submit for custom_id {self.custom_id}: {str(e)}")
            if not interaction.response.is_done():
                await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)
            else:
                await interaction.followup.send(f"Error: {str(e)}", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        logger.error(f"Error in PlayerProfile modal for custom_id {self.custom_id}: {str(error)}")
        if not interaction.response.is_done():
            await interaction.response.send_message("An error occurred while processing your request.", ephemeral=True)
        else:
            await interaction.followup.send("An error occurred while processing your request.", ephemeral=True)

    async def on_timeout(self) -> None:
        logger.warning(f"PlayerProfile modal interaction timed out for custom_id {self.custom_id}.")