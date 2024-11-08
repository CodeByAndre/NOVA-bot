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

    async def fetch_audio_url(self, query):
        try:
            # Check if the query is a URL
            is_url = query.startswith("http")
            search_query = query if is_url else f"ytsearch:{query}"

            with ytdl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(search_query, download=False)
                if not is_url:
                    info = info['entries'][0]  # Get the first result from ytsearch
                audio_url = next((format['url'] for format in info['formats'] if format.get('acodec') != 'none'), None)
                
                if audio_url:
                    return audio_url, info
        except Exception as e:
            print(f"Error fetching audio URL: {e}")
            return None, None

    async def play_song(self, ctx, query):
        search_msg = await ctx.send("Buscando a música, aguarde...")
        audio_url, info = await self.fetch_audio_url(query)

        if audio_url and info:
            audio_source = FFmpegPCMAudio(audio_url, **ffmpeg_opts)
            ctx.voice_client.play(audio_source, after=self.after_play)

            self.current_ctx = ctx
            await search_msg.delete()

            # Create Now Playing embed
            embed = discord.Embed(
                title="Now Playing", 
                description=info['title'], 
                color=discord.Color.blue()
            )
            embed.add_field(name="Duração", value=info['duration'], inline=True)
            embed.add_field(name="URL", value=f"[Clique aqui para assistir]({info['webpage_url']})", inline=True)
            if 'thumbnail' in info:
                embed.set_thumbnail(url=info['thumbnail'])

            if self.now_playing_message:
                await self.now_playing_message.edit(embed=embed)
            else:
                self.now_playing_message = await ctx.send(embed=embed)
        else:
            await ctx.send("Não foi possível encontrar a música.", delete_after=5)
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
    async def play(self, ctx, *, query: str):
        """Play a song using a URL or search query."""
        if not ctx.author.voice:
            await ctx.send("Você precisa estar em um canal de voz!", delete_after=5)
            return

        voice_channel = ctx.author.voice.channel

        if not ctx.voice_client:
            await voice_channel.connect()

        if not self.is_playing:
            self.is_playing = True
            await self.play_song(ctx, query)
            await ctx.message.delete()
        else:
            self.queue.append(query)
            embed = discord.Embed(
                title="Música adicionada à fila", 
                description=f"[Clique aqui para ouvir]({query})", 
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)
            await ctx.message.delete()

    @commands.command()
    async def add(self, ctx, *, query: str):
        """Add a song to the queue using a URL or search query."""
        audio_url, info = await self.fetch_audio_url(query)
        if audio_url and info:
            self.queue.append(query)
            embed = discord.Embed(
                title="Música adicionada à fila", 
                description=f"[{info['title']}]({info['webpage_url']})", 
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed, delete_after=7)
        else:
            await ctx.send("Não foi possível adicionar a música.", delete_after=5)
        await ctx.message.delete()

    @commands.command()
    async def queue(self, ctx):
        """Display the current music queue."""
        if not self.queue:
            await ctx.send("A fila está vazia.", delete_after=5)
        else:
            embed = discord.Embed(title="Fila de músicas", color=discord.Color.green())
            for i, query in enumerate(self.queue, start=1):
                _, info = await self.fetch_audio_url(query)
                embed.add_field(name=f"{i}. {info['title']}", value=f"[Ouvir aqui]({info['webpage_url']})", inline=False)
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

    @commands.command()
    async def stop(self, ctx):
        """Stop the current song and disconnect from the voice channel."""
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            await ctx.send("Música parada e desconectado do canal de voz.", delete_after=5)
        else:
            await ctx.send("O bot não está tocando música.", delete_after=5)
        await ctx.message.delete()

    @commands.command()
    async def leave(self, ctx):
        """Disconnect from the voice channel."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Desconectado do canal de voz.")
        else:
            await ctx.send("O bot não está em nenhum canal de voz.")
        await ctx.message.delete()

async def setup(client):
    await client.add_cog(Music(client))
