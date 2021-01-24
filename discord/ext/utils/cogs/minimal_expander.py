from discord.ext import commands
from discord.ext.utils.expander import MinimalExpander


class ExpanderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.expander = MinimalExpander

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        await self.expander.expand(self.bot, message)


def setup(bot):
    bot.add_cog(ExpanderCog(bot))
