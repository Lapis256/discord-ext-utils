from setuptools import setup
from re import search

with open("discord/ext/utils/__init__.py") as f:
    version = search(r'__version__\s=\s"(.*?)"', f.read()).group(1)

setup(
    name="discord-ext-utils",
    author="Lapis256",
    url="https://github.com/Lapis256/discord-ext-utils",
    version=version,
    packages=["discord.ext.utils", "discord.ext.utils.cogs"],
    license="MIT",
    description="An extension module of discord.ext.commands.",
    install_requires=["discord.py>=1.5.0,<2.0.0", "more-itertools"],
    python_requires=">=3.6.0"
)
