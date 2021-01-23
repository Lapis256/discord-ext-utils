from re import compile as _compile

from discord import Embed, NotFound


url_regex = _compile(
    r"(?P<start><)?(?P<is_global>!)?https?://(?:(?:ptb|canary|www)\.)?"
    r"discord(?:app)?\.com/channels/(?P<guild>[0-9]{15,21})/"
    r"(?P<channel>[0-9]{15,21})/(?P<message>[0-9]{15,21})(?P<end>>)?"
)


class Expander:
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
    def make_embed(message, content=None):
        embed = Embed(
            description=content or message.content,
            timestamp=message.created_at
        )

        if message.attachments:
            embed.set_image(url=message.attachments[0].proxy_url)

        embed.set_author(
            name=message.author.display_name,
            icon_url=message.author.avatar_url,
            url=message.jump_url
        )

        return embed.set_footer(
            text="{0.guild.name} | {0.channel.name}".format(message),
            icon_url=message.guild.icon_url
        )

    def make_image_embed(self, message, url, current, length):
        embed = self.make_embed(message, content="%s/%s" % (current, length))
        return embed.set_image(url=url)

    def embed_iter(self, message):
        if message.content:
            yield self.make_embed(message)

        length = len(message.attachments)
        for i, attachment in enumerate(message.attachments[1:]):
            yield self.make_image_embed(message, attachment.proxy_url, i + 2, length)

        for embed in message.embeds:
            yield embed

    @classmethod
    async def expand(cls, bot, message):
        self = cls(bot)
        async for m in self.extract_message_iter(message):
            for embed in self.embed_iter(m):
                await message.channel.send(embed=embed)


async def _fetch_message(guild, channel_id, message_id):
    channel = guild.get_channel(channel_id)
    return await channel.fetch_message(message_id)
