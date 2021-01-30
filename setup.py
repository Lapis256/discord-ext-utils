from setuptools import setup
from re import search

with open("requirements.txt") as f:
    requirements = f.readlines()

with open("discord/ext/utils/__init__.py") as f:
    version = search(r'__version__\s=\s"(.*?)"', f.read()).group(1)

packages = [
    "discord.ext.utils",
    "discord.ext.utils.cogs",
    "discord.ext.utils.unicode_emojis"
]

setup(
    name="discord-ext-utils",
    author="Lapis256",
    url="https://github.com/Lapis256/discord-ext-utils",
    version=version,
    packages=packages,
    license="MIT",
    description="An extension module of discord.ext.commands.",
    install_requires=requirements,
    python_requires=">=3.6.0"
)
