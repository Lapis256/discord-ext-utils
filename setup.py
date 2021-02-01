from setuptools import setup
import re

with open("requirements.txt") as f:
    requirements = f.readlines()

version = ""
with open("discord/ext/utils/__init__.py") as f:
    version = re.search(r'^__version__\s*=\s*"(.*?)"', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

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
    python_requires=">=3.8.0"
)
