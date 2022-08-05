import logging

from discord.ext import commands
from discord_slash import SlashCommand

from config import DISCORD_TOKEN


_LOGGER = logging.getLogger(__name__)

bot = commands.Bot(command_prefix="/")
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

bot.load_extension("cog")
bot.run(DISCORD_TOKEN)

_LOGGER.info("GeekBot started!")
