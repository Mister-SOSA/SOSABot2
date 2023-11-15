from dataclasses import dataclass, field

@dataclass
class Command:
    """
    Represents a command with various metadata and execution functionality.
    
    Attributes:
        - func (callable): 
            The function to be executed when the command is called.
        - name (str): 
            The name of the command.
        - description (str): 
            A brief description of what the command does.
        - emoji (str, optional): 
            An associated emoji for the command. Default is None.
        - aliases (list, optional): 
            Alternative names/shortcuts for the command. Default is an empty list.
        - usage (str, optional): 
            How the command should be used, e.g. argument syntax. Default is an empty string.
        - permission_level (int, optional): 
            Required permission level to execute the command. Default is 0.
        - cooldown (int, optional): 
            Time (in seconds) the user has to wait before using the command again. Default is 0.
        - cost (int, optional): 
            Resource cost to execute the command, e.g. in-game currency. Default is 0.
        - category (str, optional): 
            The category under which the command falls, e.g. 'GENERAL'. Default is 'GENERAL'.
        - enabled (bool, optional): 
            Whether the command is currently enabled or not. Default is True.
        - stream_only (bool, optional):
            Whether the command can only be executed during a stream or not. Default is False.
    
    Methods:
        - execute(*args, **kwargs): 
            Executes the command's function with the given arguments and keyword arguments.
    """

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
    stream_only: bool = False

    def execute(self, *args, **kwargs):
        """Executes the command's function with the provided arguments and returns the result."""
        return self.func(*args, **kwargs)
