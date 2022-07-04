import logging
from discord import Client
from pyjokes import get_joke

from config import DISCORD_TOKEN

__LOGGER = logging.getLogger(__name__)


client = Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # ignore the message from the bot so there is no conflict
    if message.author == client.user:
        return
    if message.content == '/tell-joke':
        await message.channel.send(get_joke(language="en", category="neutral"))

client.run(DISCORD_TOKEN)
