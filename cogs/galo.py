import discord
from discord.ext import commands
import random
import asyncio

class TicTacToe(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reset_game()

    def reset_game(self):
        self.player1 = None
        self.player2 = None
        self.turn = ""
        self.gameOver = True
        self.first_embed = None
        self.board = [":white_large_square:"] * 9
        self.count = 0
        self.winningConditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]
        ]
        self.first_time = True
        self.last_game_board_message = None  # Store the last game board message

    @commands.command()
    async def galo(self, ctx, p2: discord.Member):
        if self.gameOver:
            self.reset_game()

            self.player1 = ctx.author
            self.player2 = p2
            self.turn = random.choice([self.player1, self.player2])

            # Send the initial game board
            await self.display_board(ctx)

            embed = discord.Embed(
                description=f"É a tua vez <@{self.turn.id}>",
                colour=discord.Color.random()
            )
            emb = await ctx.send(embed=embed)
            self.first_embed = emb

        else:
            embed = discord.Embed(
                description="Um jogo já está a ser processado. Acabe-o para começar um novo.",
                colour=discord.Color.random()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def colocar(self, ctx, pos: int):
        if not self.gameOver:
            embed = discord.Embed(
                description="Começa um novo jogo digitando `$galo`.",
                colour=discord.Color.random()
            )
            await ctx.send(embed=embed)
            return

        if ctx.author not in [self.player1, self.player2]:
            embed = discord.Embed(
                description="Não estás a participar do jogo.",
                colour=discord.Color.random()
            )
            await ctx.send(embed=embed)
            return

        if self.turn != ctx.author:
            embed = discord.Embed(
                description="Não é a tua vez.",
                colour=discord.Color.random()
            )
            await ctx.send(embed=embed)
            return

        if 0 < pos < 10 and self.board[pos - 1] == ":white_large_square:":
            mark = ":regional_indicator_x:" if self.turn == self.player1 else ":o2:"
            self.board[pos - 1] = mark
            self.count += 1

            if self.first_time:
                await self.first_embed.delete()
                self.first_time = False

            # Delete the user's message before updating the board
            await ctx.message.delete()

            # Delete the last game board message if it exists
            if self.last_game_board_message:
                await self.last_game_board_message.delete()

            # Send the updated game board
            await self.display_board(ctx)

            if self.check_winner(mark):
                embed = discord.Embed(
                    description=f"{self.turn.mention} GANHOU!",
                    colour=discord.Color.random()
                )
                await ctx.send(embed=embed, delete_after=10)
                await asyncio.sleep(10)
                self.gameOver = True
                return

            if self.count >= 9:
                embed = discord.Embed(
                    description="É um empate!",
                    colour=discord.Color.random()
                )
                await ctx.send(embed=embed, delete_after=10)
                await asyncio.sleep(10)
                self.gameOver = True
                return

            # Switch turns
            self.turn = self.player1 if self.turn == self.player2 else self.player2
            await self.send_turn_message(ctx)

        else:
            embed = discord.Embed(
                description="Escolhe um número de 1 a 9 que não esteja a ser utilizado.",
                colour=discord.Color.random()
            )
            await ctx.send(embed=embed)

    async def display_board(self, ctx):
        # Create the board message as a string
        board_str = ""
        for i in range(9):
            board_str += self.board[i]
            if i % 3 == 2:
                board_str += "\n"  # Break into new line every 3 items
        
        # Send the board message and store it
        game_board_message = await ctx.send(board_str)
        self.last_game_board_message = game_board_message  # Store the last game board message

    async def send_turn_message(self, ctx):
        embed = discord.Embed(
            description=f"É a tua vez <@{self.turn.id}>",
            colour=discord.Color.random()
        )
        await ctx.send(embed=embed, delete_after=3)

    def check_winner(self, mark):
        for condition in self.winningConditions:
            if self.board[condition[0]] == mark and self.board[condition[1]] == mark and self.board[condition[2]] == mark:
                return True
        return False

    @galo.error
    async def galo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description="Menciona 1 pessoa para jogar.",
                colour=discord.Color.random()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                description="Tens a certeza que mencionaste alguém?",
                colour=discord.Color.random()
            )
            await ctx.send(embed=embed)

    @colocar.error
    async def colocar_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description="Coloca o número da posição que queres marcar.",
                colour=discord.Color.random()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                description="Está mal escrito.",
                colour=discord.Color.random()
            )
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(TicTacToe(client))
