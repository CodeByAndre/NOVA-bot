import discord
from discord.ext import commands

class Cmd(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def cmd(self, ctx):
        embed = discord.Embed(title="Bot Commands Page", color=discord.Color.blue())
        embed.add_field(
            name=":shield: | Moderation",
            value=(
                "`Ban`\n"
                "`Kick`\n"
                "`Unban`\n"
                "`Clean`\n"
                "Status: Available"
            ),
            inline=True
        )
        embed.add_field(
            name=":hammer: | Utility",
            value=(
                "`Latency`\n"
                "`Prefix`\n"
                "`Reboot`\n"
                "`Avatar`\n"
                "Status: Available"
            ),
            inline=True
        )
        embed.set_footer(text="Bot Prefix is customizable, use -prefix <new_prefix>")

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Cmd(client))