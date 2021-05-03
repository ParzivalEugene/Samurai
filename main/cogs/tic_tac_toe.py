import discord
from discord.ext import commands
from random import choice
from cogs.commands import commands_names
from cogs.config import *


class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.board = [None] * 9
        self.icons = {
            "x": ":negative_squared_cross_mark:",
            "o": ":o2:",
            None: ":white_large_square:"
        }
        self.game_over = True
        self.game_type = None
        self.turn = ""
        self.count = 0
        self.player1 = ""
        self.player2 = ""
        self.mark = ""
        self.pos = 0
        self.winning_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

    @commands.command(name=commands_names["tic tac toe"]["help"])
    async def tic_tac_toe_help(self, ctx):
        embed = discord.Embed(
            title="Информация о модуле **крестики-нолики**",
            description=":negative_squared_cross_mark: :o2:",
            colour=discord.Colour.purple()
        )
        embed.add_field(name="Команды",
                        value=f"""Модуль с крестиками-ноликами для игр с друзьями или мной
**{prefix}{commands_names["tic tac toe"]["help"]}** - отдельный эмбед для вывода инфы о крестиках ноликах
**{prefix}{commands_names["tic tac toe"]["rules"]}** - отдельный эмбед для вывода правил крестиков ноликов
**{prefix}{commands_names["tic tac toe"]["init game"]} <member1> <member2>** - начало игры с указанием двух юзеров
**{prefix}{commands_names["tic tac toe"]["place"]} <number>** - поместит нужный символ в клетку
:one: :two: :three:
:four: :five: :six:
:seven: :eight: :nine:
**{prefix}{commands_names["tic tac toe"]["lose"]}** - текущий игрок сдастся""",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(name=commands_names["tic tac toe"]["rules"])
    async def tic_tac_toe_rules(self, ctx):
        embed = discord.Embed(
            title="Информация о **крестиках-ноликах**",
            description=":negative_squared_cross_mark: :o2:",
            colour=discord.Colour.purple()
        )
        embed.add_field(name="Правила",
                        value="Игроки по очереди ставят на свободные клетки поля 3х3 знаки (один всегда крестики, другой всегда нолики). Первый, выстроивший в ряд 3 своих фигуры по вертикали, "
                              "горизонтали или диагонали, выигрывает. Первый ход делает игрок, ставящий крестики.\n Обычно по завершении партии выигравшая сторона зачёркивает чертой свои три знака "
                              "(нолика или крестика), составляющих сплошной ряд.\n"
                              "[Wikipedia](https://ru.wikipedia.org/wiki/%D0%9A%D1%80%D0%B5%D1%81%D1%82%D0%B8%D0%BA%D0%B8-%D0%BD%D0%BE%D0%BB%D0%B8%D0%BA%D0%B8)",
                        inline=False)
        embed.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png"
        )
        await ctx.send(embed=embed)

    @commands.command(name=commands_names["tic tac toe"]["init game"])
    async def tic_tac_toe_start(self, ctx, player1: discord.Member, player2: discord.Member, game_type="ai"):
        """Function for initialize new game"""

        """----------------------------------Errors check-----------------------------------------"""

        if not self.game_over:
            async with ctx.typing():
                return await ctx.send(choice([
                    "Сладенький ты еще здесь недовоевал, либо сдавайся, либо продолжай сосать",
                    "Дедуля ты еще не доиграл", "Пожилой доиграй игру, а потом стартуй новую или сдавайся нахуй"
                ]))
        if player1 == player2 == self.bot.user:
            async with ctx.typing():
                return await ctx.send(choice([
                    "Я блять тебе бои роботов показывать не буду иди нахуй", "Сука над дедом издевается, я перед тобой плясать не буду", "Маму свою с самой собой заставь играть"
                ]))
        if player1 == player2 == ctx.author:
            async with ctx.typing():
                return await ctx.send(choice([
                    "Ты еблан блять сам с собой играть", "Дедуля в маразм впал, сам с собой играть хочет", "Сука с самим собой нельзя играть"
                ]))
        if player1 == player2:
            async with ctx.typing():
                return await ctx.send(choice([
                    "Бля ты его за дебила держишь, он не может сам с собой играть", "Сука нельзя играть с самим собой блять"
                ]))
        if (player1 == self.bot.user or player2 == self.bot.user) and game_type not in ["ai", "random"]:
            async with ctx.typing():
                return await ctx.send(choice([
                    "Дедуля я таких аргументов не знаю.", "Пожилой я таких типов игры не знаю", f"Ебать сынок чо значит {game_type}, я блять такое не знаю",
                    "Бля деда за шизика не держи, чо это за тип игры такой", f"Бля я старенький конечно, но не в маразме, чо такое {game_type}"
                ]))
        if player1.bot and player2.bot:
            async with ctx.typing():
                return await ctx.send(choice([
                    "Чумба эти дурачки не настолько умные, чтобы в игрушки играть", "Ебать ты этих ослов за кого считаешь, они блять тупые играть не умеют, не то что я :sunglasses:",
                    "Эти ослики не такие умные для этого", "Бля это тебе цирк что-ли, дарку ботов он хочет. Я этих дурачков в обиду не дам",
                    "Бля ты тот челик, который в фифе ставит ботов друг с другом играть, ебантяй ты"
                ]))
        if (player1.bot or player2.bot) and not (player1 == self.bot.user or player2 == self.bot.user):
            bot = player1 if player1.bot else player2
            async with ctx.typing():
                return await ctx.send(choice([
                    f"Ты бля нахуй этого дурачка {bot.mention} обижаешь, со мной дерись", f"Блять этот ослик {bot.mention} не умеет играть",
                    f"Сука этот пиздахряк {bot.mention} не умеет ваши крестики очки шаришь, со мной дерись", f"Сука только я умный блять умею играть, этот осел {bot.mention} нет"
                ]))

        """-------------------------------initializing new game-----------------------------------"""

        if player1 == self.bot.user or player2 == self.bot.user:
            self.game_type = game_type
        else:
            self.game_type = None
        self.board = [None] * 9
        self.turn = ""
        self.game_over = False
        self.count = 0
        self.player1 = player1
        self.player2 = player2
        self.mark = "o"
        self.turn = choice([self.player1, self.player2]) if self.game_type is None else self.bot.user
        await self.print_board(ctx)
        await ctx.send(f"Первым ходит {self.turn.mention}")

        # Bot moves if his turn is the first
        if self.turn.bot:
            await self.bot_place(ctx)

    @commands.command(name=commands_names["tic tac toe"]["place"])
    async def tic_tac_toe_place(self, ctx, pos: int):
        """Function for place figure in current position"""

        """----------------------------------Errors check-----------------------------------------"""

        if self.game_over:
            async with ctx.typing():
                return await ctx.send(choice([
                    "Пожилой блять ты с кем воюешь, нет активных игр", "Внучок блять, чо деда наебать пытаешься, еще никто не играет", "Бля зелебобка активные игры отсутствуют, стартуй новую",
                    "Бля я для кого правила делал сука, перед тем как хуйню свою высирать начни новую игру, барбосы блять старого не уважают"
                ]))
        if self.turn not in [self.player1, self.player2]:
            async with ctx.typing():
                return await ctx.reply(choice([
                    "Сука малой блять, не видишь ребятишки играют, а тебя я в списке игроков не вижу", "Блять не лезь сука дебил ебаный, ОНО ТЕБЯ СОЖРЕТ, внучок сейчас другие играют",
                    "Блять ты вроде не даун, тогда нахуй ты пукаешь свой блять .xo_place сука, другие играют ебаный сыр", "бля я щас тебе ебальничек твой прелестный расхуепердолю, внучок, другие играют"
                ]))
        if self.turn != ctx.author:
            async with ctx.typing():
                return await ctx.send(choice([
                    "Не твой ход молодой", "Блять сейчас не ты ходишь внучкок", "Бля дедуля медленно выводит, не спеши молодой", "Молодеж блять не торопитесь, не твой ход внучок"
                ]))
        if not (0 < pos < 10):
            async with ctx.typing():
                return await ctx.send(choice([
                    "Ишь ты блять чо захотел, всего 9 сука клеток", "Бля от 1 до 9 числа вводятся ебаный ваш рот, сломаете деда скоро", "Внучок блять неправильно ты позицию ввел, ты хоть правила смотри"
                ]))
        if not (self.board[pos - 1] is None):
            async with ctx.typing():
                return await ctx.send(choice([
                    "Пожилой эта клетка занята", "Внучок сюда ставить нельзя, занято ебана", "Ебать копать эта клетка занята", "Не пизди старому, сюда нельзя ставить"
                ]))

        """-------------------------------------Player-move---------------------------------------"""

        self.switch_mark()
        self.board[pos - 1] = self.mark
        self.count += 1
        await self.print_board(ctx)
        self.check_winner()
        await self.print_game_over(ctx)
        self.switch_turn()

        """---------------------------------------Bot-move----------------------------------------"""

        if not (self.game_type is None) and not self.game_over:
            await self.bot_place(ctx)

    @commands.command(name=commands_names["tic tac toe"]["lose"])
    async def tic_tac_toe_lose(self, ctx):
        if self.game_over:
            return await ctx.send(choice([
                "Внучок ты даже не повоевал, а уже сдаешься", "Блять сынок сначала повоюй, потом сдавайся", "Ты еще не играешь не во что долбаебка, нахуй сдаешься"
            ]))
        self.game_over = True
        embed = discord.Embed(
            title=f"{self.turn.name} сдался:exclamation:",
            colour=discord.Colour.purple()
        )
        await ctx.send(embed=embed)

    async def print_game_over(self, ctx):
        if self.game_over:
            embed = discord.Embed(
                title=f"Победа {self.turn.name} {self.icons[self.mark]}:exclamation:",
                colour=discord.Colour.purple()
            )
            await ctx.send(embed=embed)
            return
        if self.count >= 9:
            self.game_over = True
            embed = discord.Embed(
                title="Ничья:exclamation:",
                colour=discord.Colour.purple()
            )
            await ctx.send(embed=embed)
        return

    def check_winner(self):
        for combo in self.winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] == self.mark:
                self.game_over = True
                return

    def check_winner_mark(self, mark):
        for combo in self.winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] == mark:
                return True
        return False

    async def bot_place(self, ctx):
        self.switch_mark()
        self.make_move()
        await ctx.send(f"{prefix}xo_place {self.pos + 1}")
        await self.print_board(ctx)
        self.count += 1
        self.check_winner()
        await self.print_game_over(ctx)
        self.switch_turn()
        return

    def switch_turn(self):
        self.turn = self.player1 if self.turn == self.player2 else self.player2

    def switch_mark(self):
        self.mark = "x" if self.mark == "o" else "o"

    async def print_board(self, ctx):
        board = [self.icons[i] for i in self.board]
        await ctx.send("\n".join([" ".join(board[i * 3:(i + 1) * 3]) for i in range(3)]))
        return

    def make_move(self):
        if self.game_type == "random":
            res = []
            for i in range(len(self.board)):
                if self.board[i] is None:
                    res.append(i)
            self.pos = choice(res)
            self.board[self.pos] = self.mark
        elif self.game_type == "ai":
            if all(i is None for i in self.board):
                self.pos = choice(range(9))
                self.board[self.pos] = self.mark
            else:
                best_score = -800
                best_move = 0
                board, count = self.board, self.count
                for i in range(len(board)):
                    if board[i] is None:
                        board[i] = self.mark
                        count += 1
                        score = self.minimax(count, board, False)
                        print(score, end=" ")
                        count -= 1
                        board[i] = None
                        if score > best_score:
                            best_score = score
                            best_move = i
                self.pos = best_move
                self.board[best_move] = self.mark

    def minimax(self, count, board, is_max):
        if self.check_winner_mark(self.mark):
            return 1
        elif self.check_winner_mark("x" if self.mark == "o" else "o"):
            return -1
        elif self.count >= 9:
            return 0

        if is_max:
            best_score = -800
            for i in range(len(board)):
                if board[i] is None:
                    board[i] = self.mark
                    count += 1
                    score = self.minimax(count, board, False)
                    count -= 1
                    board[i] = None
                    if score > best_score:
                        best_score = score
            return best_score
        else:
            best_score = 800
            for i in range(len(board)):
                if board[i] is None:
                    board[i] = "x" if self.mark == "o" else "o"
                    count += 1
                    score = self.minimax(count, board, True)
                    count -= 1
                    board[i] = None
                    if score < best_score:
                        best_score = score
            return best_score

    @tic_tac_toe_start.error
    async def tic_tac_toe_error(self, ctx, error):
        async with ctx.typing():
            if not self.game_over:
                await ctx.send(choice([
                    "Блять сынок игра идет", "Еще играем сука подожди", "Блять видишь война, позже", "Молодежь торопиться, подожди еще"
                ]))
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(choice([
                    "Сынок ебать, два участника надо", "Внучок зови друга или со мной играй, два игрока надо"
                ]))
            elif isinstance(error, commands.BadArgument):
                await ctx.send(choice([
                    "Бля ты какую то хуйню мне скормил, я сломался", "Не пихай сюда нихуя кроме участников"
                ]))

    @tic_tac_toe_place.error
    async def tic_tac_toe_place_error(self, ctx, error):
        async with ctx.typing():
            if self.game_over:
                await ctx.send(choice([
                    "Блять да мамке своей поставь нахуй, нет активных игр", "Сука где ты видишь активную игру, тогда нахуя ты мне блять свое иксо блять плейс пишешь уу молодеж ебобаная",
                    "Сука внучок нет активных игр, нахуй ставишь", "Блять все ебать фашисты победили, поздно ты свой крестик или нолик ставишь, мне похуй!!"
                ]))
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(choice([
                    "Блять куда ставить то ебана", "Ебать я чо тогадаться должен куда ты поставить хочешь", "Сука внучок ебаный, я ебу куда ставить"
                ]))
            elif isinstance(error, commands.BadArgument):
                await ctx.send(choice([
                    "Бля ты какую то хуйню мне скормил, я сломался", "Не пихай сюда нихуя кроме числа", "Вот бля шутник ебучий, сюда надо пихать число, пездюк маленький"
                ]))
