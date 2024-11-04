import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kick(ctx, *, member:discord.Member):
        await member.kick()


async def setup(client):
    await client.add_cog(Kick(client))