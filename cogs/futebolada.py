import discord
from discord.ext import commands
import random
import json
import os

class Futebolada(commands.Cog):
    def __init__(self, client):
        self.client = client

    def load_players(self):
        if os.path.exists("players.json"):
            with open("players.json", "r") as f:
                return json.load(f)
        return {}

    def save_players(self, players):
        with open("players.json", "w") as f:
            json.dump(players, f, indent=4)

    @commands.command()
    async def player(self, ctx, *args):
        if len(args) % 2 != 0:
            await ctx.send("Por favor, forneça pares de nome e habilidade (exemplo: `Lukas bom Pedro medio`).")
            return

        guild_id = str(ctx.guild.id)
        players = self.load_players()
        if guild_id not in players:
            players[guild_id] = {}

        added_players = []
        for i in range(0, len(args), 2):
            name = args[i]
            skill = args[i + 1].lower()
            if skill not in ["bom", "medio", "mau"]:
                await ctx.send(f"Habilidade inválida para {name}: {skill}. Use 'bom', 'medio', ou 'mau'.")
                return
            players[guild_id][name] = skill
            added_players.append(f"{name} ({skill})")

        self.save_players(players)
        await ctx.send(f"Jogadores adicionados: {', '.join(added_players)}")


    @commands.command()
    async def rplayer(self, ctx, name: str):
        guild_id = str(ctx.guild.id)
        players = self.load_players()
        if guild_id in players and name in players[guild_id]:
            del players[guild_id][name]
            self.save_players(players)
            await ctx.send(f"{name} removido da lista de jogadores.")
        else:
            await ctx.send(f"{name} não encontrado na lista de jogadores.")

    @commands.command()
    async def players(self, ctx):
        guild_id = str(ctx.guild.id)
        players = self.load_players().get(guild_id, {})

        if not players:
            await ctx.send("❌ Não há jogadores registrados para este servidor.")
            return

        skill_emojis = {
            "bom": "🌟 Bom",
            "medio": "⚖️ Médio",
            "mau": "👎 Mau"
        }

        embed = discord.Embed(
            title="🏆 Lista de Jogadores",
            description="Aqui estão os jogadores registrados para este servidor.",
            color=discord.Color.blue()
        )

        for name, skill in players.items():
            embed.add_field(name=f"👤 {name}", value=skill_emojis.get(skill, skill), inline=True)

        embed.set_footer(text=f"Total de jogadores: {len(players)}")
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.timestamp = ctx.message.created_at

        await ctx.send(embed=embed)


    @commands.command()
    async def futebolada(self, ctx):
        guild_id = str(ctx.guild.id)
        players = self.load_players().get(guild_id, {})
        
        if len(players) < 4:
            await ctx.send("Por favor, adicione pelo menos 4 jogadores com habilidades.")
            return

        balanced_teams = self.balance_teams(players)
        self.randomize_teams_fully(balanced_teams, players)

        embed = discord.Embed(title="Equipas da Futebolada", color=discord.Color.green())
        embed.add_field(
            name="EQUIPA 1",
            value="\n".join([f"{player} ({players[player]})" for player in balanced_teams["team_1"]]),
            inline=True
        )
        embed.add_field(
            name="EQUIPA 2",
            value="\n".join([f"{player} ({players[player]})" for player in balanced_teams["team_2"]]),
            inline=True
        )

        await ctx.send(embed=embed)

    def balance_teams(self, players):
        good_players = [p for p, skill in players.items() if skill == "bom"]
        medium_players = [p for p, skill in players.items() if skill == "medio"]
        bad_players = [p for p, skill in players.items() if skill == "mau"]

        random.shuffle(good_players)
        random.shuffle(medium_players)
        random.shuffle(bad_players)

        team_1, team_2 = [], []

        def distribute_players_evenly(team_1, team_2, players):
            for i, player in enumerate(players):
                if len(team_1) < len(team_2):
                    team_1.append(player)
                else:
                    team_2.append(player)

        distribute_players_evenly(team_1, team_2, good_players)
        distribute_players_evenly(team_1, team_2, medium_players)
        distribute_players_evenly(team_1, team_2, bad_players)

        total_players = len(players)
        if total_players % 2 == 0:
            while len(team_1) > len(team_2):
                team_2.append(team_1.pop())
            while len(team_2) > len(team_1):
                team_1.append(team_2.pop())

        return {"team_1": team_1, "team_2": team_2}

    def randomize_teams_fully(self, teams, players):
        skill_groups = {"bom": [], "medio": [], "mau": []}

        for player in teams["team_1"]:
            skill_groups[players[player]].append(player)
        for player in teams["team_2"]:
            skill_groups[players[player]].append(player)

        for skill, grouped_players in skill_groups.items():
            random.shuffle(grouped_players)
            half = len(grouped_players) // 2
            teams["team_1"] = [p for p in teams["team_1"] if players[p] != skill]
            teams["team_2"] = [p for p in teams["team_2"] if players[p] != skill]
            teams["team_1"].extend(grouped_players[:half])
            teams["team_2"].extend(grouped_players[half:])

        total_players = len(teams["team_1"]) + len(teams["team_2"])
        if total_players % 2 == 0:
            while len(teams["team_1"]) > len(teams["team_2"]):
                teams["team_2"].append(teams["team_1"].pop())
            while len(teams["team_2"]) > len(teams["team_1"]):
                teams["team_1"].append(teams["team_2"].pop())

        random.shuffle(teams["team_1"])
        random.shuffle(teams["team_2"])

async def setup(client):
    await client.add_cog(Futebolada(client))
