""" A command which can reload a cog to allow for changes to be made without restarting the bot. """
from discord.ext import commands
import discord

@commands.hybrid_command(
    name="reload", 
    description='Reload a cog or the entire bot.'
)
async def cog_reload(ctx, cog: str = None):
    if cog is None:
        await reload_all(ctx)
        await ctx.send("Reloaded all cogs.")
        return
    
    try:
        ctx.bot.reload_extension(f"cogs.{cog}")
        
        embed = discord.Embed(
            title="🔄️ Reloaded",
            description=f"Reloaded cog `{cog}`.",
            color=discord.Color.green()
        )
        
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred while trying to reload the cog: \n`{e}`",
            color=discord.Color.red()
        )
        
        await ctx.send(embed=embed)
        

def reload_all(ctx):
    for cog in ctx.bot.cogs:
        ctx.bot.reload_extension(f"cogs.{cog}")

async def setup(client):
    client.add_command(cog_reload)
