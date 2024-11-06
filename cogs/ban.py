import discord
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)  
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.guild.me.guild_permissions.ban_members:
            await member.ban(reason=reason)
            await ctx.send(f"{member} foi banido/a do servidor. Rasao: {reason if reason else 'Sem rasao.'}")
        else:
            await ctx.send("Eu não tenho permissões para banir membros.")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Não tens permissões para usar este comando.")

async def setup(client):
    await client.add_cog(Ban(client))
