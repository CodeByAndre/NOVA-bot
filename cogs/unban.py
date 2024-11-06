import discord
from discord.ext import commands

class Unban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, id: int):
        try:
            user = await self.client.fetch_user(id)
            await ctx.guild.unban(user)
            await ctx.send(f"{user} foi desbanido/a do servidor.")
        except discord.NotFound:
            await ctx.send("Utilizador não encontrado. Verifica o ID.")
        except discord.Forbidden:
            await ctx.send("Não tenho permissões para desbanir este utilizador.")
        except Exception as e:
            await ctx.send(f"Ocorreu um erro: {e}")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Não tens permissão para usar este comando.")

async def setup(client):
    await client.add_cog(Unban(client))
