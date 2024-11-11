import discord
from discord.ext import commands
import random

class Futebolada(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def futebolada(self, ctx, *args):
        if len(args) < 4 or len(args) % 2 != 0:
            await ctx.send("Por favor, forneça nomes e habilidades (exemplo: `bom medio mao`).")
            return

        players = {}
        for i in range(0, len(args), 2):
            name = args[i]
            skill = args[i + 1].lower()
            if skill not in ["bom", "medio", "mao"]:
                await ctx.send(f"Habilidade inválida para {name}: {skill}. Use 'bom', 'medio', ou 'mao'.")
                return
            players[name] = skill

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
        bad_players = [p for p, skill in players.items() if skill == "mao"]

        team_1, team_2 = [], []

        def distribute_players(team_1, team_2, players):
            for i, player in enumerate(players):
                if i % 2 == 0:
                    team_1.append(player)
                else:
                    team_2.append(player)

        distribute_players(team_1, team_2, good_players)
        distribute_players(team_1, team_2, medium_players)
        distribute_players(team_1, team_2, bad_players)

        return {"team_1": team_1, "team_2": team_2}

    def randomize_teams_fully(self, teams, players):
        skill_groups = {"bom": [], "medio": [], "mao": []}

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

        random.shuffle(teams["team_1"])
        random.shuffle(teams["team_2"])

async def setup(client):
    await client.add_cog(Futebolada(client))
