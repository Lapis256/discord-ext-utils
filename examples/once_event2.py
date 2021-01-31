from discord.ext import commands, utils


# utils.OnceEvent etc. must be written before commands.Bot.
class OnceEventBot(utils.OnceEvent, commands.Bot):
    async def once_ready(self):
        pass
        # It will be executed only once.

    async def on_ready(self):
        pass
        # It will be executed many times.


bot = OnceEventBot(command_prefix=commands.when_mentioned)


bot.run("TOKEN")
