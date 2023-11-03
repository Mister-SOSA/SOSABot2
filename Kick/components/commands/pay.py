from objects.command import Command
from common.utils.database_manager import fetch_user_balance, adjust_user_balance, user_exists

USAGE_MESSAGE = "Usage: !pay <username> <amount>"
INVALID_AMOUNT_MESSAGE = "Invalid amount."
NOT_ENOUGH_COINS_MESSAGE = "You don't have enough coins to make this payment."
USER_NOT_REGISTERED_MESSAGE = "That user is not registered."

async def validate_and_get_amount(username, args, author_username, msg_chatroom):
    if len(args) < 2:
        await msg_chatroom.send(f"@{author_username} {USAGE_MESSAGE}")
        return None

    if not await user_exists(kick_username=username):
        await msg_chatroom.send(f"@{author_username} {USER_NOT_REGISTERED_MESSAGE}")
        return None

    try:
        amount = int(args[1])
        if amount < 1:
            await msg_chatroom.send(f"@{author_username} {INVALID_AMOUNT_MESSAGE}")
            return None
        return amount
    except ValueError:
        await msg_chatroom.send(f"@{author_username} {USAGE_MESSAGE}")
        return None

async def run(client, msg, args):
    author = await msg.author.to_user()
    recipient_username = args[0]
    
    amount = await validate_and_get_amount(recipient_username, args, author.username, msg.chatroom)
    if amount is None:
        return
    
    sender_balance = await fetch_user_balance(kick_id=msg.author.id)

    if amount > sender_balance:
        await msg.chatroom.send(f"@{author.username} {NOT_ENOUGH_COINS_MESSAGE}")
        return

    await adjust_user_balance(amount=-amount, kick_id=msg.author.id)
    await adjust_user_balance(amount=amount, kick_username=recipient_username)

    await msg.chatroom.send(f"@{author.username} You paid {recipient_username} {amount} coins.")

COMMAND = Command(
    func=run,
    name="Pay",
    description="Pay another user some coins.",
    emoji="💸",
    aliases=[],
    usage=USAGE_MESSAGE,
    permission_level=1,
    cooldown=5,
    cost=0,
    category="ECONOMY",
    enabled=True
)
