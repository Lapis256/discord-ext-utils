import re

from .unicode_emojis import emojis


reverse = list(emojis.items())
reverse.reverse()
reversed_emojis = {v: k for k, v in reverse}
text_to_emoji_regex = re.compile("(?P<all>:(?P<name>.+?):)")
emoji_to_text_regex = re.compile("(?P<emoji>(?:%s))" % (
    "|".join(map(re.escape, reversed_emojis.keys()))
))


def encode(text):
    def repl(match):
        name = match.group("name")
        emoji = emojis.get(name, None)
        if emoji is None:
            return match.group("all")
        return emoji
    return text_to_emoji_regex.sub(repl, text)


def decode(text):
    def repl(match):
        emoji = match.group("emoji")
        return ":%s:" % reversed_emojis.get(emoji, None)
    return emoji_to_text_regex.sub(repl, text)


def count(text, unique=False):
    func = set if unique else list
    return len(func(emoji_to_text_regex.findall(text)))


def get(text):
    return tuple({*emoji_to_text_regex.findall(text)})
