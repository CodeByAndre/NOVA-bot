import discord
from discord.ext import commands

class MuteChannel(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_channels=True)  # Ensure the user has permissions to manage the channel
    async def lock(self, ctx):
        # Get the current channel where the command was executed
        channel = ctx.channel

        
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("Todos os usuários foram bloqueados de falar neste canal.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("Todos os usuários foram desbloqueados para falar neste canal.")

    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Não tens permissão para usar este comando.")
        else:
            await ctx.send("Ocorreu um erro ao tentar bloquear todos os usuários.")

    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Não tens permissão para usar este comando.")
        else:
            await ctx.send("Ocorreu um erro ao tentar desbloquear todos os usuários.")

async def setup(client):
    await client.add_cog(MuteChannel(client))
