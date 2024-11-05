from discord.ext import commands, tasks
import discord
from itertools import cycle
import os
import asyncio
import json
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')

def get_prefix(client, message):
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)
        
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix, intents=discord.Intents.all())
client_status = cycle(['BIP', 'BOP', 'BUP'])

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(client_status)))

@client.event
async def on_ready():
    print('Online and ready!')
    change_status.start()

    if os.path.exists("reboot_flag.txt"):
        channel = client.get_channel(1303400665493667863)

        if channel:
            # Get the message ID of the "Rebooting..." message from the file
            with open("reboot_flag.txt", "r") as f:
                rebooting_msg_id = f.read().strip()

            try:
                # Fetch and delete the "Rebooting..." message
                rebooting_msg = await channel.fetch_message(int(rebooting_msg_id))
                await rebooting_msg.delete()
            except Exception as e:
                print(f"Could not delete 'Rebooting...' message: {e}")

            # Send the "Rebooted successfully" message and delete after 5 seconds
            rebooted_message = await channel.send("Rebooted successfully.")
            await rebooted_message.delete(delay=5)

@client.event
async def on_guild_join(guild):
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '/'

    with open('prefix.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)
        
    prefixes.pop(str(guild.id))

    with open('prefix.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename[:-3]}')

async def main():
    async with client:
        await load()
        await client.start(token)

asyncio.run(main())
