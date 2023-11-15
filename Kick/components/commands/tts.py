from objects.command import Command
import os
import aiohttp

async def run(client, msg, args):
    if len(args) == 0:
        await msg.chatroom.send("Please specify a message.")
        return
    
    TTS_ENDPOINT = os.getenv("TTS_ENDPOINT")
    
    async with aiohttp.ClientSession() as session:
        async with session.post(TTS_ENDPOINT, json={"message": " ".join(args)}) as resp:
            if resp.status == 200:
                await msg.chatroom.send(f"🔊 {msg.author.mention} said: {await resp.text()}")
            else:
                await msg.chatroom.send(f"An error occurred while trying to send the message. ({resp.status})")
                
    
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
    enabled = False,
    stream_only = True
)