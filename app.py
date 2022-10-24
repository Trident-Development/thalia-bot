from discord.ext import commands
from discord_slash import SlashCommand

from config import DISCORD_TOKEN
from discord_jobs.scheduled_joke import scheduled_joke


bot = commands.Bot(command_prefix="/")
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
bot.load_extension("discord_cog.slash_routes")

scheduled_joke.start(bot)

bot.run(DISCORD_TOKEN)
