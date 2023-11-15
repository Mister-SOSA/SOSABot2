from objects.command import Command
from common.utils.database_manager import fetch_user_balance


async def run(client, msg, args):
    author = await msg.author.to_user()
    await msg.chatroom.send(f"@{author.username} Your balance is {await fetch_user_balance(kick_id=msg.author.id)} coins.")

COMMAND = Command(
    func=run,
    name="Balance",
    description="Check your coin balance.",
    emoji="🏦",
    aliases=["bal"],
    usage="!balance",
    permission_level=1,
    cooldown=5,
    cost=0,
    category="ECONOMY",
    enabled=True,
    stream_only=False
)
