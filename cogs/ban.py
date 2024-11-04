import discord
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ban(ctx, *, member:discord.Member):
        await member.ban()


async def setup(client):
    await client.add_cog(Ban(client))