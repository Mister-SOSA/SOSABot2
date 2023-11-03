from objects.command import Command
from common.objects.slot_machine import SlotMachine
from common.utils import database_manager as db


async def run(client, msg, args):
    if len(args) == 0:
        await msg.chatroom.send("Please specify an amount to gamble.")
        return

    try:
        amount = int(args[0])
    except ValueError:
        await msg.chatroom.send(f"@{msg.author.username} Please specify a valid amount to gamble.")
        return

    if amount < 1:
        await msg.chatroom.send(f"@{msg.author.username} You must gamble at least 1 coin.")
        return

    user_balance = await db.fetch_user_balance(kick_id=msg.author.id)

    if amount > user_balance:
        await msg.chatroom.send(f"{msg.author.username} You are {amount - user_balance} coins short for this bet.")
        return

    slot_machine = SlotMachine()
    slots_results, breakdown, winnings = slot_machine.spin(amount)

    await db.adjust_user_balance(winnings, kick_id=msg.author.id)

    await msg.chatroom.send(f"[{' | '.join(slots_results)}] - [{breakdown}\n{'+' if winnings > 0 else ''}] | [{winnings} coins]")

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
    enabled=True
)
