import discord
from discord_slash import SlashContext

from const.command_descriptions import HELP
from const.command_descriptions import SETUP_DAILY_JOKE
from const.command_descriptions import TELL_GEEK_JOKE
from db.joke_schedule import JokeSchedule
from thalia.joke_api import get_geek_joke


async def tell_geek_joke(ctx: SlashContext) -> None:
    await ctx.send(content=get_geek_joke())


async def setup_daily_joke(ctx: SlashContext, timestamp: str) -> None:
    try:
        hour, min = timestamp.split(":")
    except:
        await ctx.send("Unable to setup daily joke :(", hidden=True)
        return

    JokeSchedule.add_record(
        channel_id=ctx.channel_id, cron_expression=f"{min} {hour} * * *"
    )
    await ctx.send("Daily joke is successfully set up!")


async def turn_off_daily_joke(ctx: SlashContext) -> None:
    if JokeSchedule.delete_record(channel_id=ctx.channel_id):
        await ctx.send("Daily joke is removed!")
    else:
        await ctx.send("This channel does not have any daily joke setup!", hidden=True)


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
