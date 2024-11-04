import discord
from discord.ext import commands

class Unban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def unban(ctx, *, id:int):
        user = await client.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(f"O/A {user}, acabou de set desbanido")


async def setup(client):
    await client.add_cog(Unban(client))