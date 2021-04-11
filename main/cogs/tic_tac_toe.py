import discord
from discord.ext import commands
from cogs.config import *
import random


class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.player1 = ""
        self.player2 = ""
        self.turn = ""
        self.game_over = True
        self.board = []
        self.count = 0
        self.winning_conditions = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]
        self.bot = bot

    @commands.command(name="xo_rules")
    async def tic_tac_toe_rules(self, ctx):
        embed = discord.Embed(
            title="Информация о **крестиках-ноликах**",
            description=":negative_squared_cross_mark: :o2:",
            colour=discord.Colour.purple()
        )
        embed.add_field(name="Команды",
                        value=f"""**{prefix}xo <member1> <member2>** - начало игры игры в крестики-нолики с указанием игроков.
    **{prefix}xo_place <number>** - команда для установки Х или О в нужное место (число от 1 до 9)
    поле представляет из себя 
    :one: :two: :three:
    :four: :five: :six:
    :seven: :eight: :nine:
    __Все команды вводятся **латинскими буквами**__""",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="xo")
    async def tic_tac_toe(self, ctx, p1: discord.Member, p2: discord.Member):
        if self.game_over:
            if p1 == self.bot.user or p2 == self.bot.user:
                await ctx.send("К сожалению я не могу с вами играть")
                return
            self.board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                                         ":white_large_square:", ":white_large_square:", ":white_large_square:",
                                         ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            self.turn = ""
            self.game_over = False
            self.count = 0
            self.player1 = p1
            self.player2 = p2
            # print the board
            line = ""
            for i in range(len(self.board)):
                if i == 2 or i == 5 or i == 8:
                    line += " " + self.board[i]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + self.board[i]

            # determine who goes first
            num = random.randint(1, 2)
            if num == 1:
                self.turn = self.player1
                await ctx.send("Сейчас ходит <@" + str(self.player1.id) + ">")
            elif num == 2:
                self.turn = self.player2
                await ctx.send("Сейчас ходит <@" + str(self.player2.id) + ">")
        else:
            await ctx.send("Игра в прогрессе. Завершите текущую, затем начните новую.")

    @commands.command(name="xo_place")
    async def tic_tac_toe_place(self, ctx, pos: int):
        if not self.game_over:
            mark = ""
            if self.turn == ctx.author:
                if self.turn == self.player1:
                    mark = ":negative_squared_cross_mark:"
                elif self.turn == self.player2:
                    mark = ":o2:"
                if 0 < pos < 10:
                    if self.board[pos - 1] == ":white_large_square:":
                        self.board[pos - 1] = mark
                        self.count += 1

                        # print the board
                        line = ""
                        for x in range(len(self.board)):
                            if x == 2 or x == 5 or x == 8:
                                line += " " + self.board[x]
                                await ctx.send(line)
                                line = ""
                            else:
                                line += " " + self.board[x]

                        self.tic_tac_toe_check_winner(mark)
                        if self.game_over:
                            embed = discord.Embed(
                                title=f"Победа {mark} :exclamation:",
                                colour=discord.Colour.purple()
                            )
                            await ctx.send(embed=embed)
                        elif self.count >= 9:
                            self.game_over = True
                            embed = discord.Embed(
                                title="Ничья :exclamation:",
                                colour=discord.Colour.purple()
                            )
                            await ctx.send(embed=embed)

                        # switch turns
                        self.turn = self.player1 if self.turn == self.player2 else self.player2
                    else:
                        await ctx.send("Клетка уже занята!")
                else:
                    await ctx.send("Число должно быть от 1 до 9")
            else:
                await ctx.send("Сейчас не ваш ход")
        else:
            await ctx.send(f"Начните новую игру используя команду {prefix}xo")

    def tic_tac_toe_check_winner(self, mark):
        for condition in self.winning_conditions:
            if self.board[condition[0]] == mark and \
                    self.board[condition[1]] == mark and \
                    self.board[condition[2]] == mark:
                self.game_over = True

    @tic_tac_toe.error
    async def tic_tac_toe_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Необходимо два игрока")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Убедитесь что вы указали участника.")

    @tic_tac_toe_place.error
    async def tic_tac_toe_place(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Вы не указали позицию")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Вы ввели не число")
