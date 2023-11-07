import asyncio
from discord.ext import commands
import random
import common.utils.database_manager as db
import discord

@commands.hybrid_command(name="link", description='Manually link your Discord with your Kick.')
async def link(ctx):
    if await db.already_linked(discord_id=ctx.author.id):
        await ctx.send("This Discord account is already linked to a Kick account.", ephemeral=True)
        return
    
    
    if await db.link_in_progress(ctx.author.id):
        await ctx.send("You already have a link in progress.", ephemeral=True)
        return
    
    
    code = random.randint(100000, 999999)
    
    await db.start_link(ctx.author.name, ctx.author.id, code, 300)
    
    embed = discord.Embed(
        title = "🔗 Link Accounts",
        description = f"""
        To link your Discord account with your Kick account, please follow these steps:
        
        1. Visit https://kick.com/HunchoSOSA/chatroom
        2. Enter the following command: `!link {code}`
        3. Your accounts will be linked and you can use your Kick bonuses on Discord!
        """
    )
    
    link_message = await ctx.send(embed=embed)
    
    await asyncio.sleep(5)
    
    if await db.link_in_progress(ctx.author.id):
        await db.expire_link(code)
        
        embed = discord.Embed(
            title = "🔗 Link Accounts",
            description = f"""
            Your link has expired. Please run `/link` in my Discord server to generate a new code.
            """
        )
        
        await link_message.edit(embed=embed)
        


async def setup(client):
    client.add_command(link)
