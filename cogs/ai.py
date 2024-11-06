from openai import AsyncOpenAI
import os
from discord.ext import commands

# Initialize the OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
client_openai = AsyncOpenAI(api_key=openai_api_key)

class Gerar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def gerar(self, ctx, *, prompt: str):
        try:
            # Check if the user wants an image or text generation
            if "image:" in prompt.lower():
                # Remove "image:" from the prompt
                image_prompt = prompt.replace("image:", "").strip()

                # Generate an image with DALL-E
                response = await client_openai.images.generate(
                    prompt=image_prompt,
                    size="1024x1024"  # You can adjust the size if needed
                )

                # Get the URL of the generated image
                image_url = response['data'][0]['url']
                await ctx.send(f"Here's the image you requested: {image_url}")

            else:
                # Generate text if the prompt does not specify "image:"
                response = await client_openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )

                content = response.choices[0].message['content'].strip()
                await ctx.send(content)

        except Exception as e:
            await ctx.send(f"Erro ao gerar conteúdo: {e}")

async def setup(client):
    await client.add_cog(Gerar(client))
