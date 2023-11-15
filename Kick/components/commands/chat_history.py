from objects.command import Command
from common.utils.database_manager import fetch_last_x_chat_messages

async def send_usage_message(msg):
    await msg.chatroom.send("Usage: !last <number> <user_id/username>")

async def get_messages_by_author(number, author_key):
    messages = await fetch_last_x_chat_messages(number, author_id=author_key)
    if not messages:
        messages = await fetch_last_x_chat_messages(number, author=author_key)
    return messages

def split_messages_into_chunks(messages, max_length=200):
    chunks = []
    current_chunk = ""

    for msg_str in messages:
        if len(current_chunk + msg_str) > max_length:
            chunks.append(current_chunk)
            current_chunk = ""

        current_chunk += msg_str + ' '

    if current_chunk:
        chunks.append(current_chunk)
    return chunks

async def run(client, msg, args):
    if len(args) < 2:
        await send_usage_message(msg)
        return

    try:
        number = int(args[0])
        if number < 1:
            await msg.chatroom.send("Invalid number.")
            return
    except ValueError:
        await send_usage_message(msg)
        return

    messages = await get_messages_by_author(number, args[1])

    if not messages:
        await msg.chatroom.send("No messages found.")
        return

    messages = [f"[🗨️ {message['content']}]" for message in messages]
    chunks = split_messages_into_chunks(messages)

    for index, chunk in enumerate(chunks, start=1):
        prefix = f"Last {number} messages from [{args[1]}] ({index}/{len(chunks)}): "
        final_msg = prefix + chunk
        await msg.chatroom.send(final_msg)

COMMAND = Command(
    func=run,
    name="Chat History",
    description="See the last X chat messages from a user.",
    emoji="🕑",
    aliases=["ch", "last"],
    usage="!last <number> <user_id/username>",
    permission_level=1,
    cooldown=0,
    cost=0,
    category="MODERATION",
    enabled=True,
    stream_only=False
)
