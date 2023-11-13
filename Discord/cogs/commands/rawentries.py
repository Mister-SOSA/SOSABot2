from discord.ext import commands
from common.utils import database_manager as db

@commands.has_any_role("SOSA", "Admin")
@commands.hybrid_command(name="rawentries", description='Fetches raw entries from the database.')
async def rawentries(ctx, given_id: int):
    entries = await db.fetch_raw_entries(given_id)
    await ctx.send('\n'.join(entries) if entries else 'No entries found.')


async def setup(client):
    client.add_command(rawentries)
