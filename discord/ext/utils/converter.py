from discord.ext.commands import Converter, BadArgument


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


class rangeC(Converter):
    def __init__(self, min, max=None, /):
        if max is None:
            self.min = 0
            self.max = min
        else:
            self.min = min
            self.max = max

    async def convert(self, ctx, argument):
        if not argument.isdigit():
            raise ArgumentIsNotInt(argument)
        int_argument = int(argument)

        if self.min <= int_argument < self.max:
            return int_argument
        raise OutOfRange(int_argument, type(self), self.min, self.max)
