from discord.ext import commands
from common.utils import database_manager as db
import discord
from datetime import datetime

@commands.has_any_role("SOSA", "Admin", "Moderator")
@commands.hybrid_command(
    name="chat_history", 
    description='View the last X messages from a user in Kick chat.'
)
@discord.app_commands.describe(
    query="The user to look up. Can be a Kick username, Discord username, Kick ID, or Discord ID.",
    limit="The number of messages to fetch."
)
async def chat_history(ctx, query: str, limit: int = 5):
    fetch_args = [
        {"kick_id": query},
        {"strict": False, "kick_username": query},
        {"strict": False, "discord_username": query},
        {"strict": False, "discord_id": query}
    ]
    
    if query.startswith("<@") and query.endswith(">"):
        query = query[2:-1]
        if query.startswith("!"):
            query = query[1:]
        fetch_args.append({"discord_id": query})

    user = None
    for args in fetch_args:
        user = await db.fetch_user(**args)
        if user:
            break

    if not user:
        await ctx.send("User not found.")
        return

    messages = await db.fetch_last_x_chat_messages(limit, author_id=user["kick_id"])
    if not messages:
        await ctx.send("No messages found.")
        return

    embed = discord.Embed(
        title = f"🔎 Chat History for {user['kick_username']}",
        description = f""
    )
    

    for message in messages:
        
        datetime_object = datetime.strptime(message['sent_at'], '%Y-%m-%dT%H:%M:%S%z')
        message['sent_at'] = datetime_object.strftime('%m/%d/%Y, %H:%M:%S')
        
        embed.add_field(
            name=f"💬 {message['author']} ({message['sent_at']})",
            value=f"{message['content']}",
            inline=False
        )
    
    await ctx.send(embed=embed) 


async def setup(client):
    client.add_command(chat_history)
