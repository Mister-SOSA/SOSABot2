import discord
from discord.ext import commands
import os
from rich import print
import asyncio
import sys
import logging

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from cogs.commands.giveaway import GiveawayView

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.ERROR)

intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', intents=intents)

for filename in os.listdir('./cogs/commands'):
    if filename.endswith('.py') and not filename.startswith('_'):
        asyncio.run(client.load_extension(f'cogs.commands.{filename[:-3]}'))
        print(f'[green]>> Loaded Command: {filename[:-3]}[/green]')


for filename in os.listdir('./cogs/listeners'):
    if filename.endswith('.py') and not filename.startswith('_'):
        asyncio.run(client.load_extension(f'cogs.listeners.{filename[:-3]}'))
        print(f'[blue]>> Loaded Listener: {filename[:-3]}[/blue]')


for filename in os.listdir('./cogs/tasks'):
    if filename.endswith('.py') and not filename.startswith('_'):
        asyncio.run(client.load_extension(f'cogs.tasks.{filename[:-3]}'))
        print(f'[yellow]>> Loaded Task: {filename[:-3]}[/yellow]')



@client.event
async def on_ready():
    await client.tree.sync()
    client.add_view(GiveawayView())
    print(f'[green]>> Logged in as {client.user}[/green]')

client.run(os.environ.get("DISCORD_BOT_TOKEN"))
