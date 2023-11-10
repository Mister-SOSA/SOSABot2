import discord
from discord.ext import commands
from functools import wraps
from common.utils import database_manager as db

def check_linked():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            ctx = args[0]  # The context is the first argument in a command callback
            if not await db.already_linked(discord_id=ctx.author.id):
                embed = discord.Embed(
                    title="❌ Not Linked",
                    description="You must link your Kick account to your Discord account to use this command. \
                        \nLink your account by running `/link` in any channel.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed, ephemeral=True)
                return
            return await func(*args, **kwargs)
        return wrapper
    return decorator