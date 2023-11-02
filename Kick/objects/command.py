from dataclasses import dataclass, field


@dataclass
class Command:
    func: callable
    name: str
    description: str
    emoji: str = None
    aliases: list = field(default_factory=list)
    usage: str = ""
    permission_level: int = 0
    cooldown: int = 0
    cost: int = 0
    category: str = "GENERAL"
    enabled: bool = True

    def execute(self, *args, **kwargs):
        return self.func(*args, **kwargs)
