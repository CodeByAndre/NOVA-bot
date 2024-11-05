import discord
from discord.ext import commands
import os
import time

class Reboot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reboot(self, ctx):
        confirmation_msg = await ctx.send("Rebooting...")

        await ctx.message.delete()

        with open("reboot_flag.txt", "w") as f:
            f.write(str(confirmation_msg.id))
        
        await self.client.close()
        time.sleep(0.2)
        os.system("python main.py")

    @reboot.error
    async def reboot_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Parece que não tens permissões.", delete_after=5)
            await ctx.message.delete()

async def setup(client):
    await client.add_cog(Reboot(client))
