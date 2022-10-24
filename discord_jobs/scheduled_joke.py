from datetime import datetime
from datetime import timedelta

from cron_converter import Cron
from discord.ext import tasks
from discord.ext.commands import Bot

from db import JokeSchedule
from thalia.joke_api import get_geek_joke


@tasks.loop(minutes=1)
async def scheduled_joke(bot: Bot) -> None:
    now = datetime.now()
    a_min_ago = now - timedelta(minutes=1)
    schedule_records = JokeSchedule.select()

    for record in schedule_records:
        assert isinstance(record, JokeSchedule)

        if now.strftime("%m/%d/%Y, %H:%M") == Cron(record.cron_expression).schedule(
            start_date=a_min_ago
        ).next().strftime("%m/%d/%Y, %H:%M"):
            channel = bot.get_channel(record.channel_id)
            await channel.send(
                "_What's up brogrammers? Here's the joke of the day:_\n"
                f"**{get_geek_joke()}**"
            )
