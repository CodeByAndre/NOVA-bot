import discord
from discord.ext import commands
import yt_dlp as ytdl
from discord import FFmpegPCMAudio
import asyncio

ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -acodec pcm_s16le -ar 48000 -ac 2'
}

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'noplaylist': True,
    'keepvideo': False,
    'postprocessors': []
}

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []
        self.is_playing = False
        self.current_ctx = None
        self.now_playing_message = None

    async def play_song(self, ctx, url):
        search_msg = await ctx.send("Buscando a música, aguarde...")

        try:
            with ytdl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                audio_url = None
                for format in info['formats']:
                    if format.get('acodec') != 'none':
                        audio_url = format['url']
                        break

                if not audio_url:
                    await ctx.send("Não foi possível encontrar um stream de áudio.", delete_after=3)
                    return

                audio_source = FFmpegPCMAudio(audio_url, **ffmpeg_opts)
                ctx.voice_client.play(audio_source, after=self.after_play)

                self.current_ctx = ctx

                await search_msg.delete()

                thumbnail_url = info.get('thumbnail', None)

                embed = discord.Embed(title="Now Playing", description=info['title'], color=discord.Color.blue())
                embed.add_field(name="Duração", value=info['duration'], inline=True)
                embed.add_field(name="URL", value=f"[Clique aqui]({url})", inline=True)

                if thumbnail_url:
                    embed.set_thumbnail(url=thumbnail_url)

                if self.now_playing_message:
                    await self.now_playing_message.edit(embed=embed)
                else:
                    self.now_playing_message = await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Erro ao tentar reproduzir a música: {str(e)}", delete_after=3)
            await ctx.voice_client.disconnect()

    def after_play(self, e):
        if self.current_ctx:
            asyncio.run_coroutine_threadsafe(self.handle_song_end(self.current_ctx), self.client.loop)

    async def handle_song_end(self, ctx):
        if len(self.queue) > 0:
            next_song = self.queue.pop(0)
            await self.play_song(ctx, next_song)
        else:
            await ctx.voice_client.disconnect()
            self.is_playing = False
            await ctx.send("A fila de músicas acabou. Desconectando...", delete_after=3)

    @commands.command()
    async def leave(self, ctx):
        """Disconnect from the voice channel."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Desconectado do canal de voz.")
        else:
            await ctx.send("O bot não está em nenhum canal de voz.")
        await ctx.message.delete()

    @commands.command()
    async def play(self, ctx, url: str):
        """Play a song."""
        if not ctx.author.voice:
            await ctx.send("Você precisa estar em um canal de voz!", delete_after=5)
            return

        voice_channel = ctx.author.voice.channel

        if not ctx.voice_client:
            await voice_channel.connect()

        if not self.is_playing:
            self.is_playing = True
            await self.play_song(ctx, url)

            await ctx.message.delete()
        else:
            self.queue.append(url)
            embed = discord.Embed(title="Música adicionada à fila", description=f"[Clique aqui para ouvir]({url})", color=discord.Color.purple())
            await ctx.send(embed=embed)

            await ctx.message.delete()

    @commands.command()
    async def pause(self, ctx):
        """Pause the current song."""
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Música pausada.", delete_after=3)
        else:
            await ctx.send("Nenhuma música está sendo tocada.", delete_after=3)
        await ctx.message.delete()

    @commands.command()
    async def resume(self, ctx):
        """Resume the paused song."""
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Música retomada.", delete_after=3)
        else:
            await ctx.send("A música não foi pausada.", delete_after=4)
        await ctx.message.delete()

    @commands.command()
    async def stop(self, ctx):
        """Stop the current song."""
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            await ctx.send("Música parada e desconectado do canal de voz.", delete_after=5)
        else:
            await ctx.send("O bot não está tocando música.", delete_after=5)
        await ctx.message.delete()

    @commands.command()
    async def add(self, ctx, url: str):
        """Add a song to the queue."""
        self.queue.append(url)
        embed = discord.Embed(title="Música adicionada à fila", description=f"[Clique aqui para ouvir]({url})", color=discord.Color.purple())
        await ctx.send(embed=embed, delete_after=7)
        await ctx.message.delete()

    @commands.command()
    async def queue(self, ctx):
        """Display the current music queue."""
        if not self.queue:
            await ctx.send("A fila está vazia.", delete_after=5)
        else:
            embed = discord.Embed(title="Fila de músicas", color=discord.Color.green())
            for i, url in enumerate(self.queue, start=1):
                with ytdl.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info['title']
                embed.add_field(name=f"{i}. {title}", value=f"[Ouvir aqui]({url})", inline=False)
            await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    async def skip(self, ctx):
        """Skip the current song."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Música pulada.", delete_after=5)
        else:
            await ctx.send("Não há música tocando no momento.", delete_after=5)
        await ctx.message.delete()

async def setup(client):
    await client.add_cog(Music(client))
