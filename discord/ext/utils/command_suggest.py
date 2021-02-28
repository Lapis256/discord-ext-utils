from discord.ext.commands.view import StringView
from discord.ext.commands.core import hooked_wrapped_callback
from Levenshtein import distance
from discord.ext.commands import (
    Group,
    Command,
    CommandError,
    CommandNotFound
)


__all__ = ("suggest", "AutoSuggestion")


def split_content(prefix, content):
    contents = []
    view = StringView(content)
    view.skip_string(prefix)

    while not view.eof:
        word = view.get_word()
        contents.append(word)
        view.skip_ws()
    return contents


def format_content(prefix, content):
    return " ".join(split_content(prefix, content))


def find_nearest_commands(commands, content, max_distance):
    _commands = []
    for command in commands:
        dist = distance(content, command)
        if dist > max_distance:
            continue
        _commands.append((dist, command))
    return [*map(lambda x: x[1],
                sorted(_commands, key=lambda x: x[0])
           )]


async def get_filtered_commands(group, check, parent=None):
    commands = []
    if parent is None:
        parent = []
    for name, command in group.all_commands.items():
        if not await check(command):
            continue

        parent_str = " ".join(parent) + (" " if len(parent) else "")

        if isinstance(command, Group):
            commands.append(parent_str + name)
            parent.append(name)
            subcommands = await get_filtered_commands(command, check, parent)
            parent.pop()
            commands += subcommands

        elif isinstance(command, Command):
            commands.append(parent_str + name)
    return commands


def get_full_name(prefix, content, last):
    contents = split_content(prefix, content)
    for i, content in enumerate(contents):
        if content != last:
            continue
    else:
        return " ".join(contents[:i+1])


async def suggest(ctx, content, max_distance=3, max_suggestion=3):
    async def check(command):
        if command.hidden:
            return False
        try:
            return await command.can_run(ctx)
        except CommandError:
            return False

    formated_content = format_content(ctx.prefix, ctx.message.content)
    commands = await get_filtered_commands(ctx.bot, check)
    return find_nearest_commands(commands, formated_content, max_distance)[:max_suggestion]


class AutoSuggestion:
    def __init__(self, *args, max_distance=3, max_suggestion=3, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_distance = max_distance
        self.max_suggestion = max_suggestion

    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            content = ctx.message.content
            raw_commands = await suggest(ctx, content, self.max_distance, self.max_suggestion)
            if not raw_commands:
                return

            commands = map(lambda c: "`%s`" % c, raw_commands)
            replaced_error = str(error).replace('"', "`")
            await ctx.send(
                "%s\nDid you mean? :\n%s" % (replaced_error, "\n".join(commands))
            )
        else:
            await super().on_command_error(ctx, error)

    async def invoke(self, ctx):
        await super().invoke(ctx)
        if (ctx.command is None or ctx.invoked_with) and ctx.subcommand_passed is not None:
            full = get_full_name(ctx.prefix, ctx.message.content, ctx.subcommand_passed)
            exc = CommandNotFound('Command "{}" is not found'.format(full))
            self.dispatch('command_error', ctx, exc)
