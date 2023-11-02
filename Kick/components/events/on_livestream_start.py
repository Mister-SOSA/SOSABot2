from utils.bot_instance import client
import aiohttp
from common.utils.configutil import fetch_convar
import re
import os

DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
LIVESTREAM_ANNOUNCEMENTS_CHANNEL_ID = fetch_convar(
    "LIVESTREAM_ANNOUNCEMENTS_CHANNEL_ID")


@client.event
async def on_livestream_start():
    streamer_user = await client.fetch_user('HunchoSOSA')
    stream_title = re.sub(r'[^a-zA-Z ]+', '',
                          streamer_user.livestream.title).strip()

    url = f"https://discord.com/api/v10/channels/{LIVESTREAM_ANNOUNCEMENTS_CHANNEL_ID}/messages"

    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "User-Agent": "Bot",
        "Content-Type": "application/json",
    }

    embed = {
        "title": f"🟢 LIVE NOW | {stream_title}",
        "description": f"{streamer_user.livestream.categories[0].name}",
        "color": 0x00ff00,
        "image": {
            "url": f"{streamer_user.livestream.thumbnail}"
        },
        "thumbnail": {
            "url": f"{streamer_user.avatar}"
        }

    }

    button = {
        "type": 1,
        "components": [
            {
                "type": 2,
                "label": "Visit",
                "style": 5,
                "url": f"https://kick.com/{streamer_user.username}"
            }
        ]
    }

    data = {
        "embeds": [embed],
        "components": [button]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            print(f"Response: {response.status}")
            print(await response.text())
