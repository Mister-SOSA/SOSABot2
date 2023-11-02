from objects.command import Command
from common.utils.configutil import fetch_convar

DISCORD_SERVER_URL = fetch_convar("DISCORD_SERVER_INVITE_URL")

async def run(client, msg, args):
    await msg.chatroom.send(f'Join my Discord server! {DISCORD_SERVER_URL}')
    
COMMAND = Command(
    func = run,
    name = "Discord",
    description = "Get the invite link to my Discord server.",
    emoji = "💬",
    aliases = ["d"],
    usage = "!discord",
    permission_level = 0,
    cooldown = 0,
    cost = 0,
    category = "GENERAL",
    enabled = True    
)