import discord
from discord.ext import commands, tasks
from my_token import token
import requests
import json
import re
import random
from keep_alive import keep_alive
from datetime import date

prefix = "."
bot = commands.Bot(command_prefix=prefix, help_command=None)

tic_tac_toe_info = {
    "player1": "",
    "player2": "",
    "turn": "",
    "gameOver": True,
    "board": [],
    "count": 0,
    "winning_conditions": [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
}


def get_quote():
    """Return random quote"""
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = ' - '.join([json_data[0]['q'], json_data[0]['a']])
    return quote


def get_emoji(name):
    """Return emoji by name"""
    return discord.utils.get(bot.emojis, name=name)


def embed_cat(author):
    """Return the embed with random kitty"""
    response = requests.get("https://aws.random.cat/meow")
    data = response.json()
    embed = discord.Embed(
        title="Котик :smiling_face_with_3_hearts:",
        description=f"Прямо как ты {author.mention}",
        colour=discord.Colour.purple()
    )
    embed.set_image(url=data["file"])
    embed.set_footer(text="")
    return embed


def embed_dog(author):
    """Return the embed with random doggy"""
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension, url = '', ''
    while file_extension not in allowed_extension:
        contents = requests.get('https://random.dog/woof.json').json()
        url = contents['url']
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    data = url
    embed = discord.Embed(
        title="Пёсик :smiling_face_with_3_hearts:",
        description=f"Прямо как ты {author.mention}",
        colour=discord.Colour.purple()
    )
    embed.set_image(url=data)
    embed.set_footer(text="")
    return embed


@bot.event
async def on_member_join(member):
    await bot.get_channel(783742051556655174).send(member.name, "присоединлся к серверу")


@bot.event
async def on_member_remove(member):
    await bot.get_channel(783742051556655174).send(member.name, "покинул сервер")


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f"{prefix}help - INVINCIBLE WARRIORS")
    )
    await check_birthday.start()


@bot.event
async def on_message(message):
    """Reacting on messages and send request by phrase"""
    insults = [
        "ботяра пидор", "бот говно", "говно бот", "долбаеб бот", "бот долбаеб"
    ]

    msg = message.content.lower()
    if message.author == bot.user:
        return

    """Commands ----------------------------------------------------------------------------------"""

    if msg.startswith("кот"):
        await message.channel.send(embed=embed_cat(message.author))
    if any(msg.startswith(i) for i in ("пес", "соба")):
        await message.channel.send(embed=embed_dog(message.author))
    if msg.startswith("вдохновение"):
        await message.channel.send(get_quote())

    """Reacting on basic phrases -----------------------------------------------------------------"""

    if msg.startswith("привет"):
        await message.channel.send("Приветствую вас!")
    if msg.startswith("нахуй юлю"):
        await message.channel.send("туда ее")
        await message.channel.send(get_emoji("julia"))
    if any(phrase in msg for phrase in insults):
        await message.channel.send("мать твоя блять, сын собаки")
        await message.channel.send(get_emoji('kavo'))
    if msg.startswith("арина сука"):
        await message.channel.send("согласен")
        await message.channel.send(get_emoji("ahuet"))
    await bot.process_commands(message)


@bot.command(name="help")
async def my_help(ctx):
    embed = discord.Embed(
        title=f"Информация обо мне",
        description="Распиздатый ботяра! За себя постою, нахуй пошлю, в игры поиграю... блять да я все умею",
        colour=discord.Colour.purple()
    )
    embed.set_footer(text="Say your prayers, Moron!")
    embed.set_image(url="https://cdn.discordapp.com/attachments/783747422898880533/828266665602580500/ghostrunner-review.jpg")
    embed.add_field(name="Команды",
                    value=f"""**{prefix}help** - вывод информации о боте.
**{prefix}xo_rules** - вывод информации о крестиках-ноликах.
**{prefix}bd_rules** - вывод информации о днях рождения. 
__Все команды вводятся **латинскими буквами**__""",
                    inline=False)
    await ctx.send(embed=embed)


@bot.command(name="xo_rules")
async def tic_tac_toe_rules(ctx):
    embed = discord.Embed(
        title=f"Информация о крестиках-ноликах",
        description=":negative_squared_cross_mark: :o2:",
        colour=discord.Colour.purple()
    )
    embed.add_field(name="Команды",
                    value=f"""**{prefix}xo <member1> <member2>** - начало игры игры в крестики-нолики с указанием игроков.
**{prefix}place <number>** - команда для установки Х или О в нужное место (числа от 1 до 9)
поле представляет из себя 
:one: :two: :three:
:four: :five: :six:
:seven: :eight: :nine:
__Все команды вводятся **латинскими буквами**__""",
                    inline=False)
    await ctx.send(embed=embed)


@bot.command(name="xo")
async def tic_tac_toe(ctx, p1: discord.Member, p2: discord.Member):
    global tic_tac_toe_info
    if tic_tac_toe_info["gameOver"]:
        if p1.id == bot.user or p2 == bot.user:
            await ctx.send("К сожалению я не могу с вами играть")
            return
        tic_tac_toe_info["board"] = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                                     ":white_large_square:", ":white_large_square:", ":white_large_square:",
                                     ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        tic_tac_toe_info["turn"] = ""
        tic_tac_toe_info["gameOver"] = False
        tic_tac_toe_info["count"] = 0
        tic_tac_toe_info["player1"] = p1
        tic_tac_toe_info["player2"] = p2
        # print the board
        line = ""
        for i in range(len(tic_tac_toe_info["board"])):
            if i == 2 or i == 5 or i == 8:
                line += " " + tic_tac_toe_info["board"][i]
                await ctx.send(line)
                line = ""
            else:
                line += " " + tic_tac_toe_info["board"][i]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            tic_tac_toe_info["turn"] = tic_tac_toe_info["player1"]
            await ctx.send("Сейчас ходит <@" + str(tic_tac_toe_info.get("player1").id) + ">")
        elif num == 2:
            tic_tac_toe_info["turn"] = tic_tac_toe_info["player2"]
            await ctx.send("Сейчас ходит <@" + str(tic_tac_toe_info.get("player2").id) + ">")
    else:
        await ctx.send("Игра в прогрессе. Завершите текущую, затем начните новую.")


@bot.command()
async def place(ctx, pos: int):
    global tic_tac_toe_info
    if not tic_tac_toe_info["gameOver"]:
        mark = ""
        if tic_tac_toe_info["turn"] == ctx.author:
            if tic_tac_toe_info["turn"] == tic_tac_toe_info["player1"]:
                mark = ":negative_squared_cross_mark:"
            elif tic_tac_toe_info["turn"] == tic_tac_toe_info["player2"]:
                mark = ":o2:"
            if 0 < pos < 10:
                if tic_tac_toe_info["board"][pos - 1] == ":white_large_square:":
                    tic_tac_toe_info["board"][pos - 1] = mark
                    tic_tac_toe_info["count"] += 1

                    # print the board
                    line = ""
                    for x in range(len(tic_tac_toe_info["board"])):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + tic_tac_toe_info["board"][x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + tic_tac_toe_info["board"][x]

                    check_winner(mark)
                    if tic_tac_toe_info["gameOver"]:
                        await ctx.send(mark + " победил")
                    elif tic_tac_toe_info["count"] >= 9:
                        tic_tac_toe_info["gameOver"] = True
                        await ctx.send("Ничья!")

                    # switch turns
                    if tic_tac_toe_info["turn"] == tic_tac_toe_info["player1"]:
                        tic_tac_toe_info["turn"] = tic_tac_toe_info["player2"]
                    elif tic_tac_toe_info["turn"] == tic_tac_toe_info["player2"]:
                        tic_tac_toe_info["turn"] = tic_tac_toe_info["player1"]
                else:
                    await ctx.send("Клетка уже занята!")
            else:
                await ctx.send("Число должно быть от 1 до 9")
        else:
            await ctx.send("Сейчас не ваш ход")
    else:
        await ctx.send("Начните новую игру используя команду !крестики-нолики")


def check_winner(mark):
    global tic_tac_toe_info
    for condition in tic_tac_toe_info["winning_conditions"]:
        if tic_tac_toe_info["board"][condition[0]] == mark and \
                tic_tac_toe_info["board"][condition[1]] == mark and \
                tic_tac_toe_info["board"][condition[2]] == mark:
            tic_tac_toe_info["gameOver"] = True


@tic_tac_toe.error
async def tic_tac_toe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Необходимо два игрока")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Убедитесь что вы пинганули участника.")


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Вы не указали позицию")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Вы ввели не число")


@bot.command(name="test")
async def test(ctx):
    embed = discord.Embed(
        title=f"С ДНЕМ РОЖДЕНИЯ WARRIOR <@>",
        description=":sweat_drops: :sweat_drops: :sweat_drops:",
        colour=discord.Colour.purple()
    )
    embed.add_field(name="Блять какой же ты все таки ахуенный(-ая)",
                    value="Поздравляю тебя с этим заебубительным днем. Желаю тебе счастья блять, радости, вот этой всей вашей человечей хуйни. Но никогда не забывай об этом сервере, здесь тебе "
                          "всегда будут рады.",
                    inline=False)
    await ctx.send(embed=embed)


@tasks.loop(hours=12)
async def check_birthday():
    today = str(date.today())[5:]
    table = []
    with open("birthdays.json", "r") as input_file:
        data = json.load(input_file)
        for i in range(len(data["bd"])):
            info = list(data["bd"][i].keys())[0]
            month, day = data["bd"][i][info]["month"], data["bd"][i][info]["day"]
            current_date = date(2021, month, day).isoformat()[5:]
            table.append([current_date, info])
    for i in table:
        if i[0] == today and i[1] != "test":
            embed = discord.Embed(
                title=f"С ДНЕМ РОЖДЕНИЯ WARRIOR <@{i[1]}>",
                description=":sweat_drops: :sweat_drops: :sweat_drops:",
                colour=discord.Colour.purple()
            )
            embed.add_field(name="Блять какой же ты все таки ахуенный(-ая)",
                            value="Поздравляю тебя с этим заебубительным днем. Желаю тебе счастья блять, радости, вот этой всей вашей человечей хуйни. Но никогда не забывай об этом сервере, "
                                  "здесь тебе всегда будут рады.",
                            inline=False)
            await bot.get_channel(778544220054224906).send(embed=embed)


@bot.command(name="bd_rules")
async def rules_birthday(ctx):
    embed = discord.Embed(
        title="Информация о календаре дней рождений",
        description=":fire: :fire: :fire:",
        colour=discord.Colour.purple()
    )
    embed.add_field(name="Команды",
                    value=f"""**{prefix}bd <month> <day>** - внос в базу данных с указанием даты (можно внести только один раз:exclamation::exclamation::exclamation:)
    **{prefix}bd_show** - выводит график всех дней рождений.
__Все команды вводятся **латинскими буквами**__""",
                    inline=False)
    await ctx.send(embed=embed)


@bot.command(name="bd_show")
async def show_birthday_table(ctx):
    embed = discord.Embed(
        title="ДНИ РОЖДЕНИЯ",
        colour=discord.Colour.purple()
    )
    with open("birthdays.json", "r") as file:
        data = json.load(file)
        for person in range(len(data["bd"])):
            if not person:
                continue
            info = list(data["bd"][person].keys())[0]
            month, day = data["bd"][person][info]["month"], data["bd"][person][info]["day"]
            embed.add_field(name="<@{}>".format(int(info)),
                            value=f"{month}.{day}",
                            inline=False)
        await ctx.send(embed=embed)


@bot.command(name="bd")
async def add_birthday_date(ctx, month: int, day: int):
    if not any(i.id == 778542601690284034 for i in ctx.author.roles):
        await ctx.send("У вас недостачно высокая роль для этой команды")
        return
    with open("birthdays.json") as info:
        birthdays = json.load(info)
        if any(str(ctx.author.id) in i.keys() for i in birthdays["bd"]):
            await ctx.send("Вы уже указали свою дату")
            return
        if not (1 <= month <= 12 or 1 <= day <= 31):
            await ctx.send("Вы указали неверную дату")
            return
        birthdays["bd"].append({ctx.author.id: {"month": month, "day": day}})
        with open("birthdays.json", "w") as outfile:
            json.dump(birthdays, outfile)
        await ctx.send("Данные успешно внесены")


@add_birthday_date.error
async def add_birthday_date_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Вы указали неполную дату")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Вы указали неверную дату")


keep_alive()
bot.run(token)
