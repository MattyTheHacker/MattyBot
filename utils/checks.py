import asyncio
import enum
import inspect
from collections import ChainMap
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    ClassVar,
    Dict,
    List,
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

if TYPE_CHECKING:
    _CommandOrCoro = TypeVar("_CommandOrCoro", Callable[..., Awaitable[Any]])

import discord

from discord.ext.commands import check

class PrivilegeLevel(enum.IntEnum):
    NONE = enum.auto()
    MOD = enum.auto()
    ADMIN = enum.auto()
    GUILD_OWNER = enum.auto()
    BOT_OWNER = enum.auto()

class Requires:
    @staticmethod
    def get_decorator(privilege_level: Optional[PrivilegeLevel], user_perms: Optional[Dict[str, bool]]) -> Callable[['_CommandOrCoro'], '_CommandOrCoro']:
        if not user_perms:
            user_perms = None
        
        def decorator(func: "_CommandOrCoro") -> "_CommandOrCoro":
            if inspect.iscoroutinefunction(func):
                func.__requires_privilege_level__ = privilege_level
                func.__requires_user_perms__ = user_perms
            else:
                func.__requires_privilege_level__ = privilege_level
                if user_perms is None:
                    func.requires.user_perms = None
                else:
                    _validate_perms_dict(user_perms)
                    assert func.requires.user_perms is not None
                    func.requires.user_perms.update(user_perms)
            return func
        return decorator

def admin_or_permissions(**perms: bool):
    """
    Checks if the user has admin permissions or the correct permissions.
    """
    return Requires.get_decorator(PrivilegeLevel.ADMIN, perms)


def _validate_perms_dict(perms: Dict[str, bool]) -> None:
    invalid_keys = set(perms.keys()) - set(discord.Permissions.VALID_FLAGS)
    if invalid_keys:
        raise TypeError(f"Invalid permission keys: {invalid_keys}")
    for perm, value in perms.items():
        if value is not True:
            raise TypeError(f"Permission values must be True, not {value}. Use `perms.update({perm: True})` to set a permission to True.")