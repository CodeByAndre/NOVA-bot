import discord
from discord.ext import commands

class Clean(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clean(self, ctx, *, number:int):
        remove = await ctx.channel.purge(limit= number + 1)
        await ctx.send(f"Foram eliminadas {len(remove) -1}, menssagens", delete_after=3.5)

    @clean.error
    async def clean_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a position you would like to mark.") 

async def setup(client):
    await client.add_cog(Clean(client))