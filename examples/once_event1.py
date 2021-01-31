from discord.ext import commands, utils


# utils.OnceEvent etc. must be written before commands.Bot.
class OnceEventBot(utils.OnceEvent, commands.Bot):
    pass


bot = OnceEventBot(command_prefix=commands.when_mentioned)


# Also available in Bot.listen and Cog.listener.
@bot.event
async def once_ready():
    pass
    # It will be executed only once.


@bot.event
async def on_ready():
    pass
    # It will be executed many times.


bot.run("TOKEN")
