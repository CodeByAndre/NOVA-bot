import discord
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        
        member = member or ctx.author

        embed = discord.Embed(
            title=f"Avatar de {member}",
            description=f"[Clica para baixar]({member.avatar.url})",
            colour=discord.Color.random()
        )
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Avatar(client))