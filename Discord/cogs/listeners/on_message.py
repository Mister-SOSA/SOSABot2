import discord
from discord.ext import commands
from common.utils.configutil import fetch_convar

BOT_ONLY_CHANNEL_IDS = fetch_convar("BOT_ONLY_CHANNEL_IDS")
OWNER_ID = fetch_convar("OWNER_ID")

class OnMessage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        
        if msg.channel.id in BOT_ONLY_CHANNEL_IDS and msg.author.id != OWNER_ID:
            await msg.delete()
            return
        
        
        
async def setup(client):
    await client.add_cog(OnMessage(client))