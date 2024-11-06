import discord
from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def invite(self, ctx):
        invite_url = discord.utils.oauth_url(self.client.user.id, permissions=discord.Permissions(permissions=8))

        embed = discord.Embed(
            title="Convite para me adicionar em outros servidores",
            description=f"Clique [aqui]({invite_url}) para me adicionar a um novo servidor!",
            color=discord.Color.green()
        )
        
        embed.set_thumbnail(url=self.client.user.avatar.url)
        embed.set_footer(text="Obrigado por me adicionar ao teu servidor!")

        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Invite(client))
