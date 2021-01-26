import itertools

import discord
from discord.utils import maybe_coroutine
from discord.ext.tasks import Loop


class PresenceTask:
    def __init__(self, bot, interval=10, *, presences=None, activity=discord.Game, activity_kwargs=None):
        self._activity = activity
        self._kwargs = activity_kwargs or {}
        self.bot = bot

        items = self.__class__.__dict__.items()
        _presences = [v for k, v in items if not k.startswith("_")]
        str_presences = presences or []
        self._iter = itertools.cycle([*str_presences, *_presences])

        self._task = Loop(self._loop, interval, 0, 0, None, True, None)
        self._task.before_loop(self._wait_until_ready)

    async def _loop(self):
        presence = next(self._iter)
        if type(presence) is not str:
            presence = await maybe_coroutine(presence, self.bot)

        if isinstance(presence, discord.BaseActivity):
            activity = presence
        else:
            activity = self._activity(**self._kwargs, name=str(presence))

        await self.bot.change_presence(activity=activity)

    async def _wait_until_ready(self):
        await self.bot.wait_until_ready()

    def start(self):
        return self._task.start()

    def cancel(self):
        self._task.cancel()
