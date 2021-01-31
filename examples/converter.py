from discord.ext.utils import rangeC, ArgumentIsNotInt, OutOfRange
from discord.ext import commands


bot = commands.Bot(command_prefix=commands.when_mentioned)


@bot.command()
async def between(ctx, _range: rangeC(1, 4)):
    # 1 <= _range < 4
    # If there are no arguments within this range, OutOfRange will occur.
    pass


@between.error
async def between_error(ctx, error):
    if isinstance(error, ArgumentIsNotInt):
        await ctx.send("The argument must be numeric.")

    elif isinstance(error, OutOfRange):
        await ctx.send(
            "The argument is out of range. "
            "({0.min} <= arg < {0.max})".format(error)
        )
