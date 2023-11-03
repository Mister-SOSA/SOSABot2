import os
import importlib
from utils.bot_instance import client
import common.utils.database_manager as db
import common.utils.permission_manager as pm
from rich import print


class CommandManager:
    def __init__(self):
        self.commands = {}

    def _get_module(self, component_name):
        """Return the module for a given component name."""
        return importlib.import_module(f'components.commands.{component_name}')

    async def load(self):
        """Load all commands from the 'commands' directory."""
        for component in os.listdir('./components/commands'):
            if component.endswith('.py') and not component.startswith('_'):
                module = self._get_module(component[:-3])
                self.commands[module.COMMAND.name.lower()] = module.COMMAND
                print(
                    f'[cyan]>> Loaded Command: {module.COMMAND.name}[/cyan]')

    async def reload(self, command_name=None):
        """Reload a specific command or all commands if none is specified."""
        if command_name:
            if command_name in self.commands:
                module = self._get_module(command_name)
                self.commands[command_name] = module.COMMAND
        else:
            for command in self.commands:
                self.reload(command)

    async def parse(self, msg):
        """Parse a user's message to execute a command."""
        command = msg.content.split()[0][1:].lower()
        args = msg.content.split()[1:]

        for cmd_name, cmd_obj in self.commands.items():
            if command == cmd_obj.name.lower() or command in cmd_obj.aliases:
                if await CommandChecker.passes_checks(msg, cmd_obj):
                    await cmd_obj.execute(client, msg, args)
                    if cmd_obj.cost > 0:
                        await db.adjust_user_balance(kick_id=msg.author.id, amount=-cmd_obj.cost)
                return


class CommandChecker:
    @staticmethod
    async def passes_checks(msg, cmd_obj):
        """Check if the user has the required permissions and balance to execute a command."""
        user_perm = pm.fetch_permission(await db.fetch_user_permission_level(kick_id=msg.author.id))
        command_perm = pm.fetch_permission(cmd_obj.permission_level)
        author = await msg.author.to_user()

        if not cmd_obj.enabled:
            await msg.chatroom.send(f'@{author.username} This command is disabled.')
            return False

        if user_perm['level'] < command_perm['level']:
            await msg.chatroom.send(f"@{author.username} You don't have the required permission. Minimum required: {command_perm['emoji']} {command_perm['name']}.")
            return False

        if cmd_obj.cost > 0 and cmd_obj.cost > await db.fetch_user_balance(kick_id=msg.author.id):
            await msg.chatroom.send(f"@{author.username} Insufficient coins. You need {cmd_obj.cost} coins.")
            return False

        return True


cmd_mgr = CommandManager()
