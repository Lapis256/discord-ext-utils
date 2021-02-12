from discord.ext import commands
from discord.ext.utils import (
    rangeC,
    formatC
    ArgumentIsNotInt,
    OutOfRange
)


bot = commands.Bot(command_prefix=commands.when_mentioned)


# Range Converter
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


# Format Converter 1
@bot.command()
async def echo(ctx, *, message: formatC({"version": "v1.0"})):
    await ctx.send(message)

# @bot_name echo My version is {version}.
# => My version is v1.0.

# @bot_name echo My version is {version}. {hogehoge} {} {{}}
# => My version is v1.0. {hogehoge} {} {}


# Format Converter 2
class Bot(commands.Bot):
    format_converter_kwargs = {"version": "v2.0"}

bot = Bot(command_prefix=commands.when_mentioned)

@bot.command()
async def echo(ctx, *, message: formatC({"version": "v1.0"}, from_bot=True)):
    await ctx.send(message)
# or
async def echo(ctx, *, message: formatC):

# @bot_name echo My version is {version}.
# => My version is v2.0.

# @bot_name echo My version is {version}. {hogehoge} {} {{}}
# => My version is v2.0. {hogehoge} {} {}
