from objects.command import Command
from common.utils import database_manager as db

async def run(client, msg, args):
    if len(args) == 0:
        await msg.chatroom.send("Please specify a user ID or username.")
        return
    
    user = await db.fetch_user(kick_id=args[0]) 
    
    if not user:
        user = await db.fetch_user(strict=False, kick_username=args[0])
        
    if not user:
        await msg.chatroom.send("User not found.")
        return
    
    number_of_messages = await db.fetch_number_of_chat_messages(author_id=user['kick_id'])
    
    await msg.chatroom.send(f"🕵️‍♂️ {user['kick_username']} | 🔢 {user['kick_id']} | 🪙 {user['coin_balance']} | ⚖️ {user['permission_level']} | 👥 {user['aliases']} | 💬 {number_of_messages}")
    
COMMAND = Command(
    func = run,
    name = "User Info",
    description = "Information about a user.",
    emoji = "🕵️‍♂️",
    aliases = ["info", "user"],
    usage = "!info <user_id/username>",
    permission_level = 4,
    cooldown = 0,
    cost = 0,
    category = "MODERATION",
    enabled = True
)