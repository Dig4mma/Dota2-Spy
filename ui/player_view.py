import discord

class PlayerView:
    def __init__(self, player_data, matches, match_cog):
        self.player_data = player_data
        self.matches = matches
        self.match_cog = match_cog

    def create_embeds(self):
        # Calculate win/loss statistics
        win_count = sum('won' in match['result'].lower() for match in self.matches)
        loss_count = len(self.matches) - win_count
        win_rate = (win_count / len(self.matches)) * 100 if self.matches else 0

        # Set embed color based on win rate
        embed_color = discord.Color.green() if win_rate >= 50 else discord.Color.red()

        # Use the player's name as the title of the embed
        title = self.player_data.get('name', 'Unknown') if self.player_data else 'Unknown Player'

        embeds = []
        
        def create_embed():
            embed = discord.Embed(title=title, color=embed_color)
            if self.player_data:
                embed.set_thumbnail(url=self.player_data.get('profile_image', 'Unknown'))

                rank = self.player_data.get('rank', 'Unknown')
                rank_image_url = self.player_data.get('rank_image', '')

                if rank_image_url:
                    embed.set_author(name=rank, icon_url=rank_image_url)
                else:
                    embed.set_author(name=rank)
            else:
                embed.add_field(name="Overview", value="Data not found", inline=False)
            return embed

        current_embed = create_embed()
        current_embed.add_field(name="\u200b", value="\u200b", inline=False)

        if self.matches:
            for idx, match in enumerate(self.matches):
                if idx > 0 and idx % 8 == 0:
                    embeds.append(current_embed)
                    current_embed = create_embed()
                    current_embed.add_field(name="\u200b", value="\u200b", inline=False)

                result = match['result'].lower()
                if 'won' in result:
                    result_text = f"```diff\n+ {match['result']}\n```"
                else:
                    result_text = f"```diff\n- {match['result']}\n```"

                current_embed.add_field(name=match['hero'], value=match['role'], inline=True)
                current_embed.add_field(name="Result", value=result_text, inline=True)
                current_embed.add_field(name=match['duration'], value=match['date'], inline=True)

            embeds.append(current_embed)
        else:
            current_embed.add_field(name="Matches", value="No recent matches found.", inline=False)

        # Add footer with win/loss statistics to the last embed
        if embeds:
            footer_text = (
                f"Showing the last {len(self.matches)} matches.\n"
                f"{win_count} wins\n"
                f"{loss_count} losses\n"
                f"Win rate: {win_rate:.2f}%"
            )
            embeds[-1].set_footer(text=footer_text)

        return embeds

    def create_buttons(self):
        buttons = discord.ui.View()

        search_again_button = discord.ui.Button(label="Search Again", style=discord.ButtonStyle.primary, custom_id="search_again_button")
        go_back_button = discord.ui.Button(label="Go Back", style=discord.ButtonStyle.secondary, custom_id="go_back_button")

        buttons.add_item(search_again_button)
        buttons.add_item(go_back_button)

        return buttons