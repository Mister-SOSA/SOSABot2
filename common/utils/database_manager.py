import datetime
from supabase import create_client, Client
from common.utils.configutil import fetch_constant
from common.objects.user import User
from common.utils.time_tool import get_timestamp
import os

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

USERS_TABLE = fetch_constant("USERS_TABLE")
CHAT_TABLE = fetch_constant("CHAT_TABLE")

client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def fetch_user_by_id(kick_id=None, discord_id=None, kick_username=None, discord_username=None):
    if kick_id is not None:
        return client.table(USERS_TABLE).select("*").eq("kick_id", kick_id).execute().data[0]
    elif discord_id is not None:
        return client.table(USERS_TABLE).select("*").eq("discord_id", discord_id).execute().data[0]
    elif kick_username is not None:
        return client.table(USERS_TABLE).select("*").eq("kick_username", kick_username).execute().data[0]
    elif discord_username is not None:
        return client.table(USERS_TABLE).select("*").eq("discord_username", discord_username).execute().data[0]
    else:
        return None


async def fetch_user_balance(kick_id=None, discord_id=None, kick_username=None, discord_username=None):
    user = await fetch_user_by_id(kick_id, discord_id, kick_username, discord_username)
    return user["coin_balance"]


async def adjust_user_balance(amount: int, kick_id=None, discord_id=None, kick_username=None, discord_username=None):
    current_balance = await fetch_user_balance(kick_id, discord_id, kick_username, discord_username)
    if kick_id:
        client.table(USERS_TABLE).update({"coin_balance": current_balance + amount}).eq("kick_id", kick_id).execute()
    elif discord_id:
        client.table(USERS_TABLE).update({"coin_balance": current_balance + amount}).eq("discord_id", discord_id).execute()
    elif kick_username:
        client.table(USERS_TABLE).update({"coin_balance": current_balance + amount}).eq("kick_username", kick_username).execute()
    elif discord_username:  
        client.table(USERS_TABLE).update({"coin_balance": current_balance + amount}).eq("discord_username", discord_username).execute()
        
        
async def fetch_user_permission_level(kick_id=None, discord_id=None):
    user = await fetch_user_by_id(kick_id, discord_id)
    return user["permission_level"] if user["permission_level"] is not None else 0


async def create_user(user: User):
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


async def user_exists(user: User):
    if user.kick_id:
        if client.table(USERS_TABLE).select("*").eq("kick_id", user.kick_id).execute().data:
            return True
    if user.discord_id:
        if client.table(USERS_TABLE).select("*").eq("discord_id", user.discord_id).execute().data:
            return True
    if user.kick_username:
        if client.table(USERS_TABLE).select("*").eq("kick_username", user.kick_username).execute().data:
            return True
    if user.discord_username:
        if client.table(USERS_TABLE).select("*").eq("discord_username", user.discord_username).execute().data:
            return True
    return False


async def update_user(user: User):
    if await user_exists(user):
        aliases = []
        fetched_user = await fetch_user_by_id(user.kick_id)
        if fetched_user['kick_username'] != user.kick_username:
            aliases = await fetch_user_by_id(user.kick_id).aliases
            if aliases is None:
                aliases = []
            aliases.append(user.kick_username)

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
            "aliases": aliases
        }

        if user.kick_id:
            condition_field = "kick_id"
            condition_value = user.kick_id
        elif user.discord_id:
            condition_field = "discord_id"
            condition_value = user.discord_id
        else:
            return False

        client.table(USERS_TABLE).update(update_payload).eq(
            condition_field, condition_value).execute()
        

async def log_chat_message(msg):
    author = await msg.author.to_user()
    payload = {
        'sent_at': get_timestamp(),
        'epoch' : datetime.datetime.strptime(get_timestamp(), '%Y-%m-%d %H:%M:%S').timestamp(),
        'author': author.username,
        'author_id': author.id,
        'content': msg.content,
        'message_id': msg.id,
    }
    
    client.table(CHAT_TABLE).insert(payload).execute()