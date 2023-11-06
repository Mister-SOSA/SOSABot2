from discord.ext import commands
import discord


@commands.hybrid_command(name="purge", description='Delete messages in bulk.')
async def purge(ctx, amount: int):
    try:
        await ctx.defer()
        await ctx.channel.purge(limit=amount)
        
        embed = discord.Embed(
            title="✅ Success",
            description=f"{ctx.author.mention} purged {amount} messages.",
            color=discord.Color.green()
        )
        
        await ctx.channel.send(embed=embed, delete_after=5)
        
        
    except Exception as e:
        embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred while trying to purge messages: `{e}`",
            color=discord.Color.red()
        )
        
        await ctx.send(embed=embed)

async def setup(client):
    client.add_command(purge)
