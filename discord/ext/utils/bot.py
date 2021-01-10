from types import FunctionType, MethodType
import discord
from discord.ext.commands.bot import BotBase as _BotBase


class BotBase(_BotBase):
    def dispatch(self, event_name, *args, **kwargs):
        super().dispatch(event_name, *args, **kwargs)
        ev = 'once_' + event_name
        try:
            coro = getattr(self, ev)
        except AttributeError:
            pass
        else:
            if type(coro) is FunctionType:
                delattr(self, ev)
            elif type(coro) is MethodType:
                delattr(self.__class__, ev)
            
            self._schedule_event(coro, ev, *args, **kwargs) 

        for event in self.extra_events.pop(ev, []):
            self._schedule_event(event, ev, *args, **kwargs)

class Bot(BotBase, discord.Client):
    pass

class AutoShardedBot(BotBase, discord.AutoShardedClient):
    pass
