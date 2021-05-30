import discord
from discord.utils import get
from discord.ext import commands
from cogs.commands import commands_names
from cogs.config import *
from cogs.database_connector import Database
from random import choice


class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.Cog.listener("on_message")
    async def check_level_up(self, message):
        if message.author.bot:
            return
        user = message.author
        user_id = user.id
        server = message.guild
        server_id = server.id
        with Database() as db:
            db_server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id]).fetchone()[0]
            db_user_id = db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id]).fetchone()[0]
            levels = db.execute('SELECT level_id, level_xp FROM "default".servers_levels WHERE server_id = %s ORDER BY level_xp DESC ', [db_server_id]).fetchall()
            if not levels:
                return
            user_xp = db.execute('SELECT xp FROM "default".users_levels WHERE user_id = %s and server_id = %s', [db_user_id, db_server_id]).fetchone()[0]
            user_xp += 1
            db.execute('UPDATE "default".users_levels SET xp = %s WHERE user_id = %s and server_id = %s', [user_xp, db_user_id, db_server_id])
            for db_level, db_xp in levels:
                if user_xp == db_xp:
                    db.execute('UPDATE "default".users_levels SET level = %s WHERE user_id = %s and server_id = %s', [db_level, db_user_id, db_server_id])
                    mention = user.mention
                    role = get(server.roles, id=db_level)
                    await user.remove_roles(*[_role for _role in user.roles if _role in [_db_role for _db_role, _xp in levels]])
                    await user.add_roles(role)
                    embed = discord.Embed(
                        title=":chart_with_upwards_trend: LEVEL UP :chart_with_upwards_trend:",
                        description=choice([
                            f"Сладкий {mention} заслужил повышение!!!", f"Лапочка {mention} стала еще более уважаемой", f"Поздравляю с повышением, {mention}"
                        ]) + f"\n**level - {role.mention}\nxp - {user_xp}**",
                        colour=discord.Colour.purple()
                    )
                    embed.set_thumbnail(url=user.avatar_url)
                    info_chat = db.execute('SELECT info_chat FROM "default".servers_chats WHERE server_id = %s', [db_server_id]).fetchone()[0]
                    if info_chat:
                        return await self.bot.get_channel(info_chat).send(embed=embed)
                    return await message.channel.send(embed=embed)

    @commands.command(name=commands_names["level"]["add"])
    @commands.has_permissions(manage_roles=True)
    async def level_add(self, ctx, role: discord.Role, level_xp: int):
        level_id = role.id
        server_id = role.guild.id
        with Database() as db:
            db_server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id]).fetchone()[0]
            db_level_id = db.execute('SELECT level_id FROM "default".servers_levels WHERE server_id = %s and level_id = %s', [db_server_id, level_id]).fetchone()
            db_level_id = db_level_id[0] if isinstance(db_level_id, tuple) else db_level_id
            if db_level_id:
                return await ctx.send(choice([
                    "Сладкий, такой уровень уже есть.", "Лапочка, в базе уже есть такой уровень.", "Малыш, у меня уже есть такой уровень."
                ]) + f" Используй **.{commands_names['level']['up']}** чтобы обновить уровень или **.{commands_names['level']['delete']}** чтобы удалить роль")
            db.execute('INSERT INTO "default".servers_levels(server_id, level_id, level_xp) VALUES (%s, %s, %s)', [db_server_id, level_id, level_xp])
            await ctx.send(choice([
                f"Успешно добавил уровень {role.mention} в базу данных", f"Сладенький, добавил уровень {role.mention} в базу данных", f"Записал уровень {role.mention} в базу данных"
            ]))

    @commands.has_permissions(manage_roles=True)
    @commands.command(name=commands_names["level"]["up"])
    async def level_update(self, ctx, role: discord.Role, level_xp: int):
        level_id = role.id
        server_id = role.guild.id
        with Database() as db:
            db_server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id]).fetchone()[0]
            db_level_id = db.execute('SELECT level_id FROM "default".servers_levels WHERE server_id = %s and level_id = %s', [db_server_id, level_id]).fetchone()
            db_level_id = db_level_id[0] if isinstance(db_level_id, tuple) else db_level_id
            if not db_level_id:
                return await ctx.send(choice([
                    "Малыш, чтобы обновлять роль, ее сначала нужно создать.", "Сладенький, мне нечего обновлять.", "Пупсик, я не знаю такой уровень."
                ]) + f" Используй **.{commands_names['level']['add']}**, чтобы создать роль")
            db_level_xp = db.execute('SELECT level_xp FROM "default".servers_levels WHERE server_id = %s and level_id = %s', [db_server_id, level_id]).fetchone()[0]
            if db_level_xp == level_xp:
                return await ctx.send(choice([
                    f"Муська, у этого уровня {role.mention} и так такое же количество опыта", f"В базе данных те же значения"
                ]))
            db.execute('UPDATE "default".servers_levels SET level_xp = %s WHERE server_id = %s and level_id = %s', [level_xp, db_server_id, level_id])
            await ctx.send(choice([
                "Сладенький, успешно обновил уровень.", "Проапдейтил уровень, зайка.", "Обновил данные."
            ]) + f" Теперь для получения {role.mention} необходимо **{level_xp}**")

    @level_update.error
    @level_add.error
    async def level_add_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(choice([
                "Внучок, у тебя нет прав на редактирование уровней", "Братик ты не можешь менять уровни", "Молодой, тебе нельзя менять уровни"
            ]))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(choice([
                "Старичок мне нужна роль и количество опыта, чтобы ее получить", "Малыш сюда надо роль и количество опыта"
            ]))
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(choice([
                "Сладенький, для уровня нужна роль, а не человек.", "Пупсик, мне нужна роль, а не юзер"
            ]))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(choice([
                "Неверные типы данных", "Зайка, тебе нужно ввести только роль и количество опыта", "Неверные аргументы"
            ]))

    @commands.has_permissions(manage_roles=True)
    @commands.command(name=commands_names["level"]["delete"])
    async def level_delete(self, ctx, role: discord.Role):
        level_id = role.id
        server_id = role.guild.id
        with Database() as db:
            db_server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id]).fetchone()[0]
            db_level_id = db.execute('SELECT level_id FROM "default".servers_levels WHERE server_id = %s and level_id = %s', [db_server_id, level_id]).fetchone()
            db_level_id = db_level_id[0] if isinstance(db_level_id, tuple) else db_level_id
            if not db_level_id:
                return await ctx.send(choice([
                    "Малыш, чтобы удалять роль, ее сначала нужно создать.", "Сладенький, мне нечего удалять.", "Пупсик, я не знаю такой уровень."
                ]) + f" Используй **.{commands_names['level']['add']}**, чтобы создать роль")
            db.execute('DELETE FROM "default".servers_levels WHERE server_id = %s and level_id = %s', [db_server_id, level_id])
            await ctx.send(choice([
                "Успешно удалил уровень", f"Удалил {role.mention} из базы ролей"
            ]))

    @level_delete.error
    async def level_delete_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(choice([
                "Внучок, у тебя нет прав на редактирование уровней", "Братик ты не можешь менять уровни", "Молодой, тебе нельзя менять уровни"
            ]))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(choice([
                "Старичок мне нужна роль", "Малыш сюда надо роль пихать"
            ]))
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(choice([
                "Сладенький, для уровня нужна роль, а не человек.", "Пупсик, мне нужна роль, а не юзер"
            ]))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(choice([
                "Неверные типы данных", "Зайка, тебе нужно ввести только роль", "Неверные аргументы"
            ]))

    @commands.command(name=commands_names["level"]["show levels"])
    async def level_show(self, ctx):
        server = ctx.guild
        server_id = server.id
        with Database() as db:
            db_server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id]).fetchone()[0]
            levels = db.execute('SELECT level_id, level_xp FROM "default".servers_levels WHERE server_id = %s ORDER BY level_xp DESC', [db_server_id]).fetchall()
            if not levels:
                data = choice(["Информации пока нет :pensive:", "Информации отсутсвует :pensive:"])
            else:
                data = ""
                for level, xp in levels:
                    role = get(server.roles, id=level)
                    data += f"\n**{role.mention}** - **{xp} xp**"
            embed = discord.Embed(
                title=choice(["LEVELS!!!", f"Уровни {get(self.bot.emojis, name='peepohappy')}"]) + " - " + server.name,
                description=data,
                colour=discord.Colour.purple()
            )
            embed.set_thumbnail(url=server.icon_url)
            embed.set_footer(text="1 xp = 1 сообщение")
            await ctx.send(embed=embed)

    @commands.command(name=commands_names["level"]["show level"])
    async def level(self, ctx):
        server = ctx.guild
        server_id = server.id
        user = ctx.message.author
        user_id = user.id
        with Database() as db:
            db_user_id = db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id]).fetchone()[0]
            db_server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id]).fetchone()[0]
            db_server_levels = db.execute('SELECT level_id FROM "default".servers_levels WHERE server_id = %s', [db_server_id]).fetchall()
            if not db_server_levels:
                return await ctx.send(choice([
                    f"Малыш, на сервере {server.name} к сожалению пока нет системы уровней", "Зайка, на этом сервере нет системы уровней", "Система уровней отсутствует"
                ]))
            db_user_level, db_user_xp = db.execute('SELECT level, xp FROM "default".users_levels WHERE server_id = %s and user_id = %s', [db_server_id, db_user_id]).fetchone()
            print(db_user_level, get(server.roles, id=db_user_level), server.roles)
            db_user_level = 'отсутствует' if not get(server.roles, id=db_user_level) else get(server.roles, id=db_user_level).mention
            embed = discord.Embed(
                title=user.name + " - LEVEL",
                description=f"""{choice(["Пуси цунами от этой зайки!!!", "Супер экстра пупсик!"])} {user.mention}
                **level - {db_user_level}**
                **xp - {db_user_xp}**""",
                colour=discord.Colour.purple()
            )
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(name=commands_names["level"]["dashboard"])
    async def level_dashboard(self, ctx, limit=10):
        server = ctx.guild
        server_id = server.id
        with Database() as db:
            db_server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id]).fetchone()[0]
            db_server_levels = db.execute('SELECT level_id FROM "default".servers_levels WHERE server_id = %s', [db_server_id]).fetchall()
            if not db_server_levels:
                return await ctx.send(choice([
                    f"Малыш, на сервере {server.name} к сожалению пока нет системы уровней", "Зайка, на этом сервере нет системы уровней", "Система уровней отсутствует"
                ]))
            embed = discord.Embed(
                title=server.name + " - DASHBOARD",
                colour=discord.Colour.purple()
            )
            embed.set_thumbnail(url=server.icon_url)
            top_three_phrases = {
                1: choice(['Мега классный на первом месте!', 'Первый на первом!', 'Секси юзер на первом месте!']),
                2: choice(['Сладкий пупсик на втором!', 'Второй, потому что дал фору!', 'Мега солнышко на втором!']),
                3: choice(['Мега зайка на третьем!', 'Сладкий малипуська на третьем!', 'Третий, потому что 1 и 2 слишком мало!'])
            }
            db.execute('SELECT user_id, level, xp FROM "default".users_levels WHERE server_id = %s ORDER BY xp DESC LIMIT %s', [db_server_id, limit])
            data = []
            for db_user_id, db_user_level, db_user_xp in db.fetchall():
                user_id = db.execute('SELECT discord_user_id FROM "default".users WHERE id = %s', [db_user_id]).fetchone()[0]
                user = get(server.members, id=user_id)
                level = 'отсутствует' if not get(server.roles, id=db_user_level) else get(server.roles, id=db_user_level).mention
                data.append([user, level, db_user_xp])
            for i in range(min(3, len(data))):
                user, level, xp = data[i]
                embed.add_field(
                    name=f"{i + 1}. {user.name}",
                    value=f"{top_three_phrases[i + 1]} {user.mention}\n**level: {level}\nxp: {xp}**",
                    inline=False
                )
            data = data[min(3, len(data)):]
            output = []
            for pos, line in enumerate(data):
                user, level, xp = line
                output.append(f"**{pos + 4}.{user.mention}** - {' '.join([level, f'**{xp} xp**'])}")
            if output:
                embed.add_field(name=choice([
                    "Не менее крутые пупсики", "Не менее сладкие зайки", "Сопоставимые по крутости", "А также не менее мощные мужчины"
                ]),
                    value="\n".join(output),
                    inline=False
                )
            await ctx.send(embed=embed)
