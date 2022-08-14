import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Bot
from discord_slash import cog_ext
from discord_slash import SlashContext
from pyjokes import get_joke


class Descriptions:
    TELL_JOKE = "Send a random programming joke"
    SETUP_DAILY_JOKE = "The bot will send a joke everyday at 11:00 am PST"
    HELP = "Display the list of commands and their usages"


class Slash(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.channel_ids = set()

        self._tell_daily_joke.start()

    @cog_ext.cog_slash(name="tell-joke", description=Descriptions.TELL_JOKE)
    async def _tell_joke(self, ctx: SlashContext):
        await ctx.send(content=get_joke(language="en", category="neutral"))

    @cog_ext.cog_slash(
        name="setup-daily-joke", description=Descriptions.SETUP_DAILY_JOKE
    )
    async def _setup_daily_joke(self, ctx: SlashContext):
        self.channel_ids.add(ctx.channel_id)
        await ctx.send("set up successfully!")

    @cog_ext.cog_slash(name="help", description=Descriptions.HELP)
    async def _help(self, ctx: SlashContext):
        help_msg = f"""
        `tell-joke` - {Descriptions.TELL_JOKE}
        `setup-daily-joke` - {Descriptions.SETUP_DAILY_JOKE}
        `help` - {Descriptions.HELP}
        """
        embed_content = discord.Embed(
            title="Here's what you can do with GeekJoke!",
            type="rich",
            description=help_msg,
        )
        await ctx.send(embed=embed_content)

    @tasks.loop(seconds=5)
    async def _tell_daily_joke(self):
        message = "What's up brogrammers? Here's the joke of the day:\n"
        for channel_id in self.channel_ids:
            channel = self.bot.get_channel(channel_id)
            await channel.send(message)


def setup(bot):
    bot.add_cog(Slash(bot))
