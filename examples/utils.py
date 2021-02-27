from pathlib import Path

from discord.ext import utils


# cogs/cog.py
# cogs/foo/cog.py
utils.get_extensions("cogs")
utils.get_extensions(Path("cogs"))
# -> ["cogs.cog", "cogs.foo.cog"]

utils.get_extensions("cogs", recursive=False)
# -> ["cogs.cog"]

# cogs/cog/__init__.py
# cogs/cog/util.py
# cogs/foo/cog/__init__.py
# cogs/foo/cog/util.py
utils.get_extensions("cogs")
# -> ["cogs.cog", "cogs.foo.cog"]

utils.get_extensions("cogs", recursive=False)
# -> ["cogs.cog"]

# cogs/cog/__init__.py
# cogs/cog/foo/__init__.py
utils.get_extensions("cogs")
# -> ["cogs.cog"]

# cogs/cog/__init__.py
# cogs/foo/cog/__init__.py
# cogs/foo/ping.py
# cogs/help.py
utils.get_extensions("cogs")
# -> ["cogs.help", "cogs.cog", "cogs.foo.ping", "cogs.foo.cog"]

utils.get_extensions("cogs", recursive=False)
# -> ["cogs.help", "cogs.cog"]
