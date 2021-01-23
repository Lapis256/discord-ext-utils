from discord.ext import utils


bot = utils.Bot(command_prefix=".")


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
