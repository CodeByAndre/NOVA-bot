import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class FilmesESeries(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def filme(self, ctx, *, nome):
        # Obter a chave da API a partir da variável de ambiente
        api_key = os.getenv("TMDB_API_KEY")
        
        if not api_key:
            await ctx.send("Chave de API do TMDb não encontrada. Verifique o arquivo .env.")
            return

        # Buscar informações sobre o filme no TMDb
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={nome}"
        response = requests.get(search_url)

        if response.status_code != 200:
            await ctx.send(f"Erro ao buscar filme: {response.status_code}")
            return

        data = response.json()
        
        if data["results"]:
            # Pega o primeiro resultado da busca
            movie_id = data["results"][0]["id"]

            # Obter detalhes sobre o filme
            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
            details_response = requests.get(details_url)
            
            if details_response.status_code != 200:
                await ctx.send(f"Erro ao buscar detalhes do filme: {details_response.status_code}")
                return

            details = details_response.json()

            # Criar o Embed
            embed = discord.Embed(title=details["title"], color=discord.Color.blue())
            embed.set_thumbnail(url=f"https://image.tmdb.org/t/p/w500{details['poster_path']}")

            # Adicionando informações ao embed
            embed.add_field(name="Ano", value=details["release_date"].split("-")[0], inline=True)
            embed.add_field(name="Gênero", value=", ".join([genre["name"] for genre in details["genres"]]), inline=True)
            embed.add_field(name="Classificação IMDb", value=details["vote_average"], inline=True)
            embed.add_field(name="Duração", value=f"{details['runtime']} minutos", inline=True)

            # Onde assistir
            watch_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={api_key}"
            watch_response = requests.get(watch_url)
            
            if watch_response.status_code != 200:
                await ctx.send(f"Erro ao buscar plataformas: {watch_response.status_code}")
                return

            watch_data = watch_response.json()

            if "results" in watch_data and "US" in watch_data["results"]:
                platforms = watch_data["results"]["US"].get("flatrate", [])
                if platforms:
                    platform_names = [platform["provider_name"] for platform in platforms]
                    embed.add_field(name="Onde Assistir", value=", ".join(platform_names), inline=False)
                else:
                    embed.add_field(name="Onde Assistir", value="Não encontrado.", inline=False)
            else:
                embed.add_field(name="Onde Assistir", value="Não disponível ou informação não encontrada.", inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Não encontrei informações sobre o filme '{nome}'. Tente usar o nome completo ou em inglês.")

    @commands.command()
    async def serie(self, ctx, *, nome):
        # Obter a chave da API a partir da variável de ambiente
        api_key = os.getenv("TMDB_API_KEY")
        
        if not api_key:
            await ctx.send("Chave de API do TMDb não encontrada. Verifique o arquivo .env.")
            return

        # Buscar informações sobre a série no TMDb
        search_url = f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={nome}"
        response = requests.get(search_url)

        if response.status_code != 200:
            await ctx.send(f"Erro ao buscar série: {response.status_code}")
            return

        data = response.json()

        if data["results"]:
            # Pega o primeiro resultado da busca
            series_id = data["results"][0]["id"]

            # Obter detalhes sobre a série
            details_url = f"https://api.themoviedb.org/3/tv/{series_id}?api_key={api_key}"
            details_response = requests.get(details_url)
            
            if details_response.status_code != 200:
                await ctx.send(f"Erro ao buscar detalhes da série: {details_response.status_code}")
                return

            details = details_response.json()

            # Criar o Embed
            embed = discord.Embed(title=details["name"], color=discord.Color.green())
            embed.set_thumbnail(url=f"https://image.tmdb.org/t/p/w500{details['poster_path']}")

            # Adicionando informações ao embed
            embed.add_field(name="Ano", value=details["first_air_date"].split("-")[0], inline=True)
            embed.add_field(name="Gênero", value=", ".join([genre["name"] for genre in details["genres"]]), inline=True)
            embed.add_field(name="Classificação IMDb", value=details["vote_average"], inline=True)
            embed.add_field(name="Duração", value=f"{details['episode_run_time'][0]} minutos por episódio", inline=True)

            # Onde assistir
            watch_url = f"https://api.themoviedb.org/3/tv/{series_id}/watch/providers?api_key={api_key}"
            watch_response = requests.get(watch_url)
            
            if watch_response.status_code != 200:
                await ctx.send(f"Erro ao buscar plataformas: {watch_response.status_code}")
                return

            watch_data = watch_response.json()

            if "results" in watch_data and "US" in watch_data["results"]:
                platforms = watch_data["results"]["US"].get("flatrate", [])
                if platforms:
                    platform_names = [platform["provider_name"] for platform in platforms]
                    embed.add_field(name="Onde Assistir", value=", ".join(platform_names), inline=False)
                else:
                    embed.add_field(name="Onde Assistir", value="Não encontrado.", inline=False)
            else:
                embed.add_field(name="Onde Assistir", value="Não disponível ou informação não encontrada.", inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Não encontrei informações sobre a série '{nome}'. Tente usar o nome completo ou em inglês.")

async def setup(client):
    await client.add_cog(FilmesESeries(client))
