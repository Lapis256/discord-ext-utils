from discord.ext.commands import Converter, BadArgument


__all__ = (
    "RangeConverter",
    "WithinConverter",
    "rangeC",
    "within"
)


class OutOfRange(BadArgument):
    def __init__(self, argument, type, min, max):
        self.argument = argument
        self.type = type
        self.min = min
        self.max = max

        super().__init__("%s is out of range." % argument)


class RangeConverter(Converter):
    def __init__(self, min, max=None, /):
        if max is None:
            self.min = 0
            self.max = min
        else:
            self.min = min
            self.max = max

        super().__init__()

    def check(self, number):
        return self.min <= number < self.max

    async def convert(self, ctx, argument):
        if not argument.isdigit():
            raise BadArgument("%s is not int" % argument)
        int_argument = int(argument)

        if self.check(int_argument):
            return int_argument
        raise OutOfRange(int_argument, type(self), self.min, self.max)


class WithinConverter(RangeConverter):
    def check(self, number):
        return self.min <= number <= self.max


def rangeC(min, max=None, /):
    return RangeConverter(min, max)


def within(min, max=None, /):
    return WithinConverter(min, max)
