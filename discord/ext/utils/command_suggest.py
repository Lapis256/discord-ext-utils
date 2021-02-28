import itertools

from discord.ext.commands.view import StringView
from Levenshtein import distance
from discord.ext.commands import (
    Group,
    CommandError,
    CommandNotFound
)


__all__ = ("suggest", "AutoSuggestion")


def split_content(content, prefix):
    view = StringView(content)
    view.skip_string(prefix)
    words = []
    while True:
        words.append(view.get_word())
        if view.eof:
            break
        view.skip_ws()
    return words


async def find_command(words, group, max_distance, check, nest=0):
    suggest_commands = {}
    for word, command_data in itertools.product(words[nest:], group.all_commands.items()):
        name, command = command_data

        dist = distance(name, word)
        is_valid = await check(command)
        if dist > max_distance or (not is_valid):
            continue

        sub = {}
        if nest < len(words)-1:
            if not isinstance(command, Group):
                continue
            sub = await find_command(words, command, max_distance, check, nest+1)
            if not sub:
                continue

        suggest_commands[name] = {"dist": dist, "sub": sub}

    return sorted(suggest_commands.items(), key=lambda x: x[1]["dist"])


def format_suggest_commands(commands):
    formated_commands = []
    for name, command in commands:
        if command["sub"]:
            sub = format_suggest_commands(command["sub"])
            for sub_name in sub:
                formated_commands.append("%s %s" % (name, sub_name))
        else:
            formated_commands.append(name)

    return formated_commands


async def suggest(ctx, content, max_distance=3, num=3):
    async def check(command):
        if command.hidden:
            return False
        try:
            return await command.can_run(ctx)
        except CommandError:
            return False

    texts = split_content(content, ctx.prefix)
    commands = await find_command(texts, ctx.bot, max_distance, check)
    return format_suggest_commands(commands)[:num]


class AutoSuggestion:
    def __init__(self, *args, max_distance=3, suggestion_num=3, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_distance = max_distance
        self.suggestion_num = suggestion_num

        self.after_invoke(self.__after_invoke)

    async def __after_invoke(self, ctx):
        from discord.ext.commands import CommandNotFound
        if ctx.subcommand_passed is not None and\
           ctx.invoked_subcommand is None:
            exc = CommandNotFound('Command "{}" is not found'.format(ctx.subcommand_passed))
            self.dispatch('command_error', ctx, exc)

    async def on_command_error(self, ctx, error):
        print(error)
        if isinstance(error, CommandNotFound):
            commands = map(lambda c: "`%s%s`" % (ctx.prefix, c), await suggest(
                ctx,
                ctx.message.content,
                self.max_distance,
                self.suggestion_num
            ))
            await ctx.send("%s\nDid you mean? :\n%s" % (error, "\n".join(commands)))
        else:
            await super().on_command_error(ctx, error)
