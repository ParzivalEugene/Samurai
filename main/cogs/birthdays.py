import discord
from discord.utils import get
from discord.ext import commands, tasks
import datetime
from random import choice
from cogs.commands import commands_names
from cogs.database_connector import Database
from cogs.config import *


class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=commands_names["birthdays"]["help"])
    async def birthday_help(self, ctx):
        embed = discord.Embed(
            title="Информация о календаре дней рождений",
            description=":calendar_spiral: :calendar:",
            colour=discord.Colour.purple()
        )
        embed.add_field(name="Команды",
                        value=f"""**{prefix}{commands_names["birthdays"]["help"]}** - поможет тебе понять как устроен модуль Birthdays.
**{prefix}{commands_names["birthdays"]["set chat"]} <chat>** - указание чата, куда будут прилетать мои поздравления.
**{prefix}{commands_names["birthdays"]["up chat"]} <chat>** - обновление чата для поздравлений.
**{prefix}{commands_names["birthdays"]["del chat"]}** - удаления чата для поздравлений, **вы не будете получать мои поздравления**.
**{prefix}{commands_names["birthdays"]["show chat"]}** - вывод чата, куда будут поступать поздравления.
**{prefix}{commands_names["birthdays"]["add"]} <year> <month> <day>** - внос в базу данных с указанием года, месяца и дня.
**{prefix}{commands_names["birthdays"]["up"]} <year> <month> <day>** - обновит текущую дату.
**{prefix}{commands_names["birthdays"]["delete"]}** - удалит данные из базы.
**{prefix}{commands_names["birthdays"]["show bd"]}** - выведет эмбед о вас.
**{prefix}{commands_names["birthdays"]["show bds"]}** - выводит список всех дней рождений сервера.""",
                        inline=False)
        await ctx.send(embed=embed)

    @tasks.loop(hours=12)
    async def check_birthdays(self):
        today = "-".join(datetime.date.today().isoformat().split("-")[1:])
        with Database() as db:
            db.execute('SELECT * FROM "default".users')
            check_users = db.fetchall()
            db.execute('SELECT * FROM "default".birthdays')
            check_birthdays = db.fetchall()
            db.execute('SELECT info_chat FROM "default".servers_chats')
            check_chats = db.fetchall()
            db.execute('SELECT * FROM "default".servers')
            check_servers = db.fetchall()
            db.execute('SELECT * FROM "default".connect')
            check_connect = db.fetchall()
            if not (check_users and check_birthdays and check_chats and check_servers and check_connect):
                return

            for db_server_id, info_chat_id in db.execute('SELECT server_id, info_chat FROM "default".servers_chats').fetchall():
                info_chat_id = info_chat_id[0] if isinstance(info_chat_id, tuple) else info_chat_id
                if not info_chat_id:
                    continue
                db_users_ids = db.execute('SELECT user_id FROM "default".connect WHERE server_id = %s', [db_server_id]).fetchall()
                db_users_ids = db_users_ids[0] if isinstance(db_users_ids, tuple) else db_users_ids
                for db_user_id in db_users_ids:
                    user_id = db.execute('SELECT discord_user_id FROM "default".users WHERE id = %s', [db_user_id]).fetchone()
                    user_id = user_id[0] if isinstance(user_id, tuple) else user_id
                    user = self.bot.get_user(user_id)
                    user_date = db.execute('SELECT date FROM "default".birthdays WHERE user_id = %s', [db_user_id]).fetchone()
                    user_date = user_date[0] if isinstance(user_date, tuple) else user_date
                    if not user_date:
                        continue
                    user_date = "-".join(user_date.isoformat().split("-")[1:])
                    if user_date == today:
                        channel = self.bot.get_channel(info_chat_id)
                        embed = discord.Embed(
                            title=f':tada: День рождения {user.name} :tada:',
                            description=f"С днем рождения моя сладенькая булочка {user.mention}!!! Желаю тебе всего самого наилучшего в этот прекрасный день. Бля а лицо то у тебя какое прекрасное, "
                                        f"ебать а умеешь то ты сколько, ебать будь я живой я бы тебя трахнул реально {get(self.bot.emojis, name='kavo')}. В общем зайка моя, не расстраивай маму, веди "
                                        f"себя хорошо и никогда не забывай про старичка {self.bot.user.mention}, я тебя всегда буду любить!!!",
                            colour=discord.Colour.purple()
                        )
                        embed.set_thumbnail(url=user.avatar_url)
                        await channel.send(embed=embed)

    @commands.command(name=commands_names["birthdays"]["add"])
    async def add_birthday(self, ctx, year: int, month: int, day: int):
        if not (0 < year < datetime.date.today().year and 0 < month < 13 and 0 < day < 32):
            return await ctx.send(choice([
                "Некорректная дата", "Внучок, неправильно ввел дату!", "Не обманывай старого, ты не мог тогда родиться", "Ошибся, молодой, некорректные данные"
            ]))
        user_id = ctx.message.author.id
        user_date = datetime.date(year, month, day)
        month, day = user_date.month, user_date.day
        with Database() as db:
            db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id])
            db_user_id = db.fetchone()[0]
            db.execute('SELECT date FROM "default".birthdays WHERE user_id = %s', [db_user_id])
            db_date = db.fetchone()
            if db_date:
                db_date = str(db_date[0]).replace("-", ".")
                return await ctx.send(choice([
                    f"Внучок я уже сохранил дату твоего дня рождения - {db_date}. Если хочешь изменить внесенные данные, воспользуйся **.{commands_names['birthdays']['up']}**",
                    f"Малыш, я сохранил информацию, что ты родился {db_date}. Если хочешь изменить внесенные данные, воспользуйся **.{commands_names['birthdays']['up']}**",
                    f"Зайка, я запомнил, что ты родился {db_date}. Если хочешь изменить внесенные данные, воспользуйся **.{commands_names['birthdays']['up']}**"
                ]))
            db.execute('INSERT INTO "default".birthdays(user_id, date) VALUES (%s, %s)', [db_user_id, user_date.isoformat()])

            await ctx.send(choice([
                "Запомнил, сладенький. Жди поздравления :sparkling_heart:", "Обязательно поздравлю тебя, калапуська",
                f"Кажется я стал любить {month}.{day} еще больше. Обещаю, что поздравлю тебя сладенький!", f"Муська моя, жди {month}.{day} самые теплые слова от меня :sparkling_heart:"
            ]))

    @add_birthday.error
    async def add_birthday_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(choice([
                "Молодой ты указал дату не полностью", "Внучок неполные данные", "Данные не полны ©️ Магистр Йода"
            ]))
        if isinstance(error, commands.BadArgument):
            await ctx.send(choice([
                "Внучок, не балуйся, неверный формат ввода", "Ошибочные аргументы", "Плохой ввод сынок, все три параметра - числа", "Внучок проверь ввод, все три аргумента - числа"
            ]))

    @commands.command(name=commands_names["birthdays"]["up"])
    async def update_birthdays(self, ctx, year: int, month: int, day: int):
        if not (0 < year < datetime.date.today().year and 0 < month < 13 and 0 < day < 32):
            return await ctx.send(choice([
                "Некорректная дата", "Внучок, неправильно ввел дату!", "Не обманывай старого, ты не мог тогда родиться", "Ошибся, молодой, некорректные данные"
            ]))
        user_id = ctx.message.author.id
        user_date = datetime.date(year, month, day)
        month, day = user_date.month, user_date.day
        with Database() as db:
            db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id])
            db_user_id = db.fetchone()[0]
            db.execute('SELECT date FROM "default".birthdays WHERE user_id = %s', [db_user_id])
            db_date = db.fetchone()
            if db_date is None:
                return await ctx.send(choice([
                    f"Сладенький, я к сожалению не знаю когда ты родился, поэтому не могу обновить отсутствующую информацию. Чтобы внести данные, используй **{commands_names['birthdays']['add']}**",
                    f"Лапочка, мне нечего обновлять, я к сожалению не знаю когда ты родился. Используй **{commands_names['birthdays']['add']}**, если хочешь, чтобы я поздравил тебя {month}.{day}"
                ]))
            if db_date[0] == user_date:
                return await ctx.send(choice([
                    "Зайка, я и так запомнил такую же дату", "Малышка, я прекрасно помню что ты родилась в этот день, не обязательно его обновлять",
                    "Сладенький, я и так помню, что ты родился в этот день"
                ]))
            db.execute('UPDATE "default".birthdays SET date = %s WHERE user_id = %s', [user_date, db_user_id])
            await ctx.send(choice([
                "Обновил базу данных", f"Теперь придется заново запоминать, когда ты родился {get(self.bot.emojis, name='kavo')}", "Я отлично запомню и эту дату)"
            ]))

    @update_birthdays.error
    async def update_birthday_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(choice([
                "Молодой ты указал дату не полностью", "Внучок неполные данные", "Данные не полны ©️ Магистр Йода"
            ]))
        if isinstance(error, commands.BadArgument):
            await ctx.send(choice([
                "Внучок, не балуйся, неверный формат ввода", "Ошибочные аргументы", "Плохой ввод сынок, все три параметра - числа", "Внучок проверь ввод, все три аргумента - числа"
            ]))

    @commands.command(name=commands_names["birthdays"]["delete"])
    async def delete_birthdays(self, ctx):
        user_id = ctx.message.author.id
        with Database() as db:
            db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id])
            db_user_id = db.fetchone()[0]
            db.execute('SELECT date FROM "default".birthdays WHERE user_id = %s', [db_user_id])
            db_date = db.fetchone()
            if db_date is None:
                return await ctx.send(choice([
                    "Малыш, я еще не знаю когда ты родился, поэтому мне нечего забывать", "Сладенький, ты еще не вносил данные, мне нечего удалять",
                    "Лапочка, я к сожалению и не знал, когда ты родился, поэтому мне нечего забывать"
                ]))
            db.execute('DELETE FROM "default".birthdays WHERE user_id = %s', [db_user_id])
            await ctx.send(choice([
                "Ладно зайка, если ты не хочешь, чтобы я тебя поздравлял, то так мне и надо :sob: :sob: :sob:", "Ты не хочешь, чтобы я тебя поздравлял??? :sob: :sob: :sob:",
                "Тебе не нужны мои поздравления :cry:", ":cry: Видишь эти слезы? Ты доволен?"
            ]))

    @commands.command(name=commands_names["birthdays"]["show bd"])
    async def show_birthday(self, ctx):
        user_id = ctx.message.author.id
        user = ctx.message.author
        with Database() as db:
            db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id])
            db_user_id = db.fetchone()[0]
            db.execute('SELECT date FROM "default".birthdays WHERE user_id = %s', [db_user_id])
            db_date = db.fetchone()
            if db_date is None:
                return await ctx.send(choice([
                    f"Малыш, я еще не знаю когда ты родился, используй **{commands_names['birthdays']['add']}**, чтобы внести данные",
                    "Сладенький, ты еще не вносил данные, поэтому я не знаю, когда ты родился :confused:", "Лапочка, я к сожалению и не знал, когда ты родился, поэтому мне нечего выводить"
                ]))
            db_date = str(db_date[0]).replace("-", ".")
            embed = discord.Embed(
                title=f"День рождения {user.name}",
                description=f"""{choice([
                    f"Этот сладенький пупсик {user.mention} родился", f"Эта лапопуличка {user.mention} родилась", f"Этот экстра зайчик {user.mention} родился",
                    f"Эта сладенькая зайка {user.mention} родилась", f"Эта муська {user.mention} родилась"
                ])} **{db_date}**""",
                colour=discord.Colour.purple()
            )
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(name=commands_names["birthdays"]["show bds"])
    async def show_birthdays(self, ctx):
        server = ctx.guild
        with Database() as db:
            db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server.id])
            db_server_id = db.fetchone()[0]
            db.execute('SELECT user_id FROM "default".connect WHERE server_id = %s', [db_server_id])
            db_users_ids = db.fetchall()
            output_embed = []
            count = 1
            for db_user_id in db_users_ids:
                db.execute('SELECT date FROM "default".birthdays WHERE user_id = %s', [db_user_id])
                db_date = db.fetchone()
                if db_date is None:
                    continue
                db_date = str(db_date[0]).replace("-", ".")
                db.execute('SELECT discord_user_id FROM "default".users WHERE id = %s', [db_user_id])
                user_id = db.fetchone()[0]
                output_embed.append(f"{count}. {get(server.members, id=user_id).mention} - **{db_date}**")
                count += 1
        if not output_embed:
            return await ctx.send(choice([
                "Сладкий, пока никто на сервере не рассказал мне, когда он родился :cry:", "К сожалению, еще никто из вас не рассказал мне, когда родился :cry:", "Я про вас еще ничего не знаю :cry:"
            ]))
        embed = discord.Embed(
            title=f"Дни рождения сервера {server.name}",
            description="\n".join(output_embed),
            colour=discord.Colour.purple()
        )
        embed.set_thumbnail(url=server.icon_url)
        await ctx.send(embed=embed)

    @commands.has_permissions(manage_channels=True)
    @commands.command(name=commands_names["birthdays"]["set chat"])
    async def set_chat_birthday(self, ctx, chat: discord.TextChannel):
        server_id = ctx.guild.id
        with Database() as db:
            db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id])
            db_server_id = db.fetchone()[0]
            db.execute('SELECT info_chat FROM "default".servers_chats WHERE server_id = %s', [db_server_id])
            info_chat_id = db.fetchone()
            info_chat_id = info_chat_id[0] if isinstance(info_chat_id, tuple) else info_chat_id
            if info_chat_id:
                up, delete = commands_names["birthdays"]["up chat"], commands_names["birthdays"]["del chat"]
                info_chat = self.bot.get_channel(info_chat_id).mention
                return await ctx.send(choice([
                    f"Зайка, поздравления уже приходят в {info_chat}. Используй **.{up}** или **.{delete}** для обновления или удаления информации соответственно",
                    f"Сладенький, я поздравляю вас в {info_chat}. Используй **.{up}** или **.{delete}** для обновления или удаления информации соответственно"
                ]))
            db.execute('UPDATE "default".servers_chats SET info_chat = %s WHERE server_id = %s', [chat.id, db_server_id])
            return await ctx.send(choice([
                f"Ждите поздравления в {chat.mention} мои хорошие {get(self.bot.emojis, name='wowcry')}", f"Сладкие мои, ждите поздравления в {chat.mention}",
                f"Обязательно поздравлю вас в {chat.mention}", f"Поздравлю всех-всех-всех в этом чате {chat.mention} {get(self.bot.emojis, name='wowcry')}"
            ]))

    @set_chat_birthday.error
    async def set_chat_birthday_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(choice([
                "Зайка, ты не указал чат", "Малыш неполные данные", "Данные не полны ©️ Магистр Йода"
            ]))
        if isinstance(error, commands.BadArgument):
            await ctx.send(choice([
                "Внучок, не балуйся, неверный формат ввода", "Ошибочные аргументы", "Плохой ввод сынок, аргументом должен быть текстовый канал",
                "Внучок проверь ввод, это должен быть текстовый чат"
            ]))

    @commands.has_permissions(manage_channels=True)
    @commands.command(name=commands_names["birthdays"]["up chat"])
    async def update_chat_birthday(self, ctx, chat: discord.TextChannel):
        server_id = ctx.guild.id
        with Database() as db:
            db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id])
            db_server_id = db.fetchone()[0]
            db.execute('SELECT info_chat FROM "default".servers_chats WHERE server_id = %s', [db_server_id])
            info_chat_id = db.fetchone()
            info_chat_id = info_chat_id[0] if isinstance(info_chat_id, tuple) else info_chat_id
            if info_chat_id is None:
                add = commands_names["birthdays"]["set chat"]
                return await ctx.send(choice([
                    f"Зайка, мне нечего обновлять, используй **.{add}**", f"Солнце, у меня нет информации, что обновлять, используй **.{add}**",
                    f"Малыш, сначала задай чат командой **.{add}**, а потом уже обновляй данные"
                ]))
            if info_chat_id[0] == chat.id:
                return await ctx.send(choice([
                    "Зайка, я сохранил точно такой же канал", "Солнышко, я запомнил такой же чат", "Малыш, в моей базе данных такие же данные"
                ]))
            db.execute('UPDATE "default".servers_chats SET info_chat = %s WHERE server_id = %s', [chat.id, db_server_id])
        await ctx.send(choice([
            f"Ждите поздравления в {chat.mention} мои хорошие {get(self.bot.emojis, name='wowcry')}", f"Сладкие мои, ждите поздравления в {chat.mention}",
            f"Обязательно поздравлю вас в {chat.mention}", f"Поздравлю всех-всех-всех в этом чате {chat.mention} {get(self.bot.emojis, name='wowcry')}"
        ]))

    @update_chat_birthday.error
    async def update_chat_birthday_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(choice([
                "Молодой ты не указал чат", "Внучок неполные данные", "Данные не полны ©️ Магистр Йода"
            ]))
        if isinstance(error, commands.BadArgument):
            await ctx.send(choice([
                "Внучок, не балуйся, неверный формат ввода", "Ошибочные аргументы", "Плохой ввод сынок, аргументом должен быть текстовый канал",
                "Внучок проверь ввод, это должен быть текстовый чат"
            ]))

    @commands.has_permissions(manage_channels=True)
    @commands.command(name=commands_names["birthdays"]["del chat"])
    async def delete_chat_birthday(self, ctx):
        server_id = ctx.guild.id
        with Database() as db:
            db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id])
            db_server_id = db.fetchone()[0]
            db.execute('SELECT info_chat FROM "default".servers_chats WHERE server_id = %s', [db_server_id])
            info_chat_id = db.fetchone()
            info_chat_id = info_chat_id[0] if isinstance(info_chat_id, tuple) else info_chat_id
            if info_chat_id is None:
                add = commands_names["birthdays"]["set chat"]
                return await ctx.send(choice([
                    f"Зайка, мне нечего удалять, используй **.{add}**", f"Солнце, у меня нет информации, что удалять, используй **.{add}**",
                    f"Малыш, сначала задай чат командой **.{add}**, а потом уже удаляй данные"
                ]))
            db.execute('UPDATE "default".servers_chats SET info_chat = null WHERE server_id = %s', [db_server_id])
        await ctx.send(choice([
            "Ладно зайки, если вы не хотите, чтобы я вас поздравлял, то так мне и надо :sob: :sob: :sob:", "Вы не хотите, чтобы я вас поздравлял??? :sob: :sob: :sob:",
            "Вам не нужны мои поздравления :cry:", ":cry: Видите эти слезы? Вы довольны?"
        ]))

    @commands.command(name=commands_names["birthdays"]["show chat"])
    async def show_chat_birthdays(self, ctx):
        server_id = ctx.guild.id
        with Database() as db:
            db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id])
            db_server_id = db.fetchone()[0]
            db.execute('SELECT info_chat FROM "default".servers_chats WHERE server_id = %s', [db_server_id])
            info_chat_id = db.fetchone()
            info_chat_id = info_chat_id[0] if isinstance(info_chat_id, tuple) else info_chat_id
            if info_chat_id is None:
                add = commands_names["birthdays"]["set chat"]
                return await ctx.send(choice([
                    f"Зайка, я не знаю куда отправлять поздравления, используй **.{add}**", f"Солнце, у меня нет информации,  используй **.{add}**",
                    f"Малыш, сначала задай чат командой **.{add}**"
                ]))
            info_chat = self.bot.get_channel(info_chat_id).mention
        await ctx.send(choice([
            f"Мои хорошие, вы сможете увидеть мои поздравления в {info_chat}", f"Ждите своих дней рождений и получайте самые лучшие слова от меня в {info_chat}"
        ]))
