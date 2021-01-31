from discord.ext.utils import MinimalExpander
from discord.ext import commands


bot = commands.Bot(command_prefix=commands.when_mentioned)


# Expand simple.
bot.load_extension("discord.ext.utils.cogs.minimal_expander")

# Expand all.
# self.load_extension("discord.ext.utils.cogs.expander")

# Expand all and send with webhook.
# self.load_extension("discord.ext.utils.cogs.webhook_expander")


class Expander(MinimalExpander):
    async def check_global_expand(self, guild_id):
        # guild_id is the id of the guild that has the message to expand.
        # If this function returns True, allow the message to be expanded to another guild.
        pass


# Customize the behavior of the deployment.
# All Cogs are named ExpanderCog.
bot.get_cog("ExpanderCog").expander = Expander


bot.run("TOKEN")
