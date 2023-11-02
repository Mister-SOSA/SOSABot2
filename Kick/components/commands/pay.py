from objects.command import Command
from common.utils.database_manager import fetch_user_balance, adjust_user_balance, user_exists
from common.objects.user import User

async def run(client, msg, args):
    author = await msg.author.to_user()
    sender_balance = await fetch_user_balance(kick_id=msg.author.id)
    if len(args) < 2:
        await msg.chatroom.send(f"@{author.username} Usage: !pay <username> <amount>")
        return
    
    if not await user_exists(kick_username=args[0]):
        await msg.chatroom.send(f"@{author.username} That user is not registered.")
        return

    try:
        amount = int(args[1])
    except ValueError:
        await msg.chatroom.send(f"@{author.username} Usage: !pay <username> <amount>")
        return
    
    if amount < 1:
        await msg.chatroom.send(f"@{author.username} Invalid amount.")
        return
    
    if amount > sender_balance:
        await msg.chatroom.send(f"@{author.username} You don't have enough coins to make this payment.")
        return
    
    await adjust_user_balance(amount=-amount, kick_id=msg.author.id)
    await adjust_user_balance(amount=amount, kick_username=args[0])
    
    await msg.chatroom.send(f"@{author.username} You paid {args[0]} {amount} coins.")
    
COMMAND = Command(
    func = run,
    name = "Pay",
    description = "Pay another user some coins.",
    emoji = "💸",
    aliases = [],
    usage = "!pay <username> <amount>",
    permission_level = 1,
    cooldown = 5,
    cost = 0,
    category = "ECONOMY",
    enabled = True
)