import discord
from discord.ext import commands

class SlowMode(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_channels=True)  # Verifica se o usuário tem permissão para gerenciar o canal
    async def slowmode(self, ctx, segundos: int):
        """Define o modo lento no canal atual com o tempo especificado em segundos."""
        # Define o modo lento no canal atual com o tempo especificado
        await ctx.channel.edit(slowmode_delay=segundos)
        
        if segundos == 0:
            await ctx.send("Modo lento desativado neste canal.")
        else:
            await ctx.send(f"Modo lento ativado! Os usuários devem esperar {segundos} segundos antes de enviar uma nova mensagem.")

    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Não tens permissão para usar este comando.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Por favor, insere um número válido de segundos para o modo lento.")
        else:
            await ctx.send("Ocorreu um erro ao tentar definir o modo lento.")

async def setup(client):
    await client.add_cog(SlowMode(client))
