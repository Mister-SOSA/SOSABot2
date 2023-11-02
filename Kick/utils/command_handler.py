import importlib
import os
from utils.bot_instance import client
import common.utils.database_manager as db
import common.utils.permission_manager as pm

commands = {}

async def load_commands():
    for component in os.listdir('./components/commands'):
        if component.endswith(".py") and not component.startswith("_"):
            cmd = importlib.import_module(f"components.commands.{component[:-3]}")
            commands[cmd.COMMAND.name.lower()] = cmd.COMMAND
            print(f"Loaded {component[:-3]}")
            
            
async def load_new_commands():
    for component in os.listdir('./components/commands'):
        if component.endswith(".py") and not component.startswith("_"):
            if not component[:-3] in commands:
                cmd = importlib.import_module(f"components.commands.{component[:-3]}")
                commands[cmd.COMMAND.name.lower()] = cmd.COMMAND
                print(f"Loaded {component[:-3]}")
                

async def reload_command(command_name):
    if not command_name in commands:
        return

    component = f"components.commands.{command_name}"
    importlib.reload(importlib.import_module(component))
    commands[command_name] = importlib.import_module(component).COMMAND
    print(f"Reloaded {component}")
    
    
async def reload_commands():
    for command in commands:
        await reload_command(command)
        
            
async def parse_command(msg):
    command = msg.content.split()[0][1:].lower()
    args = msg.content.split()[1:]
    
    for cmd, cmd_obj in commands.items():
        if command == cmd_obj.name.lower() or command in cmd_obj.aliases:
            if await passes_checks(msg, cmd_obj):
                await cmd_obj.execute(client, msg, args)
                if cmd_obj.cost > 0:
                    await db.adjust_user_balance(kick_id=msg.author.id, amount=-cmd_obj.cost)
            return
        
async def passes_checks(msg, cmd):
    user_perm = pm.fetch_permission(await db.fetch_user_permission_level(kick_id=msg.author.id))
    command_perm = pm.fetch_permission(cmd.permission_level)
    author = await msg.author.to_user()
    
    if user_perm['level'] >= pm.max_permission_level()['level']:
        return True
    
    if cmd.enabled == False:
        await msg.channel.send(f"@{author.username} This command is disabled.")
        return False
    
    if user_perm['level'] < command_perm['level']:
        await msg.chatroom.send(f"@{author.username} You do not have permission to use this command. You must be at least {command_perm['emoji']} {command_perm['name']}.")
        return False
    
    if cmd.cost > 0 and cmd.cost > await db.fetch_user_balance(kick_id=msg.author.id):
        print(await db.fetch_user_balance(kick_id=msg.author.id))
        await msg.chatroom.send(f"@{author.username} You do not have enough coins to use this command. You need {cmd.cost} coins.")
        return False
    
    return True
        