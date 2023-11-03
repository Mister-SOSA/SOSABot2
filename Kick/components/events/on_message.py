from utils.bot_instance import client
import common.utils.configutil as config
from utils.command_handler import cmd_mgr
from common.utils import database_manager as db
from common.objects.user import User

COMMAND_PREFIX = config.fetch_convar("KICK_BOT_COMMAND_PREFIX")


@client.event
async def on_message(msg):
    kick_user = await msg.author.to_user()
    user = User(kick_id=msg.author.id, kick_username=kick_user.username)

    if not await db.user_exists(kick_id=user.kick_id):
        await user.initialize(msg)
        await db.create_user(user)
    else:
        await user.update(msg)
        await db.update_user(user)

    await db.log_chat_message(msg)

    if not msg.content.startswith(COMMAND_PREFIX):
        await db.adjust_user_balance(1, kick_id=user.kick_id)
        return

    await cmd_mgr.parse(msg)
