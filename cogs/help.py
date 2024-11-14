import discord
from discord.ext import commands
from discord import app_commands
import json

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="help", description="Get a list of all available commands.")
    async def slash_help(self, interaction: discord.Interaction):
        await self.send_help(interaction)

    async def send_help(self, interaction: discord.Interaction):
        try:
            with open("prefix.json", "r") as f:
                data = json.load(f)
                guild_prefix = data.get(str(interaction.guild.id), "!")
        except (FileNotFoundError, json.JSONDecodeError):
            guild_prefix = "!"

        embed = discord.Embed(
            title="Bot Commands Help",
            description="Lista de comandos organizados por categoria.",
            color=discord.Color.blue()
        )

        embed.add_field(
            name=":musical_note: | Music",
            value="`play`, `pause`, `resume`, `stop`, `skip`, `queue`, `add`, `leave`\nStatus: Available",
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

        await interaction.response.send_message(embed=embed)

    async def cog_load(self):
        self.client.tree.add_command(self.slash_help)

async def setup(client):
    await client.add_cog(Help(client))
