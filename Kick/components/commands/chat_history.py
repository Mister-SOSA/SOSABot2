from objects.command import Command
from common.utils.database_manager import fetch_last_x_chat_messages

async def run(client, msg, args):
    if len(args) < 2:
        await msg.chatroom.send("Usage: !last <number> <user_id/username>")
        return
    
    try:
        number = int(args[0])
    except ValueError:
        await msg.chatroom.send("Usage: !last <number> <user_id/username>")
        return
    
    if number < 1:
        await msg.chatroom.send("Invalid number.")
        return

    messages = await fetch_last_x_chat_messages(number, author_id=args[1])
    
    if not messages:
        messages = await fetch_last_x_chat_messages(number, author=args[1])
    
    if not messages:
        await msg.chatroom.send("No messages found.")
        return
    
    messages = [f"[🗨️ {msg['content']}]" for msg in messages]
    
    chunks = []
    current_chunk = ""  # We'll add the prefix later, after knowing the total number of chunks

    for msg_str in messages:
        # If adding the next message would exceed the max length, start a new chunk
        if len(current_chunk + msg_str) > 200:
            chunks.append(current_chunk)
            current_chunk = ""

        current_chunk += msg_str + ' '

    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)

    total_chunks = len(chunks)

    for index, chunk in enumerate(chunks, start=1):
        prefix = f"Last {number} messages from [{args[1]}] ({index}/{total_chunks}): "
        final_msg = prefix + chunk
        await msg.chatroom.send(final_msg)
    
COMMAND = Command(
    func = run,
    name = "Chat History",
    description = "See the last X chat messages from a user.",
    emoji = "🕑",
    aliases = ["ch", "last"],
    usage = "!last <number> <user_id/username>",
    permission_level = 1,
    cooldown = 0,
    cost = 0,
    category = "MODERATION",
    enabled = True
)