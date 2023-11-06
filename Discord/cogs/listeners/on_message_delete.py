import discord
from discord.ext import commands
from common.utils.configutil import fetch_convar

MODLOG_CHANNEL_ID = fetch_convar("MODLOG_CHANNEL_ID")

class OnMessageDelete(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if msg.author.bot:
            return
        
        channel = self.client.get_channel(MODLOG_CHANNEL_ID)
        
        embed = discord.Embed(
            title="🗑️ Message Deleted",
            description=f"Message deleted in {msg.channel.mention}",
            color=discord.Color.red()
        )
        
        embed.add_field(name="Message Author", value=msg.author.mention)
        embed.add_field(name="Message Content", value=msg.content)
        
        await channel.send(embed=embed)

async def setup(client):
    await client.add_cog(OnMessageDelete(client))