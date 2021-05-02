import discord
from discord.ext import commands, tasks
from datetime import date
import sqlite3
import os
from random import choice
from cogs.commands import commands_names
from cogs.config import *


class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(hours=12)
    async def check_birthday(self):
        today = "-".join(date.today().isoformat().split("-")[1:])

    @commands.command(name=commands_names["birthdays"]["help"])
    async def rules_birthday(self, ctx):
        embed = discord.Embed(
            title="Информация о календаре дней рождений",
            description=":calendar_spiral: :calendar:",
            colour=discord.Colour.purple()
        )
        embed.add_field(name="Команды",
                        value=f"""**{prefix}{commands_names["birthdays"]["help"]}** - поможет тебе понять как устроен модуль Birthdays.
**{prefix}{commands_names["birthdays"]["add"]} <year> <month> <day>** - внос в базу данных с указанием года, месяца и дня.
**{prefix}{commands_names["birthdays"]["up"]} <year> <month> <day>** - обновит текущую дату.
**{prefix}{commands_names["birthdays"]["delete"]}** - удалит данные из базы.
**{prefix}{commands_names["birthdays"]["show bd"]}** - выведет эмбед о вас.
**{prefix}{commands_names["birthdays"]["show bds"]}** - выводит список всех дней рождений сервера.""",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(name=commands_names["birthdays"]["add"])
    async def add_birthday(self, ctx, year: int, month: int, day: int):
        user_id = ctx.message.author.id
        guild_id = ctx.guild.id
        conn = sqlite3.connect(os.path.abspath("database/samurai.db"))
        cursor = conn.cursor()

        check_user = cursor.execute("SELECT id FROM user WHERE user_id = ?", (user_id,)).fetchone()
        if not check_user:
            cursor.execute("INSERT INTO user(user_id) VALUES(?)", (user_id,))
        check_server = cursor.execute("SELECT id FROM server WHERE server_id = ?", (guild_id,)).fetchone()
        if not check_server:
            cursor.execute("INSERT INTO server(server_id) VALUES(?)", (guild_id,))
        db_server_id = check_server[0] if isinstance(check_server, tuple) else check_server
        db_user_id = check_user[0] if isinstance(check_user, tuple) else check_user
        if not cursor.execute("SELECT id FROM connect WHERE server_id = ? and user_id = ?", (db_server_id, db_user_id)).fetchall():
            cursor.execute("INSERT INTO connect(server_id, user_id) VALUES(?,?)", (db_server_id, db_user_id))
        check_date = cursor.execute("SELECT * FROM birthdays WHERE id = ?", (db_user_id,)).fetchone()
        if check_date:
            return await ctx.send(choice([
                f"Внучок, твоя дата уже есть, юзай **{commands_names['birthdays']['up']}**", f"Молодой, ты уже есть в базе, юзай **{commands_names['birthdays']['up']}**",
                f"Старичок, ты уже вносил данные, юзай **{commands_names['birthdays']['up']}** или **{commands_names['birthdays']['delete']}**", "Внучок, по тебе уже есть инфа"
            ]))
        if not (0 < year < 2020 and 0 < month < 13 and 0 < day < 32):
            return await ctx.send(choice([
                "Внучок, не обманывай старого, неверный ввод", "Молодежь над дедом издевается, неправильный ввод", "Сынок, неправильно данные ввел", "Внучок, ты не мог тогда родиться"
            ]))

        user_date = date(year, month, day).isoformat()
        cursor.execute("INSERT INTO birthdays(id,date) VALUES(?,?)", (db_user_id, user_date))
        conn.commit()
        conn.close()
        await ctx.send(choice([
            "Внучок, успешно добавил дату, жди поздравления :sparkling_heart:", "Сынок, дату добавил, поздравлю тебя в этот день!", "Ну все, можешь ждать от меня поздравления!",
            "Обязательно поздравлю тебя в этот день!"
        ]))

    @add_birthday.error
    async def add_birthday_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(choice([
                "Молодой ты указал дату неполностью", "Внучок неполные данные", "Данные не полны ©️ Магистр Йода"
            ]))
        if isinstance(error, commands.BadArgument):
            await ctx.send(choice([
                "Внучок, не балуйся, неверный формат ввода", "Ошибочные аргументы", "Плохой ввод сынок, все три параметра числа", "Внучок проверь ввод, все три аргемента числа"
            ]))

    @commands.command(name=commands_names["birthdays"]["up"])
    async def update_birthdays(self, ctx, year: int, month: int, day: int):
        user_id = ctx.message.author.id
        guild_id = ctx.guild.id
        conn = sqlite3.connect(os.path.abspath("database/samurai.db"))
        cursor = conn.cursor()

        check_user = cursor.execute("SELECT id FROM user WHERE user_id = ?", (user_id,)).fetchone()
        if not check_user:
            cursor.execute("INSERT INTO user(user_id) VALUES(?)", (user_id,))
        check_server = cursor.execute("SELECT id FROM server WHERE server_id = ?", (guild_id,)).fetchone()
        if not check_server:
            cursor.execute("INSERT INTO server(server_id) VALUES(?)", (guild_id,))
        db_server_id = check_server[0] if isinstance(check_server, tuple) else check_server
        db_user_id = check_user[0] if isinstance(check_user, tuple) else check_user
        if not cursor.execute("SELECT id FROM connect WHERE server_id = ? and user_id = ?", (db_server_id, db_user_id)).fetchall():
            cursor.execute("INSERT INTO connect(server_id, user_id) VALUES(?,?)", (db_server_id, db_user_id))
        check_date = cursor.execute("SELECT * FROM birthdays WHERE id = ?", (db_user_id,)).fetchone()
        if not check_date:
            return await ctx.send(choice([
                f"Внучок, твоей даты еще нет, юзай **{commands_names['birthdays']['add']}**", f"Молодой, тебя еще нет в базе, юзай **{commands_names['birthdays']['add']}**",
                f"Старичок, ты еще не вносил данные, юзай **{commands_names['birthdays']['add']}**",
                f"Внучок, по тебе еще нет есть инфы, обновлять нечего {discord.utils.get(self.bot.emojis, name='ahuet')}"
            ]))
        if not (0 < year < 2020 and 0 < month < 13 and 0 < day < 32):
            return await ctx.send(choice([
                "Внучок, не обманывай старого, неверный ввод", "Молодежь над дедом издевается, неправильный ввод", "Сынок, неправильно данные ввел", "Внучок, ты не мог тогда родиться"
            ]))

        current_date = cursor.execute("SELECT date FROM birthdays WHERE id = ?", (db_user_id,)).fetchone()
        if isinstance(current_date, tuple):
            current_date = current_date[0]
        user_date = date(year, month, day).isoformat()
        if current_date == user_date:
            return await ctx.send(choice([
                "Внучок, ты ввел те же данные, что у меня есть", "Апдейт ничем не отличается от текущих данных", "У меня в базе такие же данные",
                "Апдейта не будет, он принял ислам. Внучок, данные те же что и в базе"
            ]))
        cursor.execute("UPDATE birthdays SET date = ? WHERE id = ?", (user_date, db_user_id))
        conn.commit()
        conn.close()
        await ctx.send(choice([
            f"Внучок, успешно обновил данные с {current_date} на {user_date}", f"Обновил данные с {current_date} на {user_date}", f"Апдейт прошел успешно с {current_date} на {user_date}",
        ]))

    @update_birthdays.error
    async def update_birthday_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(choice([
                "Молодой ты указал дату неполностью", "Внучок неполные данные", "Данные не полны ©️ Магистр Йода"
            ]))
        if isinstance(error, commands.BadArgument):
            await ctx.send(choice([
                "Внучок, не балуйся, неверный формат ввода", "Ошибочные аргументы", "Плохой ввод сынок, все три параметра числа", "Внучок проверь ввод, все три аргемента числа"
            ]))

    @commands.command(name=commands_names["birthdays"]["delete"])
    async def delete_birthdays(self, ctx):
        user_id = ctx.message.author.id
        guild_id = ctx.guild.id
        conn = sqlite3.connect(os.path.abspath("database/samurai.db"))
        cursor = conn.cursor()

        check_user = cursor.execute("SELECT id FROM user WHERE user_id = ?", (user_id,)).fetchone()
        if not check_user:
            cursor.execute("INSERT INTO user(user_id) VALUES(?)", (user_id,))
        check_server = cursor.execute("SELECT id FROM server WHERE server_id = ?", (guild_id,)).fetchone()
        if not check_server:
            cursor.execute("INSERT INTO server(server_id) VALUES(?)", (guild_id,))
        db_server_id = check_server[0] if isinstance(check_server, tuple) else check_server
        db_user_id = check_user[0] if isinstance(check_user, tuple) else check_user
        if not cursor.execute("SELECT id FROM connect WHERE server_id = ? and user_id = ?", (db_server_id, db_user_id)).fetchall():
            cursor.execute("INSERT INTO connect(server_id, user_id) VALUES(?,?)", (db_server_id, db_user_id))
        check_date = cursor.execute("SELECT * FROM birthdays WHERE id = ?", (db_user_id,)).fetchone()
        if not check_date:
            return await ctx.send(choice([
                f"Внучок, твоей даты еще нет, юзай **{commands_names['birthdays']['add']}**", f"Молодой, тебя еще нет в базе, юзай **{commands_names['birthdays']['add']}**",
                f"Старичок, ты еще не вносил данные, юзай **{commands_names['birthdays']['add']}**",
                f"Внучок, по тебе еще нет есть инфы, удалять нечего {discord.utils.get(self.bot.emojis, name='ahuet')}"
            ]))

        cursor.execute("DELETE FROM birthdays WHERE id = ?", (db_user_id,))
        conn.commit()
        conn.close()
        await ctx.send(choice([
            "Все сынок, удалил тебя из базы", "Успешно удалил данные", "Ты не хочешь чтобы я тебя поздравлял?((", ""
        ]))

    @commands.command(name=commands_names["birthdays"]["show bd"])
    async def show_birthday(self, ctx):
        user_id = ctx.message.author.id
        user = ctx.message.author
        guild_id = ctx.guild.id
        conn = sqlite3.connect(os.path.abspath("database/samurai.db"))
        cursor = conn.cursor()

        check_user = cursor.execute("SELECT id FROM user WHERE user_id = ?", (user_id,)).fetchone()
        if not check_user:
            cursor.execute("INSERT INTO user(user_id) VALUES(?)", (user_id,))
        check_server = cursor.execute("SELECT id FROM server WHERE server_id = ?", (guild_id,)).fetchone()
        if not check_server:
            cursor.execute("INSERT INTO server(server_id) VALUES(?)", (guild_id,))
        db_server_id = check_server[0] if isinstance(check_server, tuple) else check_server
        db_user_id = check_user[0] if isinstance(check_user, tuple) else check_user
        if not cursor.execute("SELECT id FROM connect WHERE server_id = ? and user_id = ?", (db_server_id, db_user_id)).fetchall():
            cursor.execute("INSERT INTO connect(server_id, user_id) VALUES(?,?)", (db_server_id, db_user_id))
        check_date = cursor.execute("SELECT * FROM birthdays WHERE id = ?", (db_user_id,)).fetchone()
        if not check_date:
            return await ctx.send(choice([
                f"Внучок, твоей даты еще нет, юзай **{commands_names['birthdays']['add']}**", f"Молодой, тебя еще нет в базе, юзай **{commands_names['birthdays']['add']}**",
                f"Старичок, ты еще не вносил данные, юзай **{commands_names['birthdays']['add']}**",
                f"Внучок, по тебе еще нет инфы, удалять нечего {discord.utils.get(self.bot.emojis, name='ahuet')}"
            ]))

        current_date = cursor.execute("SELECT date FROM birthdays WHERE id = ?", (db_user_id,)).fetchone()
        if isinstance(current_date, tuple):
            current_date = current_date[0]
        embed = discord.Embed(
            title=f"{user.name} - Date of Birth",
            description=f"""{choice([
                f"Этот сладенький пупсик {user.mention} родился", f"Эта лапопуличка {user.mention} родилась", f"Этот экстра зайчик {user.mention} родился", 
                f"Эта сладенькая зайка {user.mention} родилась", f"Эта муська {user.mention} родилась"
            ])} **{current_date}**""",
            colour=discord.Colour.purple()
        )
        embed.set_thumbnail(url=user.avatar_url)
        conn.commit()
        conn.close()
        await ctx.send(embed=embed)

    @commands.command(name=commands_names["birthdays"]["show bds"])
    async def show_birthdays(self, ctx):
        user_id = ctx.message.author.id
        user = ctx.message.author
        guild_id = ctx.guild.id
        guild = ctx.guild
        conn = sqlite3.connect(os.path.abspath("database/samurai.db"))
        cursor = conn.cursor()

        check_user = cursor.execute("SELECT id FROM user WHERE user_id = ?", (user_id,)).fetchone()
        if not check_user:
            cursor.execute("INSERT INTO user(user_id) VALUES(?)", (user_id,))
        check_server = cursor.execute("SELECT id FROM server WHERE server_id = ?", (guild_id,)).fetchone()
        if not check_server:
            cursor.execute("INSERT INTO server(server_id) VALUES(?)", (guild_id,))
        db_server_id = check_server[0] if isinstance(check_server, tuple) else check_server
        db_user_id = check_user[0] if isinstance(check_user, tuple) else check_user
        if not cursor.execute("SELECT id FROM connect WHERE server_id = ? and user_id = ?", (db_server_id, db_user_id)).fetchall():
            cursor.execute("INSERT INTO connect(server_id, user_id) VALUES(?,?)", (db_server_id, db_user_id))

        check_users = cursor.execute("SELECT user_id FROM connect WHERE server_id = (SELECT id FROM server WHERE server_id = ?)", (guild_id,)).fetchall()
        db_users_id = [i[0] for i in check_users]
        dates = cursor.execute(f"SELECT id,date FROM birthdays WHERE id IN ({','.join(['?'] * len(db_users_id))})", db_users_id).fetchall()
        db_user_id = [i[0] for i in dates]
        users = cursor.execute(f"SELECT user_id FROM user WHERE id IN ({','.join(['?'] * len(db_user_id))})", db_user_id).fetchall()
        dates = [i[1] for i in dates]
        users = [i[0] for i in users]
        conn.commit()
        conn.close()
        output = []
        for i in range(len(dates)):
            output.append(f"**{discord.utils.get(guild.members, id=users[i]).mention}** - **{dates[i]}**")
        if not output:
            output = "Пока данных нет"
        embed = discord.Embed(
            title=f"{guild.name} Dates of Birth",
            description="\n".join(output) if isinstance(output, list) else output,
            colour=discord.Colour.purple()
        )
        embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)

    # @tasks.loop(hours=12)
    # async def check_birthday(self):
    #     today = str(date.today())[5:]
    #     table = []
    #     with open("database/birthdays.json", "r") as input_file:
    #         data = json.load(input_file)
    #         for i in range(len(data["bd"])):
    #             info = list(data["bd"][i].keys())[0]
    #             month, day = data["bd"][i][info]["month"], data["bd"][i][info]["day"]
    #             current_date = date(2021, month, day).isoformat()[5:]
    #             table.append([current_date, info])
    #     for i in table:
    #         if i[0] == today and i[1] != "test":
    #             embed = discord.Embed(
    #                 title=f"С ДНЕМ РОЖДЕНИЯ WARRIOR <@{i[1]}>",
    #                 description=":sweat_drops: :sweat_drops: :sweat_drops:",
    #                 colour=discord.Colour.purple()
    #             )
    #             embed.add_field(name="Блять какой же ты все таки ахуенный(-ая)",
    #                             value="Поздравляю тебя с этим заебубительным днем. Желаю тебе счастья блять, радости, вот этой всей вашей человечей хуйни. Но никогда не забывай об этом сервере, "
    #                                   "здесь тебе всегда будут рады.",
    #                             inline=False)
    #             await self.bot.get_channel(778544220054224906).send(embed=embed)
