from typing import Optional
from discord.ext import commands
import discord
from common.utils.configutil import fetch_convar
from common.utils import database_manager as db

GIVEAWAY_CHANNEL_ID = fetch_convar("GIVEAWAY_CHANNEL_ID")

class GiveawayView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Enter Giveaway", style=discord.ButtonStyle.green, custom_id="enter:giveaway", emoji="🎉")
    async def enter_giveaway(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not db.already_linked(discord_id=interaction.user.id):
            embed = discord.Embed(
                title="❌ You are not linked!",
                description="You must link your Kick account to enter giveaways. This assures giveaway fairness and also ensures that any subscriber bonuses are applied to your entry."
            )
            
            embed.add_field(
                '🔗 Link your account',
                'To link your account, run the `/link` command in any Discord channel.'
            )
            
            

@commands.hybrid_command(name="giveaway", description='Giveaway controls.')
async def giveaway(ctx, action: str, title: str, description: str, image_url: str):
    if action == "create":
        embed = discord.Embed(
            title=f"🎉 {title}",
            description=description
        )
        
        embed.set_thumbnail(url=image_url)
        
        embed.add_field(
            name="🎫 Entries",
            value=0,
            inline=True
        )
        
        embed.add_field(
            name="👥 Host",
            value=ctx.author.mention,
            inline=True
        )
        
        view = GiveawayView()
        channel = ctx.guild.get_channel(GIVEAWAY_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed, view=view)
            await ctx.send("Giveaway created!", ephemeral=True)
        else:
            await ctx.send("Giveaway channel not found.", ephemeral=True)
    elif action == "end":
        # You would implement the logic for ending a giveaway here
        pass
    else:
        await ctx.send("Invalid action. Valid actions are `create` and `end`.", ephemeral=True)

async def setup(client):
    client.add_command(giveaway)
