import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashContext
from pyjokes import get_joke


class Descriptions:
    TELL_JOKE = "Send a random programming joke"
    HELP = "Display the list of commands and their usages"


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @cog_ext.cog_slash(name="tell-joke", description=Descriptions.TELL_JOKE)
    async def _tell_joke(self, ctx: SlashContext):
        await ctx.send(content=get_joke(language="en", category="neutral"))


    @cog_ext.cog_slash(name="help", description=Descriptions.HELP)
    async def _help(self, ctx: SlashContext):
        help_msg = f"""
        `tell-joke` - {Descriptions.TELL_JOKE}
        `help` - {Descriptions.HELP}
        """
        embed_content = discord.Embed(
            title="Here's what you can do with GeekJoke!",
            type="rich",
            description=help_msg,
        )
        await ctx.send(embed=embed_content)


def setup(bot):
    bot.add_cog(Slash(bot))
