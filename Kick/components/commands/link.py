from objects.command import Command
from common.utils.database_manager import fetch_link, complete_link, link_expired, already_linked, link_used, fetch_user
from common.utils.configutil import fetch_convar
import os
import aiohttp

async def run(client, msg, args):
    author = await msg.author.to_user()
    
    if not args:
        await msg.chatroom.send(f"@{author.username} Run /link in my Discord server for instructions on how to link your accounts.")
        return
    
    if await already_linked(kick_id=author.id):
        await msg.chatroom.send(f"@{author.username} This Kick account is already linked to a Discord account.")
        return
    
    link = await fetch_link(args[0])
    
    if not link:
        await msg.chatroom.send(f"@{author.username} Invalid code.")
        return
    
    if await link_expired(args[0]):
        await msg.chatroom.send(f"@{author.username} This link has expired. Please run /link in my Discord server for a new code.")
        return
    
    if await link_used(args[0]):
        await msg.chatroom.send(f"@{author.username} This code has already been used. Please run /link in my Discord server for a link code.")
        return
    
    await complete_link(link["link_code"], author.id, kick_username=author.username)
    
    await assign_linked_role(link["discord_id"])
    
    await msg.chatroom.send(f"@{author.username} Your accounts have been linked.")


async def assign_linked_role(discord_id):
    role_id = fetch_convar("LINKED_ROLE_ID")
    guild_id = fetch_convar("GUILD_ID")

    url = f"https://discord.com/api/v10/guilds/{guild_id}/members/{discord_id}/roles/{role_id}"
    
    headers = {
        "Authorization": f"Bot {os.getenv('DISCORD_BOT_TOKEN')}",
        "User-Agent": "Bot",
        "Content-Type": "application/json"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers) as response:
            pass
            
            
COMMAND = Command(
    func=run,
    name="Link",
    description="Complete a link between your Kick and Discord accounts.",
    emoji="🔗",
    aliases=[],
    usage="!link <code>",
    permission_level=1,
    cooldown=0,
    cost=0,
    category="GENERAL",
    enabled=True,
    stream_only=False
)
