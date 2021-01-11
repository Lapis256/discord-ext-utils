import asyncio
import itertools

import discord
from discord.utils import maybe_coroutine


class PresenceTask:
    def __init__(self, bot, delay=10, *, activity=discord.Game, **kwargs):
        presences = [attr for name in dir(self) if isinstance(attr := getattr(self, name, None), _Presence)]
        presences.sort(key=lambda p: p.number)
        
        self._iter = itertools.cycle(presences)
        self._task = None
        self._activity = activity
        self._kwargs = kwargs.get("activity_kwargs", {})
        
        self.delay = delay
        self.bot = bot

    async def _loop(self):
        while True:
            result = await maybe_coroutine(next(self._iter).func, self.bot)
            if result is None:
                continue
            elif isinstance(result, discord.BaseActivity):
                activity = result
            else:
                activity = self._activity(**self._kwargs, name=str(result))
            
            await self.bot.change_presence(activity=activity)
            await asyncio.sleep(self.delay)
    
    def start(self):
        if self._task is not None and not self._task.done():
            raise RuntimeError('Task is already launched and is not completed.')
        
        self._task = self.bot.loop.create_task(self._loop())
        return self._task
        
    def cancel(self):
        if self._task and not self._task.done():
            self._task.cancel()

class _Presence:
    number = 0
    
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        
        self.number = cls.number
        cls.number += 1
        
        return self 
        
    def __init__(self, func):
        self.func = func

def presence(func):
    return _Presence(func)
