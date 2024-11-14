from openai import AsyncOpenAI
import os
from discord.ext import commands
from discord import Embed

client_openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Gerar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def txt(self, ctx, *, prompt: str):
        try:
            response = await client_openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content.strip()
            await ctx.send(content)
        except Exception as e:
            await ctx.send(f"Erro ao gerar conteúdo: {e}")

    @commands.command()
    async def img(self, ctx, *, prompt: str):
        try:
            warning_msg = await ctx.send("🔄 A imagem está sendo gerada. Isso pode levar alguns segundos!")

            response = await client_openai.images.generate(
                prompt=prompt,
                size="1024x1024"
            )

            image_url = response.data[0].url

            embed = Embed(
                title="Aqui está sua imagem!",
                description=f"Prompt: {prompt}",
                color=0x00ff00
            )
            embed.set_image(url=image_url)
            embed.set_footer(text="Imagem gerada por: NovaBot") 

            await warning_msg.delete()
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Erro ao gerar a imagem: {e}")

async def setup(client):
    await client.add_cog(Gerar(client))
