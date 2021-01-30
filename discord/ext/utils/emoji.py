import re

from .unicode_emojis import emojis


__all__ = ("encode", "decode", "count", "get", "emojis")

_reverse = list(emojis.items())
_reverse.reverse()
_reversed_emojis = {v: k for k, v in _reverse}
_text_to_emoji_regex = re.compile("(?P<all>:(?P<name>.+?):)")
_emoji_to_text_regex = re.compile("(?P<emoji>(?:%s))" % (
    "|".join(map(re.escape, _reversed_emojis.keys()))
))


def encode(text):
    def repl(match):
        name = match.group("name")
        emoji = emojis.get(name, None)
        if emoji is None:
            return match.group("all")
        return emoji
    return _text_to_emoji_regex.sub(repl, text)


def decode(text):
    def repl(match):
        emoji = match.group("emoji")
        return ":%s:" % _reversed_emojis.get(emoji, None)
    return _emoji_to_text_regex.sub(repl, text)


def count(text, unique=False):
    func = set if unique else list
    return len(func(_emoji_to_text_regex.findall(text)))


def get(text):
    return tuple({*_emoji_to_text_regex.findall(text)})
