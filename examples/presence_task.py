from discord.ext.utils import Bot, PresenceTask, presence
from discord.ext import commands


class MyBotPresence(PresenceTask):
    @presence
    def help(bot):
        return f"@{bot.user.name} help"
    
    @presence
    def version(bot):
        return f"{bot.user.name} - v0.1"

class MyBot(Bot):
    async def once_ready(self):
        self.presence = MyBotPresence(self, delay=15)
        self.presence.start()

bot = MyBot(command_prefix=commands.when_mentioned)


bot.run("TOKEN")
