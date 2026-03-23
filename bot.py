import discord
import asyncio
import random
from datetime import datetime, timezone
import os
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1484101693649064039
PORTO_CHANNEL_ID = 1484101442808578148

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def clear_bot_messages(channel):
    async for message in channel.history(limit=100):
        if message.author == client.user:
            await message.delete()

async def send_poll():
    channel = client.get_channel(CHANNEL_ID)
    await clear_bot_messages(channel)
    msg = await channel.send("Wie is er vandaag?")
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

async def send_porto():
    channel = client.get_channel(PORTO_CHANNEL_ID)
    await clear_bot_messages(channel)
    number = random.randint(100, 999)
    await channel.send(f"`De porto is: {number}`")

async def daily_message():
    await client.wait_until_ready()

    while not client.is_closed():
        now = datetime.now(timezone.utc)

        # Wait until 02:00 UTC
        target = now.replace(hour=2, minute=0, second=0, microsecond=0)
        if now >= target:
            target = target.replace(day=target.day + 1)

        wait_seconds = (target - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        await send_poll()
        await send_porto()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    client.loop.create_task(daily_message())

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "!test":
        await send_poll()

    if message.content == "?rnd":
        if message.channel.id == PORTO_CHANNEL_ID:
            await message.delete()
            number = random.randint(100, 999)
            await clear_bot_messages(message.channel)
            await message.channel.send(f"`De porto is: {number}`")
        else:
            await message.channel.send(f"Gebruik <#1484101442808578148>!")

client.run(TOKEN)