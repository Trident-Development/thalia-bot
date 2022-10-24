import discord
from discord_slash import SlashContext

from const.command_descriptions import HELP
from const.command_descriptions import SETUP_DAILY_JOKE
from const.command_descriptions import TELL_GEEK_JOKE
from thalia.joke_api import get_geek_joke


async def tell_geek_joke(ctx: SlashContext) -> None:
    await ctx.send(content=get_geek_joke())


async def setup_daily_joke(ctx: SlashContext) -> None:
    pass


async def turn_off_daily_joke(ctx: SlashContext) -> None:
    pass


async def help(ctx: SlashContext) -> None:
    help_msg = (
        f"`tell-geek-joke` - {TELL_GEEK_JOKE}"
        f"`setup-daily-joke` - {SETUP_DAILY_JOKE}"
        f"`help` - {HELP}"
    )
    embed_content = discord.Embed(
        title="Here's what you can do with Thalia!",
        type="rich",
        description=help_msg,
    )
    await ctx.send(embed=embed_content)
