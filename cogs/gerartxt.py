from openai import AsyncOpenAI
import os
from discord.ext import commands

client_openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Gerar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def gerar(self, ctx, *, prompt: str):
        try:
            response = await client_openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.choices[0].message.content.strip()
            await ctx.send(content)

        except Exception as e:
            await ctx.send(f"Erro ao gerar conteúdo: {e}")

async def setup(client):
    await client.add_cog(Gerar(client))
