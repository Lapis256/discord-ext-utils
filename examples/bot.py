from discord.ext import commands, utils


# A bot class that inherits all functionality.
bot = utils.Bot(command_prefix=commands.when_mentioned)


bot.run("TOKEN")
