from objects.command import Command
import common.utils.database_manager as db 
import json

async def run(client, msg, args):
    if len(args) == 0:
        await msg.chatroom.send("Please specify a user ID or username.")
        return
    
    user = await db.fetch_user(kick_id=args[0]) 
    
    if not user:
        user = await db.fetch_user(kick_username=args[0])
        
    if not user:
        await msg.chatroom.send("User not found.")
        return
    
    if user['aliases']:
        aliases = json.loads(user["aliases"])  
        await msg.chatroom.send(f"Aliases for {user['kick_username']}: {', '.join(aliases)}")
    
    else:
        await msg.chatroom.send(f"{user['kick_username']} has no aliases.")
    
COMMAND = Command(
    func = run,
    name = "Alias",
    description = "Check a user's aliases.",
    emoji = "👥",
    aliases = ["aliases"],
    usage = "!alias <user_id/username>",
    permission_level = 6,
    cooldown = 0,
    cost = 0,
    category = "MODERATION",
    enabled = True,
    stream_only = False
)