import discord
from discord.ext import commands
import youtube_dl
import os

# Configurações do youtube_dl
ytdl_opts = {
    'format': 'bestaudio',
    'noplaylist': 'True'
}
ytdl = youtube_dl.YoutubeDL(ytdl_opts)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """Entra no canal de voz do usuário."""
        if ctx.author.voice:  # Verifica se o usuário está em um canal de voz
            channel = ctx.author.voice.channel
            try:
                await channel.connect()
                await ctx.send(f"Entrei no canal de voz {channel.name}!")
            except Exception as e:
                await ctx.send(f"Erro ao tentar entrar no canal: {e}")
        else:
            await ctx.send("Você precisa estar em um canal de voz para me chamar!")

    @commands.command()
    async def leave(self, ctx):
        """Sai do canal de voz."""
        if ctx.voice_client:  # Verifica se o bot está em um canal de voz
            await ctx.voice_client.disconnect()
            await ctx.send("Saí do canal de voz.")
        else:
            await ctx.send("Não estou em um canal de voz!")

    @commands.command()
    async def play(self, ctx, url: str):
        """Toca uma música a partir de uma URL do YouTube."""
        try:
            # Verifica se o bot está conectado ao canal de voz
            if not ctx.voice_client:
                if ctx.author.voice:  # Verifica se o usuário está em um canal de voz
                    channel = ctx.author.voice.channel
                    await channel.connect()
                else:
                    await ctx.send("Você precisa estar em um canal de voz para eu entrar.")
                    return

            await ctx.send("Buscando a música, aguarde...")

            # Extrai informações de áudio do vídeo
            info = ytdl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2)

            # Toca a música
            ctx.voice_client.play(source)
            await ctx.send(f"Tocando agora: **{info['title']}**")

        except Exception as e:
            await ctx.send(f"Erro ao tentar reproduzir a música: {e}")

async def setup(bot):
    await bot.add_cog(Music(bot))
