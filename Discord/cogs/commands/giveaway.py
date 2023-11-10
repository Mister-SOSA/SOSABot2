from typing import Optional
from discord.ext import commands
import discord
from common.utils.configutil import fetch_convar
from common.utils import database_manager as db
from utils.owner_notifier import notify_owner

GIVEAWAY_CHANNEL_ID = fetch_convar("GIVEAWAY_CHANNEL_ID")

class GiveawayView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Enter Giveaway", style=discord.ButtonStyle.green, custom_id="enter:giveaway", emoji="🎉")
    async def enter_giveaway(self, interaction: discord.Interaction, button: discord.ui.Button):
        current_giveaway = await db.fetch_open_giveaway()
        
        if not current_giveaway:
            embed = discord.Embed(
                title="❌ This giveaway is closed.",
                description="There is no giveaway currently open for that matter."
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            await notify_owner(interaction.client, title="Closed Giveaway Entry Attempted", description=f"User {interaction.user.name} attempted to enter a closed giveaway.", color=discord.Color.red())
            return
        
        if not await db.already_linked(discord_id=interaction.user.id):
            embed = discord.Embed(
                title="❌ You are not linked!",
                description="You must link your Kick account to enter giveaways. This assures giveaway fairness and also ensures that any subscriber bonuses are applied to your entry."
            )
            
            embed.add_field(
                name="**How to Link**",
                value="To link your account, simply call `/link` in any Discord channel."
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            await notify_owner(interaction.client, title="Unlinked User Entered Giveaway", description=f"User {interaction.user.name} attempted to enter a giveaway without linking their account.", color=discord.Color.red())
            return
        
        if await db.user_entered_giveaway(giveaway_id=current_giveaway['giveaway_id'], discord_id=interaction.user.id):
            embed = discord.Embed(
                title="❌ You already entered this giveaway!",
                description="You can only enter a giveaway once."
            )
            
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            await notify_owner(interaction.client, title="User Entered Giveaway Twice", description=f"User {interaction.user.name} attempted to enter a giveaway twice.", color=discord.Color.red())
            return
        
        user_entries = 1
        entry_message = f"You have entered the **{current_giveaway['name']}** giveaway! 🎉"
        
        if await db.user_is_subscribed(discord_id=interaction.user.id):
            user_entries += 1
            entry_message += "\n\n*You have been given an extra entry for being a subscriber!* 🎉"
            
        if interaction.user.premium_since:
            user_entries += 1
            entry_message += "\n\n*You have been given an extra entry for boosting the server!* 🎉"
        
        await db.enter_giveaway(interaction.user.name, interaction.user.id, user_entries, current_giveaway['giveaway_id'])
        
        embed = discord.Embed(
            title="✅ You entered the giveaway!",
            description=entry_message
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        await notify_owner(client=interaction.client, title = f"{interaction.user.name} Entered Giveaway", description=f"User {interaction.user.name} entered the {current_giveaway['name']} giveaway.\n\nMessage: {entry_message}", color=discord.Color.green())
        
        embed = interaction.message.embeds[0]
        
        embed.set_field_at(
            index=0,
            name="🎫 Entries",
            value=await db.number_of_entries(current_giveaway['giveaway_id']),
            inline=True
        )
        
        await interaction.message.edit(embed=embed, view=self)
        

@commands.has_role("SOSA")
@commands.hybrid_command(name="giveaway", description='Giveaway controls.')
async def giveaway(ctx, action: str, title: str, description: str, image_url: str, number_of_winners: Optional[int] = 1):
    if action == "create":
        embed = discord.Embed(
            title=f"🎉 Giveaway: {title}",
            description=description,
            color=discord.Color.pink()
        )
        
        embed.set_thumbnail(url=image_url)
        
        embed.add_field(
            name="🎫 Entries",
            value=0,
            inline=True
        )
        
        embed.set_footer(text=f"💫 Kick Subscribers and Server Boosters get an extra entry for each!")
        
        view = GiveawayView()
        
        channel = ctx.guild.get_channel(GIVEAWAY_CHANNEL_ID)
        
        if channel:
            await db.create_giveaway(title, description, number_of_winners)
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
