import discord
from discord.ext import commands
import json

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        client.remove_command("help")

    @commands.command()
    async def help(self, ctx):
        try:
            with open("prefix.json", "r") as f:
                data = json.load(f)
                guild_prefix = data.get(str(ctx.guild.id), "!")
        except FileNotFoundError:
            guild_prefix = "!"
        except json.JSONDecodeError:
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
            name=":hammer: | Utility",
            value="`Latency`, `Avatar`, `Translate`\nStatus: Available",
            inline=False
        )
        embed.add_field(
            name=":game_die: | Games",
            value="`galo`, `colocar` , `futebolada`\nStatus: Available",
            inline=False
        )
        embed.set_footer(text=f"Bot Prefix: {guild_prefix}")

        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Help(client))
