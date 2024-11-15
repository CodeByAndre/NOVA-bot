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

    async def clear_state(self):
        self.queue.clear()
        self.is_playing = False
        self.current_ctx = None
        self.now_playing_message = None

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.client.user and before.channel is not None and after.channel is None:
            if self.current_ctx:
                try:
                    await self.current_ctx.send("O bot foi desconectado do canal.", delete_after=5)
                except Exception as e:
                    print(f"Error sending disconnect message: {e}")
            await self.clear_state()

    async def fetch_audio_url(self, query):
        try:
            is_url = query.startswith("http")
            search_query = query if is_url else f"ytsearch:{query}"

            with ytdl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(search_query, download=False)
                if not is_url:
                    info = info['entries'][0]
                audio_url = next((format['url'] for format in info['formats'] if format.get('acodec') != 'none'), None)
                
                if audio_url:
                    return audio_url, info
        except Exception as e:
            print(f"Error fetching audio URL: {e}")
            return None, None

    async def play_song(self, ctx, query):
        search_msg = await ctx.send("A procura da música, aguarde...")
        audio_url, info = await self.fetch_audio_url(query)

        if audio_url and info:
            audio_source = FFmpegPCMAudio(audio_url, **ffmpeg_opts)
            ctx.voice_client.play(audio_source, after=self.after_play)

            self.current_ctx = ctx
            await search_msg.delete()

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
            await ctx.send("Precisas de estar em um canal de voz!", delete_after=5)
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
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Música pulada.", delete_after=5)
        else:
            await ctx.send("Não há música a tocar no momento.", delete_after=5)
        await ctx.message.delete()

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            await ctx.send("Música parada e desconectado do canal de voz.", delete_after=5)
        else:
            await ctx.send("O bot não está a tocar música.", delete_after=5)
        await ctx.message.delete()

    @commands.command()
    async def pause(self, ctx):
        """Pausa a música atual."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("A música foi pausada.", delete_after=5)
        else:
            await ctx.send("Não há música a tocar no momento para pausar.", delete_after=5)
        await ctx.message.delete()

    @commands.command()
    async def resume(self, ctx):
        """Resume a música pausada."""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("A música foi retomada.", delete_after=5)
        else:
            await ctx.send("Não há música pausadas no momento.", delete_after=5)
        await ctx.message.delete()

async def setup(client):
    await client.add_cog(Music(client))
