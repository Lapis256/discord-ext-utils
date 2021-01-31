from discord.ext.commands import BadArgument


__all__ = (
    "ArgumentIsNotInt",
    "OutOfRange"
)


class ArgumentIsNotInt(BadArgument):
    def __init__(self, argument):
        self.argument = argument
        super().__init__("%s is not int." % argument)


class OutOfRange(BadArgument):
    def __init__(self, argument, type, min, max):
        self.argument = argument
        self.type = type
        self.min = min
        self.max = max
        super().__init__("%s is out of range." % argument)
