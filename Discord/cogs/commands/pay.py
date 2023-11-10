from discord.ext import commands
from common.utils import database_manager as db
import discord

@commands.hybrid_command(
    name="pay", 
    description='Pay another user some coins.',
    help='Pay another user some coins.',
    usage='!pay <username> <amount>',
    aliases=[],
    brief='Pay another user some coins.'
)
@discord.app_commands.describe(
    amount="The amount of coins to pay.",
    user="The user to pay."
)
async def pay(ctx, amount: discord.app_commands.Range[int, 1, None], user: discord.User):
    
    sender_balance = await db.fetch_user_balance(discord_id=ctx.author.id)

    if amount > sender_balance:
        await ctx.send("You don't have enough coins to make this payment.")
        return

    await db.adjust_user_balance(amount=-amount, kick_id=ctx.author.id)
    await db.adjust_user_balance(amount=amount, kick_id=user.id)

    embed = discord.Embed(
        title=f"💸 Payment",
        description=f"{ctx.author.mention} paid {user.mention} {amount} coins.",
        color=discord.Color.green()
    )
    
    await ctx.send(embed=embed)


async def setup(client):
    client.add_command(pay)
