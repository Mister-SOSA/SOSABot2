import datetime
import json
import os
from supabase import create_client, Client
from common.utils.configutil import fetch_constant
from common.objects.user import User
from common.utils.time_tool import get_timestamp

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

USERS_TABLE = fetch_constant("USERS_TABLE")
CHAT_TABLE = fetch_constant("CHAT_TABLE")

client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def fetch_user(strict=True, **kwargs):
    """Fetches a user based on the provided criteria."""
    for key, value in kwargs.items():
        if value:
            result = client.table(USERS_TABLE).select("*").eq(key, value) if strict else client.table(USERS_TABLE).select("*").ilike(key, value).execute().data
            if result:
                return result[0]
    return None


async def fetch_user_balance(**kwargs):
    """Fetches the coin balance of a user."""
    user = await fetch_user(**kwargs)
    return user["coin_balance"] if user else None


async def adjust_user_balance(amount: int, **kwargs):
    """Adjusts the coin balance of a user."""
    current_balance = await fetch_user_balance(**kwargs)
    for key, value in kwargs.items():
        if value:
            client.table(USERS_TABLE).update({"coin_balance": current_balance + amount}).eq(key, value).execute()
            break


async def fetch_user_permission_level(**kwargs):
    """Fetches the permission level of a user."""
    user = await fetch_user(**kwargs)
    return user["permission_level"] if user and "permission_level" in user else 0


async def create_user(user: User):
    """Creates a new user in the database."""
    client.table(USERS_TABLE).insert({
        "kick_id": user.kick_id,
        "kick_username": user.kick_username,
        "discord_id": user.discord_id,
        "discord_username": user.discord_username,
        "is_staff": user.is_staff,
        "is_owner": user.is_owner,
        "is_mod": user.is_mod,
        "is_subscribed": user.is_subscribed,
        "following_since": user.following_since,
        "coin_balance": user.coin_balance,
        "last_seen": user.last_seen,
        "permission_level": user.permission_level
    }).execute()


async def user_exists(**kwargs):
    """Checks if a user exists in the database."""
    user = await fetch_user(**kwargs)
    return bool(user)


async def update_user(user: User):
    """Updates an existing user in the database."""
    exists = await user_exists(kick_id=user.kick_id) or await user_exists(discord_id=user.discord_id)
    if not exists:
        return False
    condition_field, condition_value = _get_update_condition(user)
    aliases = await _get_updated_aliases(user)
    update_payload = {
        "kick_id": user.kick_id,
        "kick_username": user.kick_username,
        "discord_id": user.discord_id,
        "discord_username": user.discord_username,
        "is_staff": user.is_staff,
        "is_owner": user.is_owner,
        "is_subscribed": user.is_subscribed,
        "following_since": user.following_since,
        "coin_balance": user.coin_balance,
        "last_seen": user.last_seen,
        "permission_level": user.permission_level,
        "aliases": json.dumps(aliases) if aliases else None
    }
    if not condition_field or not condition_value:
        return False
    client.table(USERS_TABLE).update(update_payload).eq(condition_field, condition_value).execute()
    return True


def _get_update_condition(user: User):
    """Returns the field and value to be used as a condition for updating a user."""
    if user.kick_id:
        return "kick_id", user.kick_id
    elif user.discord_id:
        return "discord_id", user.discord_id
    return None, None


async def _get_updated_aliases(user: User):
    """Fetches and updates the username aliases for a user."""
    current_username = user.kick_username
    db_user = await fetch_user(kick_id=user.kick_id)
    db_username = db_user['kick_username']
    aliases = json.loads(db_user.get('aliases', '[]'))
    if current_username != db_username and db_username not in aliases:
        aliases.append(db_username)
    return aliases


async def log_chat_message(msg):
    """Logs a chat message in the database."""
    author = await msg.author.to_user()
    payload = {
        'sent_at': get_timestamp(),
        'epoch': datetime.datetime.strptime(get_timestamp(), '%Y-%m-%d %H:%M:%S').timestamp(),
        'author': author.username,
        'author_id': author.id,
        'content': msg.content,
        'message_id': msg.id,
    }
    client.table(CHAT_TABLE).insert(payload).execute()


async def fetch_last_x_chat_messages(x, **kwargs):
    """Fetches the last x chat messages based on the provided criteria."""
    for key, value in kwargs.items():
        if value:
            result, count = client.table(CHAT_TABLE).select("*").ilike(key, value).order('epoch', desc=True).limit(x).execute()
            if result[1]:
                return result[1]
    return None


async def fetch_number_of_chat_messages(**kwargs) -> int:
    """Fetches the number of chat messages based on the provided criteria."""
    for key, value in kwargs.items():
        if value:
            result = client.table(CHAT_TABLE).select("*").ilike(key, value).execute().data
            if result:
                return len(result)
    return 0
