import discord
from discord.ext import commands
from deep_translator import GoogleTranslator

class Translate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def translate(self, ctx, lang: str, *, text: str):
        try:
            translated = GoogleTranslator(source='auto', target=lang).translate(text)
            await ctx.send(f"Tradução ({lang}): {translated}")
        except Exception as e:
            await ctx.send("Desculpa, ocorreu um erro ao tentar traduzir a frase. Verifique o código do idioma e tente novamente.")

    @translate.error
    async def translate_error(self, ctx, error):
        await ctx.send("Formato do comando incorreto. Use: `translate <código_do_idioma> <texto>`")

async def setup(client):
    await client.add_cog(Translate(client))
