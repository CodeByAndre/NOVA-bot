import discord
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def avatar(self, ctx, member:discord.Member):
        embed = discord.Embed(
        title=f"Avatar de {member}",
        description=f"[Clica para baixar]({member.avatar_url_as(static_format='png')})",
        colour=discord.Color.random()
        )
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Avatar(client))