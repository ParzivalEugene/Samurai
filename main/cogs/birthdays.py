import discord
from discord.ext import commands, tasks
from datetime import date
import json
from random import choice
from cogs.commands import commands_names
from cogs.config import *


class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(hours=12)
    async def check_birthday(self):
        today = str(date.today())[5:]
        table = []
        with open("database/birthdays.json", "r") as input_file:
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
                await self.bot.get_channel(778544220054224906).send(embed=embed)

    @commands.command(name=commands_names["birthdays"]["help"])
    async def rules_birthday(self, ctx):
        embed = discord.Embed(
            title="Информация о календаре дней рождений",
            description=":fire: :fire: :fire:",
            colour=discord.Colour.purple()
        )
        embed.add_field(name="Команды",
                        value=f"""**{prefix}{commands_names["birthdays"]["add birthday"]} <month> <day>** - внос в базу данных с указанием даты (можно внести только один раз)
        **{prefix}{commands_names["birthdays"]["show birthdays"]}** - выводит график всех дней рождений.""",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(name=commands_names["birthdays"]["show birthdays"])
    async def show_birthday_table(self, ctx):
        embed = discord.Embed(
            title="ДНИ РОЖДЕНИЯ",
            colour=discord.Colour.purple()
        )
        with open("database/birthdays.json", "r") as file:
            data = json.load(file)
            for person in range(len(data["bd"])):
                if not person:
                    continue
                info = list(data["bd"][person].keys())[0]
                month, day = data["bd"][person][info]["month"], data["bd"][person][info]["day"]
                embed.add_field(name=f"<@{info}>",
                                value=f"{month}.{day}",
                                inline=False)
            await ctx.send(embed=embed)

    @commands.command(name=commands_names["birthdays"]["add birthday"])
    async def add_birthday_date(self, ctx, month: int, day: int):
        if not any(i.id == 694548925612425317 for i in ctx.author.roles):
            await ctx.send(choice([
                "Внучок у тебя слишком низкая роль для этой команды", "Пожилой тебе эту команду еще рано юзать", "Молодой, слишком низкая роль, чтобы юзать эту команду"
            ]))
            return
        with open("database/birthdays.json") as info:
            birthdays = json.load(info)
            async with ctx.typing():
                if any(str(ctx.author.id) in i.keys() for i in birthdays["bd"]):
                    return await ctx.send(choice([
                        "Блять тебя семь раз записывать ебана, ты уже в базе", "Нахуя тебе второй раз в базу вноситься, молодой", "Ебаный сыр блять :cheese: :pinched_fingers: ты уже в базе",
                        "Блять я тебя второй раз в базу вносить не буду", "Ты уже в базе молодой"
                    ]))
                if not (1 <= month <= 12 and 1 <= day <= 31):
                    return await ctx.send(choice([
                        "Сынок ебучий ты чо меня наебать пытаешь, не вводи хуйни", "Блять ты вводишь хуйню, переделывай", "Ебана введи нормальный месяц и день, хуле ты делаешь",
                        "Неправильно блять ебаные волки :wolf:, широкую на широкую, не вводи в меня хуйню"
                    ]))
                birthdays["bd"].append({ctx.author.id: {"month": month, "day": day}})
                with open("database/birthdays.json", "w") as outfile:
                    json.dump(birthdays, outfile)
                await ctx.send(choice([
                    f"Ну все сладенький ты в базе, поздравлю тебя {month}.{day} {discord.utils.get(self.bot.emojis, name='lewd')}",
                    f"Все зайка моя поздравлю тебя, вот такое лицо будет {discord.utils.get(self.bot.emojis, name='ahuet')}",
                    f"Радость моя, поздравлю тебя в твой лучший день {discord.utils.get(self.bot.emojis, name='giggle')}"
                ]))

    @add_birthday_date.error
    async def add_birthday_date_error(self, ctx, error):
        async with ctx.typing():
            if isinstance(error, commands.MissingRequiredArgument):
                return await ctx.send(choice([
                    "Заебись команда, правда? Только сынок блять мне бы еще день и месяц знать", "Бля я чо телепат ебанный, день и месяц то какой", "Сука внучок, дата то какая"
                ]))
            if isinstance(error, commands.BadArgument):
                await ctx.send(choice([
                    "Ебать ты меня говном накормил, нахуй ты это сделал", "Вот пидор, старичка говном кормит, молодеж блять"
                ]))
