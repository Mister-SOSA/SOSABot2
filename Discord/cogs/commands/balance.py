from discord.ext import commands
import discord
from discord import app_commands
import common.utils.database_manager as db
from utils.custom_checks import check_linked

@commands.hybrid_command(
    name="balance", 
    description='Check your coin balance.'
)
@check_linked()
async def balance(ctx):    
    user_balance = await db.fetch_user_balance(discord_id=ctx.author.id)
    
    embed = discord.Embed(
        title = "🪙 Coin Balance",
        description = f"You have **{user_balance}** coins.",
        color=discord.Color.green()
    )
    
    await ctx.send(embed=embed, ephemeral=True)


async def setup(client):
    client.add_command(balance)
