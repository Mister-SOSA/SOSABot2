from discord.ext import commands


@commands.hybrid_command(name="test", description='A test command.')
async def test(ctx, param1: str, param2: int = 0):
    await ctx.send(f"param1: {param1}, param2: {param2}")


async def setup(client):
    client.add_command(test)
