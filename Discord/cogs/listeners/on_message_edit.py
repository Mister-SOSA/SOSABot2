import discord
from discord.ext import commands
from common.utils.configutil import fetch_convar

MODLOG_CHANNEL_ID = fetch_convar("MODLOG_CHANNEL_ID")

class OnMessageEdit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel = self.client.get_channel(MODLOG_CHANNEL_ID)
        
        embed = discord.Embed(
            title="📝 Message Edited",
            description=f"Message edited in {before.channel.mention}",
            color=discord.Color.greyple()
        )
        
        embed.add_field(name="Message Author", value=before.author.mention)
        embed.add_field(name="Before", value=before.content)
        embed.add_field(name="After", value=after.content)
        
        await channel.send(embed=embed)
        
async def setup(client):
    await client.add_cog(OnMessageEdit(client))