from utils.bot_instance import client
import sys
from utils.command_handler import load_commands
from threading import Thread
import random
import asyncio
import time


@client.event
async def on_ready():
    if "-t" in sys.argv:
        username = "SOSABot"
    else:
        username = "HunchoSOSA"

    user = await client.fetch_user(username)
    await user.chatroom.connect()

    print(f'Connected to {username}!')

    await load_commands()
