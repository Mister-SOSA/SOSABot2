from objects.command import Command
import aiohttp
from common.utils.configutil import fetch_constant

async def run(client, msg, args):
    author = await msg.author.to_user()
    async with aiohttp.ClientSession() as session:
        async with session.get(fetch_constant("FLASHBANG_ENDPOINT_URL")) as resp:
            if resp.status == 200:
                await msg.chatroom.send(f"@{author.username} threw a flashbang!")
            else:
                await msg.chatroom.send(f"@{author.username} failed to throw a flashbang because something is broken...")
    
    
COMMAND = Command(
    func = run,
    name = "Flashbang",
    description = "Throw a flashbang that blinds me.",
    emoji = "💥",
    aliases = ["flash", "fb"],
    usage = "!flash",
    permission_level = 1,
    cooldown = 10,
    cost = 50,
    category = "FUN",
    enabled = True
)