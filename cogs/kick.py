import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, motivo=None):

        if ctx.guild.me.guild_permissions.kick_members:
            await member.kick(reason=motivo)
            await ctx.send(f"{member} foi expulso/a do servidor. Motivo: {motivo if motivo else 'Nenhum motivo fornecido.'}")
        else:
            await ctx.send("Não tenho permissão para expulsar membros.")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Não tens permissão para usar este comando.")

async def setup(client):
    await client.add_cog(Kick(client))
