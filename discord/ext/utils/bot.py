from discord.ext.commands import (
    Bot as _Bot,
    AutoShardedBot as _AutoShardedBot
)

from .once_event import OnceEvent
from .command_suggest import AutoSuggestion


__all__ = ("Bot", "AutoShardedBot")


class BotBase(OnceEvent, AutoSuggestion):
    pass


class Bot(BotBase, _Bot):
    pass


class AutoShardedBot(BotBase, _AutoShardedBot):
    pass
