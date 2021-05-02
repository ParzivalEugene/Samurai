import discord
from discord.ext import commands
from cogs.commands import commands_names
from cogs.config import prefix
import sqlite3
from random import choice
import os


class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def check_level_up(self, message):
        if message.author == self.bot.user:
            return
        user_id = message.author.id
        user = message.author
        guild_id = message.guild.id
        guild = message.guild
        conn = sqlite3.connect(os.path.abspath("database/samurai.db"))
        cursor = conn.cursor()
        check_user_id = cursor.execute("SELECT id FROM user WHERE user_id = ?", (user_id,)).fetchone()
        if not check_user_id:
            cursor.execute("INSERT INTO user(user_id) VALUES(?)", (user_id,))
        check_xp = cursor.execute("SELECT xp FROM user_levels WHERE id = (SELECT id FROM user WHERE user_id = ?)", (user_id,)).fetchone()
        if not check_xp:
            cursor.execute("INSERT INTO user_levels(id,xp) VALUES((SELECT id FROM user WHERE user_id = ?),?)", (user_id, 0))
        xp = cursor.execute("SELECT xp FROM user_levels WHERE id = (SELECT id FROM user WHERE user_id = ?)", (user_id,)).fetchone()[0]
        cursor.execute("UPDATE user_levels SET xp = ? WHERE id = (SELECT id FROM user WHERE user_id = ?)", (xp + 1, user_id))
        check_server = cursor.execute("SELECT id FROM server WHERE server_id = ?", (guild_id,)).fetchone()
        if not check_server:
            cursor.execute("INSERT INTO server(server_id) VALUES(?)", (guild_id,))
        server = cursor.execute("SELECT id FROM server WHERE server_id = ?", (guild_id,)).fetchone()[0]
        check_levels = cursor.execute("SELECT * FROM levels WHERE id = (SELECT id FROM server WHERE server_id = ?)", (guild_id,)).fetchall()
        if not check_levels:
            print("здесь нет ролей")
            return
        xp += 1
        levels = cursor.execute("SELECT level_id, level_xp FROM levels WHERE id = (SELECT id FROM server WHERE server_id = ?) ORDER BY level_xp DESC", (guild_id,)).fetchall()
        for level, current_xp in levels:
            if discord.utils.get(guild.roles, id=level) in user.roles and xp < current_xp:
                xp = cursor.execute("SELECT level_xp FROM levels WHERE level_id = ?", (level,)).fetchone()[0]
                cursor.execute("UPDATE user_levels SET level = ?, xp = ?", (level, xp))
            if xp == current_xp:
                mention, current_role = message.author.mention, discord.utils.get(guild.roles, id=level).mention
                await message.channel.send(choice([
                    f"Поздравляю {mention}, ты заслужил повышение! Текущий уровень {current_role}", f"Пожилой {mention} повысился до {current_role}, мои поздравления!",
                    f"Эль негр {mention} апнулся до {current_role}!!! супер пупер пупсик"
                ]))
                cursor.execute("UPDATE user_levels SET level = ?", (level,))
                break
        db_server_id, db_user_id = server, cursor.execute("SELECT id FROM user WHERE user_id = ?", (user_id,)).fetchone()[0]
        if not cursor.execute("SELECT id FROM connect WHERE server_id = ? and user_id = ?", (db_server_id, db_user_id)).fetchall():
            cursor.execute("INSERT INTO connect(server_id,user_id) VALUES(?,?)", (db_server_id, db_user_id))
        conn.commit()
        conn.close()

    @commands.command(name=commands_names["level"]["help"])
    async def level_help(self, ctx):
        embed = discord.Embed(
            title="Информация о системе уровней",
            description=":bar_chart: :chart_with_upwards_trend: :chart_with_downwards_trend:",
            colour=discord.Colour.purple()
        )
        embed.add_field(name="Команды",
                        value=f"""**{prefix}{commands_names["level"]["help"]}** - поможет тебе понять как устроен модуль LevelSystem.
**{prefix}{commands_names["level"]["add"]} <role> <xp>** - внос в базу данных с указанием роли и количество опыта для ее получения.
**{prefix}{commands_names["level"]["up"]} <role> <xp>** - обновит данную роль.
**{prefix}{commands_names["level"]["delete"]}** - удалит роль из базы данных.
**{prefix}{commands_names["level"]["show levels"]}** - выведет список всех уровней сервера и количество опыта для их получения.
**{prefix}{commands_names["level"]["show level"]}** - выведет эмбед о вашем уровне.
**{prefix}{commands_names["level"]["dashboard"]}** - выведет топ участников сервера.""",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(name=commands_names["level"]["add"])
    @commands.has_permissions(manage_roles=True)
    async def level_add(self, ctx, role: discord.Role, level_xp: int):
        role_id = role.id
        user_id = ctx.message.author.id
        guild_id = role.guild.id
        conn = sqlite3.connect(os.path.abspath("database/samurai.db"))
        cursor = conn.cursor()
        server = cursor.execute("SELECT id FROM server WHERE server_id = ?", (guild_id,)).fetchone()
        if not server:
            cursor.execute("INSERT INTO server(server_id) VALUES(?)", (guild_id,))
            server = cursor.execute("SELECT id FROM server WHERE server_id = ?", (guild_id,)).fetchone()
        database_role = cursor.execute("SELECT id FROM levels WHERE level_id = ?", (role_id,)).fetchall()
        if database_role:
            return await ctx.send(choice([
                "Внучок, такой уровень", "Старичок, уровень уже есть, юзай команду **.level_update**", "Ебен бобен уже есть такой уровень", "Молодой я тут **добавляю** уровни, а не обновляю"
            ]))
        cursor.execute("INSERT INTO levels(id,level_id,level_xp) VALUES(?,?,?)", (server[0], role_id, level_xp))
        check_name = cursor.execute("SELECT id FROM user WHERE user_id = ?", (user_id,)).fetchone()
        if not check_name:
            cursor.execute("INSERT INTO user(user_id) VALUES(?)", (user_id,))
            check_name = cursor.execute("SELECT id FROM user WHERE user_id = ?", (user_id,)).fetchone()
        db_server_id, db_user_id = server[0], check_name[0]
        if not cursor.execute("SELECT id FROM connect WHERE server_id = ? and user_id = ?", (db_server_id, db_user_id)).fetchall():
            cursor.execute("INSERT INTO connect(server_id,user_id) VALUES(?,?)", (db_server_id, db_user_id))
        conn.commit()
        conn.close()
        await ctx.send(choice([
            f"Успешно добавил уровень {role.mention} в базу данных", f"Все внучок, внес {role.mention} в базу данных", f"Записал пожилую роль {role.mention} в базу данных"
        ]))

    @level_add.error
    async def level_add_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(choice([
                "Внучок, у тебя нет прав на редактирование уровней", "Братик ты не можешь менять уровни", "Молодой, тебе нельзя менять уровни"
            ]))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(choice([
                "Старичок мне нужна роль и количество очков, чтобы ее получить", "пожилой сюда надо роль и количество очков"
            ]))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(choice([
                "Бля ты какую то хуйню мне скормил, я сломался", "Не пихай сюда нихуя кроме ролей и уровня", "Внучок ебать не то в меня пихаешь, смотри **.help**"
            ]))

    @commands.has_permissions(manage_roles=True)
    @commands.command(name=commands_names["level"]["up"])
    async def level_update(self, ctx, role: discord.Role, level_xp: int):
        role_id = role.id
        user_id = ctx.message.author.id
        guild_id = role.guild.id
        conn = sqlite3.connect(os.path.abspath("database/samurai.db"))
        cursor = conn.cursor()
        server = cursor.execute("SELECT id FROM server WHERE server_id = ?", (guild_id,)).fetchone()
        if not server:
            cursor.execute("INSERT INTO server(server_id) VALUES(?)", (guild_id,))
            return await ctx.send(choice([
                "Пожилой я блять еще даже твой сервер в базу не внес, а ты команды апать просишь", "Дедуля блять я еще про этот сервер нихуя не знаю, не то что про команды"
            ]))
        database_role = cursor.execute("SELECT id FROM levels WHERE level_id = ?", (role_id,)).fetchone()
        if not database_role:
            return await ctx.send(choice([
                "Внучок таких ролей еще нет", "Пожилой мне нехуй апдейтить, еще нет такого уровня", "Бля сынок первый раз вижу этот уровень, юзай **.level_add**"
            ]))
        current_xp = cursor.execute("SELECT level_xp FROM levels WHERE level_id = ?", (role_id,)).fetchone()[0]
        if current_xp == level_xp:
            return await ctx.send(choice([
                f"Внучок, у этого уровня {role.mention} и так такое же количество опыта", f"Чтобы получить этот уровень {role.mention} нужно такое же количество опыта, в чем апдейт",
                "А в чем апдейт то, данные те же"
            ]))
        cursor.execute("UPDATE levels SET level_xp = ? WHERE level_id = ?", (level_xp, role_id))
        check_name = cursor.execute("SELECT id FROM user WHERE user_id = ?", (user_id,)).fetchone()
        if not check_name:
            cursor.execute("INSERT INTO user(user_id) VALUES(?)", (user_id,))
            check_name = cursor.execute("SELECT id FROM user WHERE user_id = ?", (user_id,)).fetchone()
        db_server_id, db_user_id = server[0], check_name[0]
        if not cursor.execute("SELECT id FROM connect WHERE server_id = ? and user_id = ?", (db_server_id, db_user_id)).fetchall():
            cursor.execute("INSERT INTO connect(server_id,user_id) VALUES(?,?)", (db_server_id, db_user_id))
        conn.commit()
        conn.close()
        await ctx.send(choice([
            f"Успешно обновил уровень {role.mention} с **{current_xp} xp** на **{level_xp} xp**", f"Внучок проапдейтил роль {role.mention}", f"Обновил уровень {role.mention} на **{current_xp} xp**"
        ]))

    @level_update.error
    async def level_update_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(choice([
                "Внучок, у тебя нет прав на редактирование уровней", "Братик ты не можешь менять уровни", "Молодой, тебе нельзя менять уровни"
            ]))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(choice([
                "Старичок мне нужна роль и количество очков, чтобы ее получить", "пожилой сюда надо роль и количество очков"
            ]))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(choice([
                "Бля ты какую то хуйню мне скормил, я сломался", "Не пихай сюда нихуя кроме ролей и уровня", "Внучок ебать не то в меня пихаешь, смотри **.help**"
            ]))

    @commands.has_permissions(manage_roles=True)
    @commands.command(name=commands_names["level"]["delete"])
    async def level_delete(self, ctx, role: discord.Role):
        role_id = role.id
        user_id = ctx.message.author.id
        guild_id = role.guild.id
        conn = sqlite3.connect(os.path.abspath("database/samurai.db"))
        cursor = conn.cursor()
        server = cursor.execute("SELECT id FROM server WHERE server_id = ?", (guild_id,)).fetchone()
        if not server:
            cursor.execute("INSERT INTO server(server_id) VALUES(?)", (guild_id,))
            return await ctx.send(choice([
                "Пожилой я блять еще даже твой сервер в базу не внес, а ты команды апать просишь", "Дедуля блять я еще про этот сервер нихуя не знаю, не то что про команды"
            ]))
        database_role = cursor.execute("SELECT id FROM levels WHERE level_id = ?", (role_id,)).fetchone()
        if not database_role:
            return await ctx.send(choice([
                "Внучок таких ролей еще нет", "Пожилой мне нехуй удалять, еще нет такого уровня", f"Бля сынок первый раз вижу этот уровень, юзай **.{commands_names['level']['add']}**"
            ]))
        cursor.execute("DELETE FROM levels WHERE level_id = ?", (role_id,))
        check_name = cursor.execute("SELECT id FROM user WHERE user_id = ?", (user_id,)).fetchone()
        if not check_name:
            cursor.execute("INSERT INTO user(user_id) VALUES(?)", (user_id,))
            check_name = cursor.execute("SELECT id FROM user WHERE user_id = ?", (user_id,)).fetchone()
        db_server_id, db_user_id = server[0], check_name[0]
        if not cursor.execute("SELECT id FROM connect WHERE server_id = ? and user_id = ?", (db_server_id, db_user_id)).fetchall():
            cursor.execute("INSERT INTO connect(server_id,user_id) VALUES(?,?)", (db_server_id, db_user_id))
        conn.commit()
        conn.close()
        await ctx.send(choice([
            f"Успешно удалил уровень {role.mention}", f"Внучок удалил роль {role.mention}", f"Удалил уровень {role.mention}"
        ]))

    @level_delete.error
    async def level_delete_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(choice([
                "Внучок, у тебя нет прав на редактирование уровней", "Братик ты не можешь менять уровни", "Молодой, тебе нельзя менять уровни"
            ]))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(choice([
                "Старичок мне нужна только роль", "пожилой сюда надо роль пихать"
            ]))
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(choice([
                "Внучок блять, мне нужна роль а не юзер", "Сынок ты сюда роли пихай, а не пользователей", "Внучок блять это место для ролей, а не для людей"
            ]))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(choice([
                "Бля ты какую то хуйню мне скормил, я сломался", "Не пихай сюда нихуя кроме ролей и уровня", "Внучок ебать не то в меня пихаешь, смотри **.help**"
            ]))

    @commands.command(name=commands_names["level"]["show levels"])
    async def level_show(self, ctx):
        guild_id = ctx.guild.id
        guild = ctx.guild
        conn = sqlite3.connect(os.path.abspath("database/samurai.db"))
        cursor = conn.cursor()
        levels = cursor.execute("SELECT level_id, level_xp FROM levels WHERE id = (SELECT id FROM server WHERE server_id = ?) ORDER BY level_xp DESC", (guild_id,)).fetchall()
        data = ""
        for line in levels:
            role = discord.utils.get(guild.roles, id=line[0])
            xp = line[1]
            data += f"\n**{role.mention}** - необходимо для получения: {xp} xp"
        embed = discord.Embed(
            title="Уровни на сервере",
            description="Информация об уровнях сервера и количества опыта для их получения" + data +
            "\n**1 xp = 1 сообщение**",
            colour=discord.Colour.purple()
        )
        await ctx.send(embed=embed)

    @commands.command(name=commands_names["level"]["show level"])
    async def level(self, ctx):
        user_id = ctx.message.author.id
        user = ctx.message.author
        guild_id = ctx.guild.id
        guild = ctx.guild
        conn = sqlite3.connect(os.path.abspath("database/samurai.db"))
        cursor = conn.cursor()

        # -----------------------------------Check-info----------------------------------------------
        db_user_id = cursor.execute("SELECT id FROM user WHERE user_id = ?", (user_id,)).fetchone()
        if not db_user_id:
            cursor.execute("INSERT INTO user(user_id) VALUES(?)", (user_id,))
            return await ctx.send(choice([
                "Сынок я тебя первый раз вижу, какой лвл", "Внучок о тебе информации в базе данных нет", "Сынок я тебя не знаю, а лвл уж точно"
            ]))
        if isinstance(db_user_id, tuple):
            db_user_id = db_user_id[0]
        db_server_id = cursor.execute("SELECT id FROM server WHERE server_id = ?", (guild_id,)).fetchone()
        if not db_server_id:
            cursor.execute("INSERT INTO server(server_id) VALUES(?)", (guild_id,))
            return await ctx.send(choice([
                "Пожилой я на этом сервере еще не освоился, поэтому о ролях ничего не знаю", "В моей базе данных отсутствует инфа о лвлах этого сервера", "Внучок в душе не ебу какие здесь лвла"
            ]))
        if isinstance(db_server_id, tuple):
            db_server_id = db_server_id[0]
        info = cursor.execute("SELECT level, xp FROM user_levels WHERE id = ?", (db_user_id,)).fetchone()
        if not info:
            return await ctx.send(choice([
                "Сынок у меня по твоим уровням нет инфы, прояви активность на сервере", "Внучок пока по твоему лвлу нет инфы", "Сынок в душе не ебу какой у тебя лвл"
            ]))
        # -------------------------------------------------------------------------------------------

        level, xp = info
        embed = discord.Embed(
            title=f"{user.name} - DASHBOARD",
            description=f"""{choice(["Пуси цунами от этой зайки!!!", "Он пиздатый, ахуенный, самый первый, не въебенный!", "Супер экстра пупсик!"])} {user.mention}
**level - {discord.utils.get(guild.roles, id=level).mention}**
**xp - {xp}**""",
            colour=discord.Colour.purple()
        )
        embed.set_thumbnail(url=user.avatar_url)
        if not cursor.execute("SELECT id FROM connect WHERE server_id = ? and user_id = ?", (db_server_id, db_user_id)).fetchall():
            cursor.execute("INSERT INTO connect(server_id,user_id) VALUES(?,?)", (db_server_id, db_user_id))
        conn.commit()
        conn.close()
        await ctx.send(embed=embed)

    @commands.command(name=commands_names["level"]["dashboard"])
    async def level_dashboard(self, ctx):
        user_id = ctx.message.author.id
        user = ctx.message.author
        guild_id = ctx.guild.id
        guild = ctx.guild
        conn = sqlite3.connect(os.path.abspath("database/samurai.db"))
        cursor = conn.cursor()

        # -----------------------------------Check-info----------------------------------------------
        check_user = cursor.execute("SELECT id FROM user WHERE user_id = ?", (user_id,)).fetchone()
        if not check_user:
            cursor.execute("INSERT INTO user(user_id) VALUES(?)", (user_id,))
        check_server = cursor.execute("SELECT id FROM server WHERE server_id = ?", (guild_id,)).fetchone()
        if not check_server:
            cursor.execute("INSERT INTO server(server_id) VALUES(?)", (guild_id,))
            return await ctx.send(choice([
                "Сынок у меня пока вообще нет инфы об этом сервере", "Внучок я пока об этом сервере ничего не знаю", "Пожилой, пока ноль инфы об этом сервере"
            ]))
        check_users = cursor.execute("SELECT user_id FROM connect WHERE server_id = (SELECT id FROM server WHERE server_id = ?)", (guild_id,)).fetchall()
        if not check_users:
            return await ctx.send(choice([
                "Я пока не получил ни одного сообщения на сервере", "Пока ноль инфы об уровнях участников", "Еще не получил ни одного сообщения", "0 инфы о вас ребятки"
            ]))
        # -------------------------------------------------------------------------------------------

        check_users = [i[0] for i in check_users]
        users = cursor.execute(f"SELECT user_id FROM user WHERE id IN ({','.join(['?'] * len(check_users))})", check_users).fetchall()
        levels = cursor.execute(f"SELECT level, xp FROM user_levels WHERE id IN ({','.join(['?'] * len(check_users))})", check_users).fetchall()
        info = []
        for i in range(len(check_users)):
            info.append(users[i] + levels[i])
        info.sort(key=lambda x: x[2], reverse=True)
        embed = discord.Embed(
            title=f"{guild.name} DASHBOARD",
            colour=discord.Colour.purple()
        )
        embed.set_thumbnail(url=guild.icon_url)
        phrases_three_winners = {
            1: choice(['Мега распиздатый на первом месте!', 'Первый на первом!', 'Секси юзер на первом месте!']),
            2: choice(['Сладкий пупсик на втором!', 'Второй, потому что дал фору!', 'Мега негр на втором!']),
            3: choice(['Мега зайка на третьем!', 'Сладкий малипуська на третьем!', 'Третий, потому что 1 и 2 слишком мало!'])
        }
        for i in range(min(3, len(info))):
            cur_user = discord.utils.get(guild.members, id=info[i][0])
            cur_level = discord.utils.get(guild.roles, id=info[i][1])
            cur_xp = info[i][2]
            embed.add_field(
                name=f"{i + 1}. {cur_user.name}",
                value=f"{phrases_three_winners[i + 1]} {cur_user.mention}\n**level: {cur_level if not cur_level else cur_level.mention}\nxp: {cur_xp}**",
                inline=False
            )
        info = info[:max(-3, -len(info))]
        output = []
        for num, line in enumerate(info):
            cur_user = discord.utils.get(guild.members, id=line[0])
            cur_level = discord.utils.get(guild.roles, id=line[1])
            cur_xp = line[2]
            output.append(f"**{num + 4}.{cur_user.mention}** - {' '.join([cur_level if not cur_level else cur_level.mention, f'**{cur_xp} xp**'])}")
        if output:
            embed.add_field(
                name=choice([
                    "Не менее крутые пупсики", "Не менее сладкие зайки", "Сопоставимые по пиздатости", "А также не менее мощные мужчины"
                ]),
                value="\n".join(output),
                inline=False
            )

        db_server_id = check_server[0] if isinstance(check_server, tuple) else check_server
        db_user_id = check_user[0] if isinstance(check_user, tuple) else check_user
        if not cursor.execute("SELECT id FROM connect WHERE server_id = ? and user_id = ?", (db_server_id, db_user_id)).fetchall():
            cursor.execute("INSERT INTO connect(server_id,user_id) VALUES(?,?)", (db_server_id, db_user_id))
        conn.commit()
        conn.close()
        await ctx.send(embed=embed)
