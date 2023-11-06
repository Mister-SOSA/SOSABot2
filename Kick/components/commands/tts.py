from objects.command import Command
import requests

async def run(client, msg, args):
    if len(args) == 0:
        await msg.chatroom.send("Please specify a message.")
        return
    
    await msg.chatroom.send()
    
COMMAND = Command(
    func = run,
    name = "Text-to-Speech",
    description = "Send a text-to-speech message.",
    emoji = "🔊",
    aliases = ["tts"],
    usage = "!tts <message>",
    permission_level = 1,
    cooldown = 5,
    cost = 15,
    category = "FUN",
    enabled = False
)