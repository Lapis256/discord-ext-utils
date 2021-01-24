from re import compile as _compile

from discord import Embed, NotFound
from discord.embeds import EmptyEmbed
from more_itertools import chunked


__all__ = (
    "MinimalExpander",
    "WebhookExpander",
    "Expander"
)

url_regex = _compile(
    r"(?P<start><)?(?P<is_global>!)?https?://(?:(?:ptb|canary|www)\.)?"
    r"discord(?:app)?\.com/channels/(?P<guild>[0-9]{15,21})/"
    r"(?P<channel>[0-9]{15,21})/(?P<message>[0-9]{15,21})(?P<end>>)?"
)
image_types = (".png", ".jpg", ".jpeg", ".webp", ".gif")


async def _fetch_message(guild, channel_id, message_id):
    channel = guild.get_channel(channel_id)
    return await channel.fetch_message(message_id)


def _divide_attachments(attachments):
    images = []
    files = []

    for attachment in attachments:
        is_image = attachment.filename.lower().endswith(image_types)
        if is_image:
            images.append(attachment)
        else:
            files.append(attachment)

    return (images, files)


class MinimalExpander:
    def __init__(self, bot):
        self.bot = bot

    async def check_global_expand(self, guild_id):
        return False

    async def extract_message_iter(self, message):
        for m in url_regex.finditer(message.content):
            if m["start"] and m["end"]:
                continue

            guild = message.guild
            guild_id: int = int(m["guild"])
            if guild.id != guild_id:
                if not (m["is_global"] and await self.check_global_expand(guild_id)):
                    continue
                guild = self.bot.get_guild(guild_id)

            try:
                yield await _fetch_message(
                    guild=guild,
                    channel_id=int(m["channel"]),
                    message_id=int(m["message"])
                )
            except (NotFound, AttributeError):
                continue

    @staticmethod
    def make_first_embed(message, image_url=EmptyEmbed):
        return Embed(
            description=message.content,
            timestamp=message.created_at
        ).set_author(
            name=message.author.display_name,
            icon_url=message.author.avatar_url,
            url=message.jump_url
        ).set_footer(
            text="{0.guild.name} | {0.channel.name}".format(message),
            icon_url=message.guild.icon_url
        ).set_image(url=image_url)

    def embed_iter(self, message):
        images, _ = _divide_attachments(message.attachments)
        kwargs = {}

        if images:
            kwargs["image_url"] = images[0].proxy_url

        if images or message.content:
            yield self.make_first_embed(message, **kwargs)

        if message.embeds:
            yield message.embeds[0]

    @classmethod
    async def expand(cls, bot, message):
        self = cls(bot)
        async for m in self.extract_message_iter(message):
            for embed in self.embed_iter(m):
                await message.channel.send(embed=embed)


class Expander(MinimalExpander):
    @staticmethod
    def make_image_embed(message, url, current, total):
        return Embed().set_image(
            url=url
        ).set_footer(text="%s/%s" % (current, total))

    @staticmethod
    def make_files_embed(files):
        text = ""
        for file in files:
            text += "[%s](%s)\n" % (file.filename, file.proxy_url)
        return Embed(title="Attachment", description=text)

    def embed_iter(self, message):
        images, files = _divide_attachments(message.attachments)
        kwargs = {}

        if images:
            kwargs["image_url"] = images[0].proxy_url

        if images or message.content:
            yield self.make_first_embed(message, **kwargs)

        for i, image in enumerate(images[1:]):
            yield self.make_image_embed(message, image.proxy_url, i + 2, len(images))

        yield self.make_files_embed(files)

        for embed in message.embeds:
            yield embed

    @classmethod
    async def expand(cls, bot, message):
        self = cls(bot)
        async for m in self.extract_message_iter(message):
            for embed in self.embed_iter(m):
                await message.channel.send(embed=embed)


class WebhookExpander(Expander):
    def __init__(self, bot, webhook):
        super().__init__(bot)
        self.webhook = webhook

    @classmethod
    async def expand(cls, bot, message, webhook):
        self = cls(bot, webhook)
        async for m in self.extract_message_iter(message):
            for embeds in chunked(self.embed_iter(m), 10):
                await self.webhook.send(
                    embeds=embeds,
                    username="%s's Expander" % message.guild.me.display_name,
                    avatar_url=bot.user.avatar_url
                )
