import discord
from discord.ext import commands
from common.utils.configutil import fetch_convar

MODLOG_CHANNEL_ID = fetch_convar("MODLOG_CHANNEL_ID")

class OnMemberRemove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(MODLOG_CHANNEL_ID)
        
        async for log in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if log.target.id == member.id:
                embed = discord.Embed(
                    title="👢 User Kicked",
                    description=f"User kicked: {member.name}\nKicked by: {log.user.mention}",
                    color=discord.Color.red()
                )
                
                await channel.send(embed=embed)
                return
        
        embed = discord.Embed(
            title="👋 User Left",
            description=f"User left: {member.name}",
            color=discord.Color.red()
        )
        
        await channel.send(embed=embed)
        
        
async def setup(client):
    await client.add_cog(OnMemberRemove(client))