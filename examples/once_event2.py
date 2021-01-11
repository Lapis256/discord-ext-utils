from discord.ext import utils


class MyBot(utils.Bot):
    async def once_ready(self):
        pass
        # It will be executed only once.

    async def on_ready():
        pass
        # It will be executed many times.

bot = MyBot(command_prefix=".")


bot.run("TOKEN")
