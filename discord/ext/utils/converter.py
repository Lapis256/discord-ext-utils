from string import Formatter

from discord.ext.commands import Converter
from .errors import ArgumentIsNotInt, OutOfRange

__all__ = ("rangeC", "formatC")


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


class _KeyOnlyFormatter(Formatter):
    def format(self, format_string, kwargs, recursion_depth=2):
        if recursion_depth < 0:
            raise ValueError("Max string recursion exceeded")
        result = []
        for literal_text, field_name, format_spec, conversion in self.parse(format_string):
            if literal_text:
                result.append(literal_text)

            if field_name is not None:
                obj, _ = self.get_field(field_name, kwargs)
                obj = self.convert_field(obj, conversion)
                format_spec = self.format(format_spec, kwargs, recursion_depth-1)
                result.append(self.format_field(obj, format_spec))

        return "".join(result)

    def get_field(self, field_name, kwargs):
        try:
            return super().get_field(field_name, (), kwargs)
        except (KeyError, AttributeError, ValueError) as e:
            return "{%s}" % field_name, field_name


class formatC(Converter):
    def __init__(self, kwargs=None, from_bot=False):
        self.kwargs = kwargs
        self.from_bot = from_bot

        if kwargs is None:
            self.kwargs = {}
            self.from_bot = True

    async def convert(self, ctx, argument):
        global_kwargs = ctx.bot.format_converter_kwargs
        kwargs = global_kwargs if self.from_bot else self.kwargs
        return _KeyOnlyFormatter().format(argument, kwargs)
