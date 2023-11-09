""" A utility for notifying the owner of the bot when an event occurs """

import discord

OWNER_DISCORD_ID = 268974144593461248

async def notify_owner(client, title=None, description=None, color=discord.Color.red(), **kwargs):
    """Notifies the owner of the bot when an event occurs.

    Args:
    - client (discord.Client): The client instance.
    - title (str): The title of the notification.
    - description (str): The description of the notification.
    - color (discord.Color): The color of the notification. Defaults to red.
    - **kwargs: Any fields to add to the notification.
    """
    
    owner = await client.fetch_user(OWNER_DISCORD_ID)
    
    if "embed" in kwargs:
        await owner.send(embed=kwargs["embed"])
        return
    
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    
    for key, value in kwargs.items():
        embed.add_field(name=key, value=value, inline=True)
        
    await owner.send(embed=embed)