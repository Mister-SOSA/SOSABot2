from objects.command import Command

# @dataclass
# class Command:
#     func: callable
#     name: str
#     description: str
#     emoji: str = None
#     aliases: list = field(default_factory=list)
#     usage: str = ""
#     permission_level: int = 0
#     cooldown: int = 0
#     cost: int = 0
#     category: str = "GENERAL"
#     enabled: bool = True

#     def execute(self, *args, **kwargs):
#         return self.func(*args, **kwargs)

async def run(client, msg, args):
    await msg.chatroom.send("Test command ran successfully!")
    
COMMAND = Command(
    func = run,
    name = "Test",
    description = "A test command.",
    emoji = "🤖",
    aliases = ["t"],
    usage = "!test",
    permission_level = 1,
    cooldown = 5,
    cost = 5,
    category = "GENERAL",
    enabled = True
)