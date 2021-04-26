import discord
from discord.ext import commands
from cogs.config import *
from cogs.commands import commands_names
from random import choice


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

    @commands.command(name=commands_names["connect four"]["help"])
    async def connect_four_place_help(self, ctx):
        embed = discord.Embed(
            title="Информация о **4 в ряд**",
            description=f'{self.icons["ball_1"]} {self.icons["ball_2"]}',
            colour=discord.Colour.purple()
        )
        embed.add_field(name="Команды",
                        value=f"""Аналогичный модуль крестикам-ноликам, катай с друзьями или со мной
**{prefix}{commands_names["connect four"]["help"]}** - отдельный эмбед для вывода инфы о четыре в ряд
**{prefix}{commands_names["connect four"]["rules"]}** - отдельный эмбед для вывода правил четыре в ряд
**{prefix}{commands_names["connect four"]["init game"]} <member1> <member2>** - начало игры с указанием двух участников
**{prefix}{commands_names["connect four"]["place"]} <number>** - бросок фишки в колонку с указанным номером
**{prefix}{commands_names["connect four"]["lose"]}** - текущий игрок сдастся""",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(name=commands_names["connect four"]["rules"])
    async def connect_four_place_rules(self, ctx):
        embed = discord.Embed(
            title="Информация о **4 в ряд**",
            description=f'{self.icons["ball_1"]} {self.icons["ball_2"]}',
            colour=discord.Colour.purple()
        )
        embed.add_field(name="Правила",
                        value="Цель игры — расположить раньше противника подряд по горизонтали, вертикали или диагонали четыре фишки своего цвета. Существуют варианты игры с полем разного размера, "
                              "с фишками в форме дисков или шариков. Наиболее распространенный вариант, также называемый классическим, 7x6. \n"
                              "[Wikipedia](https://ru.wikipedia.org/wiki/%D0%A7%D0%B5%D1%82%D1%8B%D1%80%D0%B5_%D0%B2_%D1%80%D1%8F%D0%B4)",
                        inline=False)
        embed.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png"
        )
        await ctx.send(embed=embed)

    @commands.command(name=commands_names["connect four"]["init game"])
    async def connect_four(self, ctx, player1: discord.Member, player2: discord.Member):
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
        if player1.bot and player2.bot:
            async with ctx.typing():
                return await ctx.send(choice([
                    "Чумба эти дурачки не настолько умные, чтобы в игрушки играть", "Ебать ты этих ослов за кого считаешь, они блять тупые играть не умеют",
                    "Эти ослики не такие умные для этого", "Бля это тебе цирк что-ли, дарку ботов он хочет. Я этих дурачков в обиду не дам",
                    "Бля ты тот челик, который в фифе ставит ботов друг с другом играть, ебантяй ты"
                ]))
        elif player1 == self.bot.user or player2 == self.bot.user:
            async with ctx.typing():
                return await ctx.send(choice([
                    "Молодой я еще не научился в эту парашу играть и нахуй оно мне не надо", "Бля у тебя чо друзей нет, я не умею в эту парашу играть", "Не напрягай старого, не буду я в это играть"
                ]))

        """-------------------------------initializing new game-----------------------------------"""

        self.board = [[self.icons["cell"] for _ in range(self.board_size["length"])] for _ in range(self.board_size["height"])]
        self.game_over = False
        self.count = 0
        self.player1 = player1
        self.player2 = player2

        self.turn = choice([self.player1, self.player2])
        await self.print_board(ctx)
        await ctx.send(f"Первым ходит {self.turn.mention}")

    @commands.command(name=commands_names["connect four"]["place"])
    async def connect_four_place(self, ctx, pos: int):
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
                    "Блять ты вроде не даун, тогда нахуй ты пукаешь свой блять .с4_place сука, другие играют ебаный сыр",
                    "бля я щас тебе ебальничек твой прелестный расхуепердолю, внучок, другие играют"
                ]))
        if self.turn != ctx.author:
            async with ctx.typing():
                return await ctx.send(choice([
                    "Не твой ход молодой", "Блять сейчас не ты ходишь внучок", "Бля дедуля медленно выводит, не спеши молодой", "Молодеж блять не торопитесь, не твой ход внучок"
                ]))
        if 0 < pos < self.board_size["length"]:
            async with ctx.typing():
                return await ctx.send(choice([
                    f"Блять молодой позиция от 1 до {self.board_size['length']}", "Сука неверная позиция", "Неправильно ставишь", "Деда наебать пытается, неверная позиция"
                ]))
        if not any(self.board[i][pos - 1] == self.icons["cell"] for i in range(self.board_size["height"])):
            async with ctx.typing():
                return await ctx.send(choice([
                    "Пожилой этот столбец занят", "Внучок сюда ставить нельзя, занято ебана", "Ебать копать этот столбец занят", "Не пизди старому, сюда нельзя ставить"
                ]))
        mark = self.icons["ball_1"] if self.turn == self.player2 else self.icons["ball_2"]
        position = 5
        while self.board[position][pos - 1] != self.icons["cell"]:
            position -= 1
        self.board[position][pos - 1] = mark
        self.count += 1

        await self.print_board(ctx)
        self.connect_four_check_winner(mark)
        if self.game_over:
            embed = discord.Embed(
                title=f"Победа {self.turn.mention} {self.icons[mark]}:exclamation:",
                colour=discord.Colour.purple()
            )
            await ctx.send(embed=embed)
        if self.count >= 9:
            self.game_over = True
            embed = discord.Embed(
                title="Ничья:exclamation:",
                colour=discord.Colour.purple()
            )
            await ctx.send(embed=embed)
        self.turn = self.player1 if self.turn == self.player2 else self.player2

    @commands.command(name=commands_names["connect four"]["lose"])
    async def connect_four_lose(self, ctx):
        if self.game_over:
            return await ctx.send(choice([
                "Внучок ты даже не повоевал, а уже сдаешься", "Блять сынок сначала повоюй, потом сдавайся", "Ты еще не играешь не во что долбаебка, нахуй сдаешься"
            ]))
        self.game_over = True
        embed = discord.Embed(
            title=f"{self.turn.mention} сдался:exclamation:",
            colour=discord.Colour.purple()
        )
        await ctx.send(embed=embed)

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

    async def print_board(self, ctx):
        await ctx.send("\n".join([" ".join(i) for i in self.board]))
        return

    @connect_four.error
    async def connect_four_error(self, ctx, error):
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

    @connect_four_place.error
    async def connect_four_place_error(self, ctx, error):
        async with ctx.typing():
            if self.game_over:
                await ctx.send(choice([
                    "Блять да мамке своей поставь нахуй, нет активных игр", "Сука где ты видишь активную игру, тогда нахуя ты мне блять свое си четыре блять плейс пишешь уу молодеж ебобаная",
                    "Сука внучок нет активных игр, нахуй ставишь"
                ]))
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(choice([
                    "Блять куда ставить то ебана", "Ебать я чо тогадаться должен куда ты поставить хочешь", "Сука внучок ебаный, я ебу куда ставить"
                ]))
            elif isinstance(error, commands.BadArgument):
                await ctx.send(choice([
                    "Бля ты какую то хуйню мне скормил, я сломался", "Не пихай сюда нихуя кроме числа", "Вот бля шутник ебучий, сюда надо пихать число, пездюк маленький"
                ]))
