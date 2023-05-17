import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio


client = commands.Bot(command_prefix = '.', intents=discord.Intents.all())

client_status = cycle(['BIP', 'BOP', 'BUP'])

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(client_status)))

@client.event
async def on_ready():
    print('BIP... BOP... BUP... READY!')
    change_status.start()

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename[:-3]}')

async def main():
    async with client:
        await load()
        await client.start("MTEwODM5ODA2NzIzMDcyMDExMg.GmhHNi.m3lJio63F5V35GQbmlA8BPQBmLr94SVFjZ4yhk")

asyncio.run(main())