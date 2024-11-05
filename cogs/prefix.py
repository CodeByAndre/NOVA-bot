import discord
from discord.ext import commands
import json

class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def prefix(self, ctx, prefix):
        with open('prefix.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefix.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"O prefixo foi atualizado para: `{prefix}`", delete_after=5)

        await ctx.message.delete()

async def setup(client):
    await client.add_cog(Prefix(client))
