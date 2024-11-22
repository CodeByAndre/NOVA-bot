import discord
from discord.ext import commands

class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reaction_roles = {}

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

        self.reaction_roles[message.id] = (emoji, role)

        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        message_id = reaction.message.id
        if message_id in self.reaction_roles:
            emoji, role = self.reaction_roles[message_id]
            if str(reaction.emoji) == emoji:
                guild = reaction.message.guild
                member = guild.get_member(user.id)
                if member:
                    await member.add_roles(role)
                    await reaction.message.channel.send(
                        f"{user.mention} foi adicionado ao cargo {role.name}.",
                        delete_after=5
                    )

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return

        message_id = reaction.message.id
        if message_id in self.reaction_roles:
            emoji, role = self.reaction_roles[message_id]
            if str(reaction.emoji) == emoji:
                guild = reaction.message.guild
                member = guild.get_member(user.id)
                if member:
                    await member.remove_roles(role)
                    await reaction.message.channel.send(
                        f"{user.mention} foi removido do cargo {role.name}.",
                        delete_after=5
                    )

async def setup(bot):
    await bot.add_cog(ReactionRole(bot))