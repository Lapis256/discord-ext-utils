from discord.ext.utils import PresenceTask
from discord.ext import commands


class MyBotPresence(PresenceTask):
    def help(bot):
        return f"@{bot.user.name} help"

    def version(bot):
        return f"{bot.user.name} - v0.1"


bot = commands.Bot(command_prefix=commands.when_mentioned)


MyBotPresence(bot, 15, presences=[
    "I am the best bot in the world!!"
]).start()


bot.run("TOKEN")
