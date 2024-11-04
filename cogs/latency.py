import discord
from discord.ext import commands


class Latency(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def latency(self, ctx):
        bot_latency = round(self.client.latency * 1000)
        await ctx.send(f'Latency! {bot_latency}ms')

async def setup(client):
    await client.add_cog(Latency(client))