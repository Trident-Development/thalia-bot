from discord.ext import commands
from discord.ext.commands import Bot
from discord_slash import cog_ext
from discord_slash import SlashContext

from const.command_descriptions import HELP
from const.command_descriptions import SETUP_DAILY_JOKE
from const.command_descriptions import TELL_GEEK_JOKE
from const.command_descriptions import TURN_OFF_DAILY_JOKE
from discord_cog.controllers import help
from discord_cog.controllers import setup_daily_joke
from discord_cog.controllers import tell_geek_joke
from discord_cog.controllers import turn_off_daily_joke


class Slash(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.channel_ids = set()

    @cog_ext.cog_slash(name="tell-geek-joke", description=TELL_GEEK_JOKE)
    async def _tell_geek_joke(self, ctx: SlashContext):
        await tell_geek_joke(ctx)

    @cog_ext.cog_slash(name="setup-daily-joke", description=SETUP_DAILY_JOKE)
    async def _setup_daily_joke(self, ctx: SlashContext, timestamp: str):
        await setup_daily_joke(ctx, timestamp)

    @cog_ext.cog_slash(name="turn-off-daily-joke", description=TURN_OFF_DAILY_JOKE)
    async def _turn_off_daily_joke(self, ctx: SlashContext):
        await turn_off_daily_joke(ctx)

    @cog_ext.cog_slash(name="help", description=HELP)
    async def _help(self, ctx: SlashContext):
        await help(ctx)


def setup(bot):
    bot.add_cog(Slash(bot))
