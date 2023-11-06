from discord.ext import commands
import discord
from common.utils.configutil import fetch_convar

GIVEAWAY_CHANNEL_ID = fetch_convar("GIVEAWAY_CHANNEL_ID")

@commands.hybrid_command(name="giveaway", description='Giveaway controls.')
async def giveaway(ctx, action: str = commands.parameter(description="The action to perform. Valid actions are `create`, and `end`"), title = commands.parameter(description="The title of the giveaway."), description = commands.parameter(description="The description of the giveaway."), winners = commands.parameter(description="The number of winners for the giveaway."), image_url = commands.parameter(description="The image URL for the giveaway.")):
    if action == "create":
        embed = discord.Embed(
            title = f"🎉 {title}",
            description = f"{description}"
        )
        
        embed.set_image(url=image_url)
        
        embed.add_field(
            name="🎫 Winners",
            value=f"{winners}",
            inline=True
        )
        
        embed.add_field(
            name="👥 Host",
            value=f"{ctx.author.mention}",
            inline=True
        )
        
        class GiveawayButton(discord.ui.Button):
            def __init__(self):
                super().__init__(style=discord.ButtonStyle.green, label="Enter Giveaway")
            
            async def callback(self, interaction: discord.Interaction):
                await interaction.response.send_message("You have entered the giveaway!", ephemeral=True)
                
        class GiveawayView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(GiveawayButton())
                
        view = GiveawayView()
        
        channel = ctx.guild.get_channel(GIVEAWAY_CHANNEL_ID)
        message = await channel.send(embed=embed, view=view)
        
        
async def setup(client):
    client.add_command(giveaway)
        
        
        
