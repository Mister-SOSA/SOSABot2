from dataclasses import dataclass
from typing import Optional, Set, Union
from common.utils.configutil import fetch_convar
from common.utils.time_tool import get_timestamp
from common.utils.permission_manager import max_permission_level
from common.utils import database_manager as db


@dataclass
class User:
    created_at: Optional[str] = None
    kick_id: Optional[str] = None
    kick_username: Optional[str] = None
    discord_id: Optional[int] = None
    discord_username: Optional[str] = None
    is_staff: Optional[bool] = False
    is_owner: Optional[bool] = False
    is_mod: Optional[bool] = False
    is_subscribed: Optional[bool] = False
    following_since: Optional[str] = None
    coin_balance: Optional[int] = 0
    last_seen: Optional[str] = None
    permission_level: int = 1
    aliases: Optional[str] = None

    async def initialize(self, kick_message=None):

        if kick_message is not None:
            kick_user = await kick_message.author.to_user()
            kick_chatter = await kick_message.chatroom.fetch_chatter(kick_user.username)

            self.created_at = get_timestamp()
            self.kick_id = kick_user.id
            self.kick_username = kick_user.username
            self.is_staff = kick_chatter.is_staff
            self.is_owner = kick_chatter.is_owner
            self.is_subscribed = kick_chatter.subscribed_for > 0
            self.is_mod = kick_chatter.is_mod
            self.following_since = kick_chatter.following_since.strftime(
                "%Y-%m-%d %H:%M:%S") if kick_chatter.following_since else None
            self.coin_balance = fetch_convar("STARTING_COIN_BALANCE")
            self.last_seen = get_timestamp()
            self.aliases = None

            if self.is_owner:
                self.permission_level = max_permission_level()

            elif self.is_subscribed:
                self.permission_level = fetch_convar(
                    "SUBSCRIBER_PERMISSION_LEVEL")

            elif self.following_since:
                self.permission_level = fetch_convar(
                    "FOLLOWER_PERMISSION_LEVEL")

            else:
                self.permission_level = fetch_convar(
                    "DEFAULT_PERMISSION_LEVEL")

    async def update(self, kick_message=None):
            
            if kick_message is not None:
                kick_user = await kick_message.author.to_user()
                kick_chatter = await kick_message.chatroom.fetch_chatter(kick_user.username)
    
                self.last_seen = get_timestamp()
                self.kick_id = kick_user.id
                self.kick_username = kick_user.username
                self.is_staff = kick_chatter.is_staff
                self.is_owner = kick_chatter.is_owner
                self.is_subscribed = kick_chatter.subscribed_for > 0
                self.is_mod = kick_chatter.is_mod
                self.following_since = kick_chatter.following_since.strftime(
                    "%Y-%m-%d %H:%M:%S") if kick_chatter.following_since else None
                self.coin_balance = await db.fetch_user_balance(kick_id=kick_user.id)
                self.permission_level = await db.fetch_user_permission_level(kick_id=kick_user.id)
                self.aliases = None