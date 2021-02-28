from discord.ext import commands
from discord.ext.utils import Bot, AutoSuggestion, suggest

bot = Bot(...

# or

# AutoSuggestion must be written before commands.Bot.
class MyBot(AutoSuggestion, commands.Bot):
    pass

bot = MyBot(...

# or

@bot.event
async def on_command_error(ctx, error):
    commands: list[str] = await suggest(ctx, ctx.message.content, max_distance=3, suggestion_num=3)
    ...
