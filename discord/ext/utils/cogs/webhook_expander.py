from discord.ext import commands
from discord.ext.utils.expander import WebhookExpander


class ExpanderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.expander = WebhookExpander

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        webhook = await message.channel.create_webhook(
            name="Message Expander",
            reason="For message expand."
        )
        await self.expander.expand(self.bot, message, webhook)
        await webhook.delete()


def setup(bot):
    bot.add_cog(ExpanderCog(bot))
