from discord.ext import commands
import discord
import requests

@commands.has_role("Admin")
@commands.hybrid_command(
    name="avatar", 
    description='Change the avatar of the bot.'
)
@discord.app_commands.describe(
    image_url="The URL of the image to use as the avatar."
)
async def avatar(ctx, image_url: str):
    try:
        img = requests.get(image_url)

        await ctx.bot.user.edit(avatar=img.content)

        embed = discord.Embed(
            title="Bot avatar changed!",
            description=f"SOSABot\'s avatar was changed by {ctx.author.mention}.",
            color=discord.Color.green()
        )

        embed.set_thumbnail(url=image_url)

        await ctx.reply(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title="Error!",
            description=f"An error occurred while changing the avatar: ```{e}```",
            color=discord.Color.red()
        )

        await ctx.reply(embed=embed)


async def setup(client):
    client.add_command(avatar)
