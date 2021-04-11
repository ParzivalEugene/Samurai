import discord
from discord.ext import commands, tasks
from datetime import date
import json
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

    @commands.command(name="bd_rules")
    async def rules_birthday(self, ctx):
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

    @commands.command(name="bd_show")
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

    @commands.command(name="bd")
    async def add_birthday_date(self, ctx, month: int, day: int):
        if not any(i.id == 778542601690284034 for i in ctx.author.roles):
            await ctx.send("У вас недостачно высокая роль для этой команды")
            return
        with open("database/birthdays.json") as info:
            birthdays = json.load(info)
            if any(str(ctx.author.id) in i.keys() for i in birthdays["bd"]):
                await ctx.send("Вы уже указали свою дату")
                return
            if not (1 <= month <= 12 or 1 <= day <= 31):
                await ctx.send("Вы указали неверную дату")
                return
            birthdays["bd"].append({ctx.author.id: {"month": month, "day": day}})
            with open("database/birthdays.json", "w") as outfile:
                json.dump(birthdays, outfile)
            await ctx.send("Данные успешно внесены")

    @add_birthday_date.error
    async def add_birthday_date_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Вы указали неполную дату")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Вы указали неверную дату")
