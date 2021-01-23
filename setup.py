from setuptools import setup

setup(
    name="discord-ext-utils",
    author="Lapis256",
    url="https://github.com/Lapis256/discord-ext-utils",
    version="0.2",
    packages=["discord.ext.utils", "discord.ext.utils.cogs"],
    license="MIT",
    description="An extension module of discord.ext.commands.",
    install_requires=["discord.py>=1.2.5"],
    python_requires=">=3.6.0"
)
