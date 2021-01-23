from .expander import ExpanderCog


def setup(bot):
    bot.add_cog(ExpanderCog(bot))
