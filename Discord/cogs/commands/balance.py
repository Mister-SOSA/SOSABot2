from discord.ext import commands
import discord
from discord import app_commands
import common.utils.database_manager as db

@commands.hybrid_command(
    name="balance", 
    description='Check your coin balance.'
)
async def balance(ctx):
    if not await db.already_linked(discord_id=ctx.author.id):
        embed = discord.Embed(
            title="❌ Not Linked",
            description="You must link your Kick account to your Discord account to activate your coin balance. \
                \nLink your account by running `/link` in any channel.",
            color=discord.Color.red()
        )
        
        await ctx.send(embed=embed, ephemeral=True)
        return
    
    user_balance = await db.fetch_user_balance(discord_id=ctx.author.id)
    
    embed = discord.Embed(
        title = "💰 Coin Balance",
        description = f"You have **{user_balance}** coins."
    )
    
    await ctx.send(embed=embed, ephemeral=True)


async def setup(client):
    client.add_command(balance)
