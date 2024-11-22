import discord
from discord.ext import commands
from discord import File
from easy_pil import Editor, load_image_async, Font
import json
import os

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            with open('welcome_channel.json', 'r') as f:
                data = json.load(f)

            channel_id = data.get(str(member.guild.id))
            channel = member.guild.get_channel(channel_id) if channel_id else member.guild.system_channel

            if channel is None:
                print("Nenhum canal configurado ou system channel não definido.")
                return

            background = Editor("pic2.jpg")
            avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

            profile_image = await load_image_async(str(avatar_url))
            profile = Editor(profile_image).resize((150, 150)).circle_image()

            poppins = Font.poppins(size=50, variant="bold")
            poppins_small = Font.poppins(size=20, variant="light")

            background.paste(profile, (325, 90))
            background.ellipse((325, 90), 150, 150, outline="white", stroke_width=5)

            background.text((400, 260), f"BEM-VINDO AO {member.guild.name}", color="white", font=poppins, align="center")
            background.text((400, 325), f"{member.name}#{member.discriminator}", color="white", font=poppins_small, align="center")

            file = File(fp=background.image_bytes, filename="welcome.jpg")

            await channel.send(f"OLÁ! {member.mention}! BEM-VINDO ao **{member.guild.name}**. Para mais informações vai a #rules.")
            await channel.send(file=file)
            
        except Exception as e:
            print(f"An error occurred: {e}")

    @commands.command(name='setwelcome')
    @commands.has_permissions(administrator=True)
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        with open('welcome_channel.json', 'r') as f:
            data = json.load(f)

        data[str(ctx.guild.id)] = channel.id

        with open('welcome_channel.json', 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"O canal de boas-vindas foi configurado para {channel.mention}.")

    @set_welcome_channel.error
    async def set_welcome_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Apenas administradores podem usar este comando.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Por favor, menciona um canal válido.")

async def setup(bot):
    await bot.add_cog(Welcome(bot))

if not os.path.exists('welcome_channel.json'):
    with open('welcome_channel.json', 'w') as f:
        json.dump({}, f, indent=4)
