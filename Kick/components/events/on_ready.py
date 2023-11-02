from utils.bot_instance import client
import sys
from utils.command_handler import cmd_mgr
from rich import print


@client.event
async def on_ready():
    if "-t" in sys.argv:
        username = "SOSABot"
    else:
        username = "HunchoSOSA"

    user = await client.fetch_user(username)
    await user.chatroom.connect()

    print(f'[green]>> Connected to Chatroom: {username}[/green]')

    await cmd_mgr.load()
