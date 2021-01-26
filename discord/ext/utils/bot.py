from discord.ext.commands import (
    Bot as _Bot,
    AutoShardedBot as _AutoShardedBot
)

from .once_event import OnceEvent
# from .help_slash_command import HelpSlashCommand


__all__ = ("Bot", "AutoShardedBot")


"""
class BotBase(OnceEvent, HelpSlashCommand):
    def __init__(self, *args, **kwargs):
        kwargs["register_help_slash_command"] = kwargs.get("register_help_slash_command", False)
        
        super().__init__(*args, **kwargs)
"""

class BotBase(OnceEvent):
    pass


class Bot(BotBase, _Bot):
    pass


class AutoShardedBot(BotBase, _AutoShardedBot):
    pass
