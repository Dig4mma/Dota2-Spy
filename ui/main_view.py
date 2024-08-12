import discord
import logging
import os
from discord.ui import View, Select, Button
from ui.modal_view import PlayerProfile
from cogs.match_cog import MatchCog  # Import MatchCog

logger = logging.getLogger(__name__)

class MainView(View):
    def __init__(self, match_cog: MatchCog):
        super().__init__()
        self.match_cog = match_cog  # Store a reference to the match cog
        self.selected_option = None  # Initialize an instance variable to store the selected option
        
        options = [
            discord.SelectOption(label="Player Profile", value="Player Profile", description="Search for a player's profile"),
            discord.SelectOption(label="Option 2", value="option_2", description="Description for option 2"),
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

    @discord.ui.button(label="Start Analysis", style=discord.ButtonStyle.primary, custom_id="start_analysis_button", row=1)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            logger.debug(f"Button clicked with selected option: {self.selected_option}")
            if self.selected_option == "Player Profile":
                custom_id = os.urandom(16).hex()  # Generate a unique custom_id for the modal
                await interaction.response.send_modal(PlayerProfile(self.match_cog, custom_id=custom_id))
                logger.debug(f"Sent PlayerProfile modal with custom_id: {custom_id}")
            else:
                await interaction.response.send_message("Please select an option first.", ephemeral=True)
        except Exception as e:
            logger.error(f"Error in button_callback: {str(e)}")