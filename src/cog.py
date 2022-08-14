import asyncio

import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Bot
from discord_slash import cog_ext
from discord_slash import SlashContext
from joke_api import get_geek_joke
from utils.time_util import seconds_until


class Descriptions:
    SETUP_DAILY_JOKE = (
        "The bot will send a joke everyday at 11:00 am PST in the current channel"
    )
    TURN_OFF_DAILY_JOKE = "Turn off the current daily joke if there is any"
    TELL_GEEK_JOKE = "Send a random programming joke"
    HELP = "Display the list of commands and their usages"


class Slash(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.channel_ids = set()

        self._tell_daily_joke.start()

    @cog_ext.cog_slash(name="tell-geek-joke", description=Descriptions.TELL_GEEK_JOKE)
    async def _tell_geek_joke(self, ctx: SlashContext):
        await ctx.send(content=get_geek_joke())

    @cog_ext.cog_slash(
        name="setup-daily-joke", description=Descriptions.SETUP_DAILY_JOKE
    )
    async def _setup_daily_joke(self, ctx: SlashContext):
        self.channel_ids.add(ctx.channel_id)
        await ctx.send("daily joke is successfully set up!")

    @cog_ext.cog_slash(
        name="turn-off-daily-joke", description=Descriptions.TURN_OFF_DAILY_JOKE
    )
    async def _turn_off_daily_joke(self, ctx: SlashContext):
        if ctx.channel_id in self.channel_ids:
            self.channel_ids.remove(ctx.channel_id)
            await ctx.send("daily joke is now removed!")
        else:
            await ctx.send(
                "This channel does not have any daily joke setup", hidden=True
            )

    @cog_ext.cog_slash(name="help", description=Descriptions.HELP)
    async def _help(self, ctx: SlashContext):
        help_msg = f"""
        `tell-geek-joke` - {Descriptions.TELL_GEEK_JOKE}
        `setup-daily-joke` - {Descriptions.SETUP_DAILY_JOKE}
        `help` - {Descriptions.HELP}
        """
        embed_content = discord.Embed(
            title="Here's what you can do with Thalia!",
            type="rich",
            description=help_msg,
        )
        await ctx.send(embed=embed_content)

    @tasks.loop(seconds=1)
    async def _tell_daily_joke(self):
        await asyncio.sleep(seconds_until(11, 00))

        message = "_What's up brogrammers? Here's the joke of the day:_\n"
        for channel_id in self.channel_ids:
            channel = self.bot.get_channel(channel_id)
            await channel.send(message + f"**{get_geek_joke()}**")


def setup(bot):
    bot.add_cog(Slash(bot))
