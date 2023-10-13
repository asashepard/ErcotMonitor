import asyncio
import functools
import time
import typing

import discord

import main
import responses
import os

TOKEN = os.environ.get('token')
GRAPH = discord.File('plot.png')


async def send_message(message, user_message):
    try:
        response = responses.handle_response(user_message)
        await message.channel.send(response[0])
        if response[1]:
            await message.channel.send(file=GRAPH)
    except Exception as e:
        print(e)


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
        time.sleep(seconds)

# todo run automated / live updates

# todo run emergency notification updates based on values


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} has started running')
        await call_updates(5)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said : '{user_message}' ({channel})")

        await send_message(message, user_message)

    client.run(TOKEN)
