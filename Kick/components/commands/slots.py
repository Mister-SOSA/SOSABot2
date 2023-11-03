from objects.command import Command
import random


async def run(client, msg, args):
    print('pass')

COMMAND = Command(
    func=run,
    name="Slots",
    description="Gamble your coins on a slot roll.",
    emoji="🎰",
    aliases=["slot"],
    usage="!slots <amount>",
    permission_level=1,
    cooldown=5,
    cost=0,
    category="ECONOMY",
    enabled=False
)
