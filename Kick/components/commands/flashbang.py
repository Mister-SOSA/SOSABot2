from objects.command import Command
import aiohttp
from common.utils.configutil import fetch_constant

# Constants for better clarity
FLASHBANG_ENDPOINT = fetch_constant("FLASHBANG_ENDPOINT_URL")
TIMEOUT_DURATION = 10  # for example, you can adjust

# Helper functions to make the main function clearer
async def notify_flashbang_throw(msg, author_username):
    await msg.chatroom.send(f"@{author_username} threw a flashbang!")

async def notify_flashbang_failure(msg, author_username):
    await msg.chatroom.send(f"@{author_username} failed to throw a flashbang because something is broken...")

async def run(client, msg, args):
    author = await msg.author.to_user()

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TIMEOUT_DURATION)) as session:
            async with session.get(FLASHBANG_ENDPOINT) as resp:
                if resp.status == 200:
                    await notify_flashbang_throw(msg, author.username)
                else:
                    await notify_flashbang_failure(msg, author.username)
    except aiohttp.ClientError as e:  # Catching possible exceptions like timeouts, DNS failures, etc.
        print(f"Error occurred when trying to connect to {FLASHBANG_ENDPOINT}. Error: {e}")
        await notify_flashbang_failure(msg, author.username)

    
    
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