from dataclasses import dataclass, field
from typing import Optional
from common.utils.configutil import fetch_convar
from common.utils.time_tool import get_timestamp
from common.utils.permission_manager import max_permission_level
from common.utils import database_manager as db


@dataclass
class User:
    created_at: Optional[str] = field(default=None)
    kick_id: Optional[str] = field(default=None)
    kick_username: Optional[str] = field(default=None)
    discord_id: Optional[int] = field(default=None)
    discord_username: Optional[str] = field(default=None)
    is_staff: bool = field(default=False)
    is_owner: bool = field(default=False)
    is_mod: bool = field(default=False)
    is_subscribed: bool = field(default=False)
    following_since: Optional[str] = field(default=None)
    coin_balance: int = field(default=0)
    last_seen: Optional[str] = field(default=None)
    permission_level: int = field(default=1)
    aliases: Optional[str] = field(default=None)

    async def _populate_attributes_from_kick_message(self, kick_message):
        """Private helper method to populate user attributes from a kick message."""
        kick_user = await kick_message.author.to_user()
        kick_chatter = await kick_message.chatroom.fetch_chatter(kick_user.username)

        self.last_seen = get_timestamp()
        self.kick_id = kick_user.id
        self.kick_username = kick_user.username
        self.is_staff = kick_chatter.is_staff
        self.is_owner = kick_chatter.is_owner
        self.is_mod = kick_chatter.is_mod
        self.is_subscribed = kick_chatter.subscribed_for > 0
        self.following_since = (kick_chatter.following_since.strftime("%Y-%m-%d %H:%M:%S") 
                                if kick_chatter.following_since else None)

    async def _set_permission_level(self):
        """Private helper method to set user's permission level based on their status."""
        if self.is_owner:
            self.permission_level = max_permission_level()
        elif self.is_subscribed:
            self.permission_level = fetch_convar("SUBSCRIBER_PERMISSION_LEVEL")
        elif self.following_since:
            self.permission_level = fetch_convar("FOLLOWER_PERMISSION_LEVEL")
        else:
            self.permission_level = fetch_convar("DEFAULT_PERMISSION_LEVEL")

    async def initialize(self, kick_message=None):
        """
        Initializes a user instance with attributes from a kick message.

        Args:
        - kick_message (Optional): The kick message to initialize the user from. Defaults to None.
        """
        if kick_message:
            await self._populate_attributes_from_kick_message(kick_message)
            self.created_at = get_timestamp()
            self.coin_balance = fetch_convar("STARTING_COIN_BALANCE")
            self.aliases = None
            await self._set_permission_level()

    async def update(self, kick_message=None):
        """
        Updates user attributes based on the provided kick message.

        Args:
        - kick_message (Optional): The kick message to update the user from. Defaults to None.
        """
        if kick_message:
            await self._populate_attributes_from_kick_message(kick_message)
            self.coin_balance = await db.fetch_user_balance(kick_id=self.kick_id)
            self.permission_level = await db.fetch_user_permission_level(kick_id=self.kick_id)
            self.aliases = None
