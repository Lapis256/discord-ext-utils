from discord.ext import commands
from discord.ext.utils.expander import *


class ExpanderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cls = Expander
        self.args = ()
        self.kwargs = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            await expand(
                self.bot,
                message,
                cls=self.cls,
                cls_args=self.args,
                cls_kwargs=self.kwargs
            )


def setup(bot):
    bot.add_cog(ExpanderCog(bot))
