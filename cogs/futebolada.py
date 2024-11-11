import discord
from discord.ext import commands
import random

class Futebolada(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def futebolada(self, ctx, *nomes):
        if len(nomes) < 2:
            await ctx.send("Precisas de pelo menos 2 pessoas para criar equipes!")
            return

        nomes = list(nomes)
        random.shuffle(nomes)

        meio = len(nomes) // 2
        equipe_1 = nomes[:meio]
        equipe_2 = nomes[meio:]

        embed = discord.Embed(title="Equipas da Futebolada", color=discord.Color.green())
        embed.add_field(name="EQUIPA 1", value="\n".join(equipe_1), inline=True)
        embed.add_field(name="EQUIPA 2", value="\n".join(equipe_2), inline=True)

        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Futebolada(client))
