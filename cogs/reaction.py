import discord
from discord.ext import commands

class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="react")
    async def react(self, ctx, message_text: str, emoji: str, role: discord.Role):
        embed = discord.Embed(
            title="ADICIONAR CARGO",
            description=f"{message_text} ({role.mention})",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Reage para teres acesso ao servidor!")

        message = await ctx.send(embed=embed)

        await message.add_reaction(emoji)

        await ctx.message.delete()

        @self.bot.event
        async def on_reaction_add(reaction, user):
            if reaction.message.id == message.id and str(reaction.emoji) == emoji:
                await user.add_roles(role)

        @self.bot.event
        async def on_reaction_remove(reaction, user):
            if reaction.message.id == message.id and str(reaction.emoji) == emoji:
                await user.remove_roles(role)

async def setup(bot):
    await bot.add_cog(ReactionRole(bot))
