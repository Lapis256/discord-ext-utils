from discord.ext.utils import emoji


emoji.encode("Discord is :+1:")
# 'Discord is 👍'

emoji.decode("Discord is 👍")
# 'Discord is :thumbsup:'

emoji.count("😀😁😀😁")
# 4

emoji.count("😀😁😀😁", unique=True)
# 2

emoji.get("😀😁😀😁")
# ('😀', '😁')
