import asyncio
import functools
import time
import typing

import discord

import main
import responses
import os

TOKEN = os.environ.get('token')

embed = discord.Embed(title='')

message_def = [None]  # only index 0 occupied

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)


async def send_message(channel, user_message):
    try:
        should_repeat = responses.handle_response(user_message)  # whether message is updating
        temp = message_def[0]
        with open('plot.png', 'r'):
            message_def[0] = await channel.send(file=discord.File('plot.png'), embed=embed)
        if not should_repeat:
            message_def[0] = temp  # reset message_def to prev state
    except Exception as e:
        print(e)


# REPEATING #

def to_thread(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


@to_thread
def call_updates(seconds):
    main.data_class.setup()
    while main.data_class.continue_running:
        main.data_class.scrape_data()
        if message_def[0] is not None:  # there is a repeating message
            bot.dispatch('update_message')
        time.sleep(seconds)


# RUN #


def run_discord_bot():
    @bot.event
    async def on_ready():
        print(f'{bot.user} has started running')
        await call_updates(60)

    @bot.event
    async def on_message(message):
        if not message.author.bot:
            await send_message(message.channel, str(message.content))

    @bot.event
    async def on_update_message():
        await message_def[0].edit(embed=responses.generate_repeating())
        if float(main.data_class.last_update[1]) < 59.4:
            await message_def[0].channel.send(responses.generate_warning())

    bot.run(TOKEN)
