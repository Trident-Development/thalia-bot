import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashContext
from joke_api import get_geek_joke


class Descriptions:
    TELL_GEEK_JOKE = "Send a random programming joke"
    HELP = "Display the list of commands and their usages"


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="tell-joke", description=Descriptions.TELL_JOKE)
    async def _tell_joke(self, ctx: SlashContext):
        await ctx.send(content=get_geek_joke())

    @cog_ext.cog_slash(name="help", description=Descriptions.HELP)
    async def _help(self, ctx: SlashContext):
        help_msg = f"""
        `tell-geek-joke` - {Descriptions.TELL_GEEK_JOKE}
        `help` - {Descriptions.HELP}
        """
        embed_content = discord.Embed(
            title="Here's what you can do with Thalia!",
            type="rich",
            description=help_msg,
        )
        await ctx.send(embed=embed_content)


def setup(bot):
    bot.add_cog(Slash(bot))
