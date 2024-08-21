# ui/main_view.py
import discord
import logging
import os
from discord.ui import View, Select, Button
from cogs.match_cog import MatchCog
from ui.modal_view import PlayerProfile

logger = logging.getLogger(__name__)

class MainView(View):
    def __init__(self, match_cog: 'MatchCog'):
        super().__init__()
        self.match_cog = match_cog  # Store a reference to the match cog
        self.selected_option = None  # Initialize an instance variable to store the selected option
        
        options = [
            discord.SelectOption(label="Player Profile", value="Player Profile", description="Search for a player's profile"),
            discord.SelectOption(label="Find a match", value="Find a match", description="Search for a specific match"),
        ]
        
        select = Select(
            placeholder="Search for : ",
            options=options,
            custom_id="main_view_select",
            min_values=1,
            max_values=1,
            row=0
        )
        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        try:
            self.selected_option = interaction.data['values'][0]  # Store the selected option
            logger.debug(f"Selected option: {self.selected_option}")
            await interaction.response.defer()  # Acknowledge the interaction without sending a message
        except Exception as e:
            logger.error(f"Error in select_callback: {str(e)}")

    @discord.ui.button(label="Start Analysis", style=discord.ButtonStyle.success, custom_id="start_analysis_button", row=1)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            logger.debug(f"Button clicked with selected option: {self.selected_option}")
            if self.selected_option == "Player Profile":
                custom_id = os.urandom(16).hex()  # Generate a unique custom_id for the modal
                from ui.modal_view import PlayerProfile
                await interaction.response.send_modal(PlayerProfile(self.match_cog, custom_id=custom_id))
                logger.debug(f"Sent PlayerProfile modal with custom_id: {custom_id}")
            elif self.selected_option == "Find a match":
                # Add logic to handle "Find a match" option
                await interaction.response.send_message("Find a match option selected.", ephemeral=True)
            else:
                await interaction.response.send_message("Please select an option first.", ephemeral=True)
        except Exception as e:
            logger.error(f"Error in button_callback: {str(e)}")