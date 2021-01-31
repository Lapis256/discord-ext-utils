from discord.ext.commands import (
    Bot as _Bot,
    AutoShardedBot as _AutoShardedBot
)

from .once_event import OnceEvent


__all__ = ("Bot", "AutoShardedBot")


class BotBase(OnceEvent):
    pass


class Bot(BotBase, _Bot):
    pass


class AutoShardedBot(BotBase, _AutoShardedBot):
    pass
