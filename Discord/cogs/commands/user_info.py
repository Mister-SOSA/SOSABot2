from discord.ext import commands
from common.utils import database_manager as db
import discord

@commands.has_any_role("SOSA", "Admin", "Moderator")
@commands.hybrid_command(name="userinfo", description='Look up a user\'s information.', aliases=["info", "lookup"])
async def user_info(ctx, query: str):
    fetch_args = [
        {"kick_id": query},
        {"strict": False, "kick_username": query},
        {"strict": False, "discord_username": query},
        {"strict": False, "discord_id": query}
    ]

    user = None
    for args in fetch_args:
        user = await db.fetch_user(**args)
        if user:
            break

    if not user:
        await ctx.send("User not found.")
        return

    embed = discord.Embed(
        title = "🔎 User Info",
        description = f""
    )
    
    embed.add_field(
        name="<:kick:1171189813060313140> Kick Username",
        value=f"{user['kick_username']}",
        inline=True
    )
    
    embed.add_field(
        name="<:kick:1171189813060313140> Kick ID",
        value=f"{user['kick_id']}",
        inline=False
    )
    
    embed.add_field(
        name="<:discord:1171190447834681374> Discord Username",
        value=f"{user['discord_username']}",
        inline=True
    )
    
    embed.add_field(
        name="<:discord:1171190447834681374> Discord ID",
        value=f"{user['discord_id']}",
        inline=False
    )
    
    embed.add_field(
        name="🪙 Coin Balance",
        value=f"{user['coin_balance']}",
        inline=False
    )
    
    embed.add_field(
        name="⚖️ Permission Level",
        value=f"{user['permission_level']}",
        inline=False
    )
    
    embed.add_field(
        name="👥 Aliases",
        value=f"{user['aliases']}",
        inline=False
    )
    
    embed.add_field(
        name="💬 Chat Messages",
        value=f"{await db.fetch_number_of_chat_messages(author_id=user['kick_id'])}",
        inline=False
    )
    
    embed.set_footer(
        text=f"Requested by {ctx.author.name}",
        icon_url=ctx.author.avatar
    )
    
    await ctx.send(embed=embed)

async def setup(client):
    client.add_command(user_info)
