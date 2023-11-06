import discord
from discord.ext import commands
from common.utils.configutil import fetch_convar

OWNER_ID = fetch_convar("OWNER_ID")

class OnMessage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        
        
        
async def setup(client):
    await client.add_cog(OnMessage(client))