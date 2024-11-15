import discord
from discord.ext import commands
from discord import app_commands
import json

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        client.remove_command("help")

    @commands.command()
    async def help(self, ctx):
        await self.send_help(ctx)

    @app_commands.command(name="help", description="Get a list of all available commands.")
    async def slash_help(self, interaction: discord.Interaction):
        await self.send_help(interaction)

    async def send_help(self, target):
        try:
            with open("prefix.json", "r") as f:
                data = json.load(f)
                guild_prefix = data.get(str(target.guild.id), "!")
        except (FileNotFoundError, json.JSONDecodeError):
            guild_prefix = "!"

        embed = discord.Embed(
            title="Bot Commands Help",
            description="Lista de comandos organizados por categoria.",
            color=discord.Color.blue()
        )

        embed.add_field(
            name=":musical_note: | Music",
            value="`play`, `add`, `skip`, `pause`, `resume`, `stop`, `queue`\nStatus: Available",
            inline=False
        )

        embed.add_field(
            name=":game_die: | Games",
            value=(
                "`galo` - Inicia o jogo\n"
                "  ↳ `colocar` - Faz uma jogada (use após `galo`)\n"
                "`futebolada` - Cria equipes\n"
                "  ↳ `player` - Adiciona jogador\n"
                "  ↳ `rplayer` - Remove jogador\n"
                "  ↳ `players` - Lista jogadores"
            ),
            inline=False
        )

        embed.add_field(
            name=":hammer: | Utility",
            value="`latency`, `avatar`, `translate`, `txt`, `img`\nStatus: Available",
            inline=False
        )

        embed.set_footer(text=f"Bot Prefix: {guild_prefix}")

        if isinstance(target, discord.Interaction):
            await target.response.send_message(embed=embed)
        else:
            await target.send(embed=embed)

async def setup(client):
    await client.add_cog(Help(client))
