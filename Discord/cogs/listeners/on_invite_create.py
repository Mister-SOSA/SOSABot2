import discord
from discord.ext import commands
from common.utils.configutil import fetch_convar

MODLOG_CHANNEL_ID = fetch_convar("MODLOG_CHANNEL_ID")

class OnInviteCreate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        channel = self.client.get_channel(MODLOG_CHANNEL_ID)
        
        embed = discord.Embed(
            title="📨 Invite Created",
            description=f"Invite created by {invite.inviter.name}",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Invite URL", value=invite.url)
        embed.add_field(name="Invite Duration", value=f"{invite.max_age}")
        
        
        await channel.send(embed=embed)


async def setup(client):
    await client.add_cog(OnInviteCreate(client))