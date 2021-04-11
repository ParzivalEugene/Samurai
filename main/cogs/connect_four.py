import discord
from discord.ext import commands
from cogs.config import *
import random


class ConnectFour(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player1 = ""
        self.player2 = ""
        self.turn = ""
        self.game_over = True
        self.board = []
        self.count = 0
        self.icons = {
            "cell": ":white_large_square:",
            "ball_1": ":blue_square:",
            "ball_2": ":yellow_square:"
        }
        self.board_size = {
                "height": 6,
                "length": 7
        }

    @commands.command(name="c4_rules")
    async def connect_four_place_rules(self, ctx):
        embed = discord.Embed(
            title="Информация о **4 в ряд**",
            description=f'{self.icons["ball_1"]} {self.icons["ball_2"]}',
            colour=discord.Colour.purple()
        )
        embed.add_field(name="Команды",
                        value=f"""**{prefix}с4 <member1> <member2>** - начало игры игры в 4 в ряд с указанием игроков.
        **{prefix}c4_place <number>** - команда для установки броска фишки в нужный столбик (число от 1 до {self.board_size["length"]})
    Полем является доска 6х7.
        __Все команды вводятся **латинскими буквами**__""",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="c4")
    async def connect_four(self, ctx, p1: discord.Member, p2: discord.Member):
        if self.game_over:
            if p1 == self.bot.user or p2 == self.bot.user:
                await ctx.send("К сожалению я не могу с вами играть")
                return
            self.board = [[self.icons["cell"] for _ in range(self.board_size["length"])] for _ in range(self.board_size["height"])]
            self.game_over = False
            self.count = 0
            self.player1 = p1
            self.player2 = p2

            for line in self.board:
                await ctx.send(" ".join(line))

            num = random.choice((1, 2))
            if num == 1:
                self.turn = self.player1
                await ctx.send("Сейчас ходит <@" + str(self.player1.id) + ">")
            elif num == 2:
                self.turn = self.player2
                await ctx.send("Сейчас ходит <@" + str(self.player2.id) + ">")
        else:
            await ctx.send("Игра в прогрессе. Завершите текущую, затем начните новую.")

    @commands.command(name="c4_place")
    async def connect_four_place(self, ctx, pos: int):
        if not self.game_over:
            if self.turn == ctx.author:
                mark = self.icons["ball_1"] if self.turn == self.player2 else self.icons["ball_2"]
                if 0 < pos < self.board_size["length"]:
                    if any(self.board[i][pos - 1] == self.icons["cell"] for i in range(self.board_size["height"])):
                        position = 5
                        while self.board[position][pos - 1] != self.icons["cell"]:
                            position -= 1
                        self.board[position][pos - 1] = mark
                        self.count += 1

                        for line in self.board:
                            await ctx.send(" ".join(line))

                        self.connect_four_check_winner(mark)
                        if self.game_over:
                            embed = discord.Embed(
                                title=f"Победа {mark} :exclamation:",
                                colour=discord.Colour.purple()
                            )
                            await ctx.send(embed=embed)
                        elif self.count >= 42:
                            self.game_over = True
                            embed = discord.Embed(
                                title="Ничья :exclamation:",
                                colour=discord.Colour.purple()
                            )
                            await ctx.send(embed=embed)
                        self.turn = self.player1 if self.turn == self.player2 else self.player2
                    else:
                        await ctx.send("Ряд уже переполнен")
                else:
                    await ctx.send("Неверный столбец")
            else:
                await ctx.send("Сейчас не ваш ход")
        else:
            await ctx.send(f"Начните новую игру используя комнду {prefix}с4")

    def connect_four_check_winner(self, mark):
        col, row = len(self.board[0]), len(self.board)
        columns = [[] for _ in range(col)]
        rows = [[] for _ in range(row)]
        left_diagonals = [[] for _ in range(row + col - 1)]
        right_diagonals = [[] for _ in range(len(left_diagonals))]
        k = 1 - row

        for x in range(col):
            for y in range(row):
                columns[x].append(self.board[y][x])
                rows[y].append(self.board[y][x])
                left_diagonals[x + y].append(self.board[y][x])
                right_diagonals[x - y - k].append(self.board[y][x])
        left_diagonals = left_diagonals[3:-3]
        right_diagonals = right_diagonals[3:-3]
        for lines in [columns, rows, right_diagonals, left_diagonals]:
            for line in lines:
                if mark * 4 in "".join(line):
                    self.game_over = True
                    return

    @connect_four.error
    async def connect_four_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Необходимо два игрока")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Убедитесь что вы указали участника.")

    @connect_four_place.error
    async def connect_four_place_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Вы не указали позицию")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Вы ввели не число")
