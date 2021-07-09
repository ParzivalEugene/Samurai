import datetime
from random import choice
import discord
from discord.ext import commands, tasks
from discord.utils import get
from main.cogs.config import colour
from main.cogs.commands import commands_names as cs
from main.cogs.database_connector import Database
from main.cogs.glossary import speech_setting

commands_names = cs.birthdays


class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=commands_names.help)
    async def birthday_help(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).birthdays
        embed = discord.Embed(
            title=vocabulary.help.title,
            description=vocabulary.help.description,
            colour=colour
        )
        embed.add_field(
            name=vocabulary.help.name,
            value=vocabulary.help.value,
            inline=False
        )
        await ctx.send(embed=embed)

    @tasks.loop(hours=12)
    async def check_birthdays(self):
        with Database() as db:
            data = db.execute('''
                SELECT discord_user_id,
                date_part('year', CURRENT_DATE) - date_part('year', birthdays.date),
                discord_server_id,
                birthdays_chat
                FROM "default".users, "default".birthdays, "default".servers, "default".servers_chats
                WHERE users.id = birthdays.user_id
                AND servers.id = servers_chats.server_id
                AND (users.id, servers.id) IN (
                    SELECT user_id, server_id
                    FROM "default".connect
                    )
                AND birthdays_chat != 0
                AND date_part('month', CURRENT_DATE) = date_part('month', date)
                AND date_part('day', CURRENT_DATE) = date_part('day', date)''').fetchall()
            for user_id, age, server_id, chat_id in data:
                user = self.bot.get_user(user_id)
                server = self.bot.get_guild(server_id)
                chat = self.bot.get_channel(chat_id)
                vocabulary = speech_setting(server.id).birthdays
                embed = discord.Embed(
                    title=vocabulary.check_birthdays.title.format(user.name),
                    description=vocabulary.check_birthdays.description.format(user.mention, ':heart:', self.bot.user.mention),
                    colour=colour
                )
                embed.set_thumbnail(url=user.avatar_url)
                await chat.send(embed=embed)

    @commands.command(name=commands_names.add)
    async def add_birthday(self, ctx, year: int, month: int, day: int):
        vocabulary = speech_setting(ctx.guild.id).birthdays
        if not (0 < year < datetime.date.today().year and 0 < month < 13 and 0 < day < 32):
            return await ctx.send(choice(vocabulary.add_birthday.incorrect_date))
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
                return await ctx.send(choice(vocabulary.add_birthday.date_already_exosts).format(db_date))
            db.execute('INSERT INTO "default".birthdays(user_id, date) VALUES (%s, %s)', [db_user_id, user_date.isoformat()])

            await ctx.send(choice(vocabulary.add_birthday.success).format(month, day))

    @add_birthday.error
    async def add_birthday_error(self, ctx, error):
        vocabulary = speech_setting(ctx.guild.id).birthdays
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(choice(vocabulary.add_birthday_error.MissingRequiredArgument))
        if isinstance(error, commands.BadArgument):
            await ctx.send(choice(vocabulary.add_birthday_error.BadArgument))

    @commands.command(name=commands_names.up)
    async def update_birthdays(self, ctx, year: int, month: int, day: int):
        vocabulary = speech_setting(ctx.guild.id).birthdays
        if not (0 < year < datetime.date.today().year and 0 < month < 13 and 0 < day < 32):
            return await ctx.send(choice(vocabulary.update_birthday.incorrect_date))
        user_id = ctx.message.author.id
        user_date = datetime.date(year, month, day)
        month, day = user_date.month, user_date.day
        with Database() as db:
            db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id])
            db_user_id = db.fetchone()[0]
            db.execute('SELECT date FROM "default".birthdays WHERE user_id = %s', [db_user_id])
            db_date = db.fetchone()
            if db_date is None:
                return await ctx.send(choice(vocabulary.update_birthday.date_does_not_exist_yet).format(month, day))
            if db_date[0] == user_date:
                return await ctx.send(choice(vocabulary.update_birthday.the_same_date))
            db.execute('UPDATE "default".birthdays SET date = %s WHERE user_id = %s', [user_date, db_user_id])
            await ctx.send(choice(vocabulary.update_birthday.success))

    @update_birthdays.error
    async def update_birthday_error(self, ctx, error):
        vocabulary = speech_setting(ctx.guild.id).birthdays
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(choice(vocabulary.update_birthday_error.MissingRequiredArgument))
        if isinstance(error, commands.BadArgument):
            await ctx.send(choice(vocabulary.update_birthday_error.BadArgument))

    @commands.command(name=commands_names.delete)
    async def delete_birthdays(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).birthdays
        user_id = ctx.message.author.id
        with Database() as db:
            db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id])
            db_user_id = db.fetchone()[0]
            db.execute('SELECT date FROM "default".birthdays WHERE user_id = %s', [db_user_id])
            db_date = db.fetchone()
            if db_date is None:
                return await ctx.send(choice(vocabulary.delete_birthday.date_does_not_exist_yet))
            db.execute('DELETE FROM "default".birthdays WHERE user_id = %s', [db_user_id])
            await ctx.send(choice(vocabulary.delete_birthday.success))

    @commands.command(name=commands_names.show_bd)
    async def show_birthday(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).birthdays
        user_id = ctx.message.author.id
        user = ctx.message.author
        with Database() as db:
            db_date = db.execute('''SELECT date FROM "default".birthdays
                                    WHERE user_id = (
                                        SELECT id FROM "default".users
                                        WHERE discord_user_id = %s)''', [user_id]).fetchone()
            if db_date is None:
                return await ctx.send(choice(vocabulary.show_birthday.date_does_not_exist_yet))
            db_date = str(db_date[0]).replace("-", ".")
            embed = discord.Embed(
                title=vocabulary.show_birthday.title.format(user.name),
                description=choice(vocabulary.show_birthday.description_start).format(user.mention) + vocabulary.show_birthday.description_end.format(db_date),
                colour=colour
            )
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(name=commands_names.show_bds)
    async def show_birthdays(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).birthdays
        server = ctx.guild
        with Database() as db:
            output_embed = db.execute('''SELECT discord_user_id, date 
                                         FROM "default".users, "default".birthdays 
                                         WHERE birthdays.user_id = users.id 
                                         AND users.id IN (
                                            SELECT user_id FROM "default".connect 
                                            WHERE server_id = (
                                                SELECT id FROM "default".servers 
                                                WHERE discord_server_id = %s 
                                            )
                                         ) ORDER BY date''', [server.id]).fetchall()
        if not output_embed:
            return await ctx.send(choice(vocabulary.show_birthdays.no_info))
        embed = discord.Embed(
            title=vocabulary.show_birthdays.title.format(server.name),
            description="\n".join([f"{pos + 1}. {get(server.members, id=value[0]).mention} - **{str(value[1]).replace('-', '.')}**" for pos, value in enumerate(output_embed)]),
            colour=colour
        )
        embed.set_thumbnail(url=server.icon_url)
        await ctx.send(embed=embed)

    @commands.has_permissions(manage_channels=True)
    @commands.command(name=commands_names.set_chat)
    async def set_chat_birthday(self, ctx, chat: discord.TextChannel):
        vocabulary = speech_setting(ctx.guild.id).birthdays
        server_id = ctx.guild.id
        with Database() as db:
            db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id])
            db_server_id = db.fetchone()[0]
            db.execute('SELECT birthdays_chat FROM "default".servers_chats WHERE server_id = %s', [db_server_id])
            birthdays_chat_id = db.fetchone()[0]
            if birthdays_chat_id:
                up, delete = commands_names.up_chat, commands_names.del_chat
                birthdays_chat = self.bot.get_channel(birthdays_chat_id).mention
                return await ctx.send(choice(vocabulary.set_chat_birthday.chat_already_exist).format(birthdays_chat, up, delete))
            db.execute('UPDATE "default".servers_chats SET birthdays_chat = %s WHERE server_id = %s', [chat.id, db_server_id])
            return await ctx.send(choice(vocabulary.set_chat_birthday.success).format(chat.mention))

    @set_chat_birthday.error
    async def set_chat_birthday_error(self, ctx, error):
        vocabulary = speech_setting(ctx.guild.id).birthdays
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(choice(vocabulary.set_chat_birthday_error.MissingRequiredArgument))
        if isinstance(error, commands.BadArgument):
            await ctx.send(choice(vocabulary.set_chat_birthday_error.BadArgument))

    @commands.has_permissions(manage_channels=True)
    @commands.command(name=commands_names.up_chat)
    async def update_chat_birthday(self, ctx, chat: discord.TextChannel):
        vocabulary = speech_setting(ctx.guild.id).birthdays
        server_id = ctx.guild.id
        with Database() as db:
            db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id])
            db_server_id = db.fetchone()[0]
            db.execute('SELECT birthdays_chat FROM "default".servers_chats WHERE server_id = %s', [db_server_id])
            birthdays_chat_id = db.fetchone()[0]
            if not birthdays_chat_id:
                return await ctx.send(choice(vocabulary.update_chat_birthday.chat_does_not_exist))
            if birthdays_chat_id[0] == chat.id:
                return await ctx.send(choice(vocabulary.update_chat_birthday.the_same_data))
            db.execute('UPDATE "default".servers_chats SET birthdays_chat = %s WHERE server_id = %s', [chat.id, db_server_id])
        await ctx.send(choice(vocabulary.update_chat_birthday.success).format(chat.mention))

    @update_chat_birthday.error
    async def update_chat_birthday_error(self, ctx, error):
        vocabulary = speech_setting(ctx.guild.id).birthdays
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(choice(vocabulary.update_chat_birthday_error.MissingRequiredArgument))
        if isinstance(error, commands.BadArgument):
            await ctx.send(choice(vocabulary.update_chat_birthday_error.BadArgument))

    @commands.has_permissions(manage_channels=True)
    @commands.command(name=commands_names.del_chat)
    async def delete_chat_birthday(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).birthdays
        server_id = ctx.guild.id
        with Database() as db:
            db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id])
            db_server_id = db.fetchone()[0]
            db.execute('SELECT birthdays_chat FROM "default".servers_chats WHERE server_id = %s', [db_server_id])
            birthdays_chat_id = db.fetchone()[0]
            if not birthdays_chat_id:
                return await ctx.send(choice(vocabulary.delete_chat_birthday))
            db.execute('UPDATE "default".servers_chats SET birthdays_chat = null WHERE server_id = %s', [db_server_id])
        await ctx.send(choice(vocabulary.delete_chat_birthday.success))

    @commands.command(name=commands_names.show_chat)
    async def show_chat_birthdays(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).birthdays
        server_id = ctx.guild.id
        with Database() as db:
            birthdays_chat_id = db.execute('''SELECT birthdays_chat FROM "default".servers_chats
                                             WHERE server_id = (
                                                 SELECT id FROM "default".servers
                                                 WHERE discord_server_id = %s)''', [server_id]).fetchone()[0]
            if not birthdays_chat_id:
                return await ctx.send(choice(vocabulary.show_chat_birthdays.no_info))
            birthdays_chat = self.bot.get_channel(birthdays_chat_id).mention
        await ctx.send(choice(vocabulary.show_chat_birthdays.success).format(birthdays_chat))
