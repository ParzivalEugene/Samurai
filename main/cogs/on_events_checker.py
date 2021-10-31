from random import choice
import discord
from discord.ext import commands
from discord.utils import get
from cogs.database_connector import Database
from cogs.config import colour


class OnEventsChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(choice([
                "Внучок, я таких команд не знаю", "Боевой, это чо за команда", "*\Бип\* - *\Боп\* неизвестная мне команда"
            ]))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(choice([
                "Малыш, у меня нет прав на выполнение этого действия.", "Сладкий, я не могу это сделать, потому что у меня нет прав."
            ])) + " Попробуй добавить мне роль с правами администратора"
        elif error:
            raise error

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before == self.bot.user:
            return
        if before.roles != after.roles:
            with Database() as db:
                db_user_id = db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [after.id]).fetchone()[0]
                db_server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [after.guild.id]).fetchone()[0]
                db_levels = db.execute('SELECT level_id, level_xp FROM "default".servers_levels WHERE server_id = %s', [db_server_id]).fetchall()
                if not db_levels:
                    return
                before_roles, after_roles = set(before.roles), set(after.roles)
                role = before_roles.symmetric_difference(after_roles).pop()
                if role.id not in [level for level, xp in db_levels]:
                    return
                user_level, user_xp = db.execute('SELECT level, xp FROM "default".users_levels WHERE server_id = %s and user_id = %s', [db_server_id, db_user_id]).fetchone()
                db_xp = db.execute('SELECT level_xp FROM "default".servers_levels WHERE server_id = %s and level_id = %s', [db_server_id, role.id]).fetchone()[0]
                info_chat = self.bot.get_channel(db.execute('SELECT info_chat FROM "default".servers_chats WHERE server_id = %s', [db_server_id]).fetchone()[0])
                if not info_chat:
                    return
                if db_xp > user_xp:
                    async for event in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
                        if event.user.bot:
                            return
                        if event.target.id != before.id:
                            continue
                        levels_to_remove = []
                        for _level, _xp in db_levels:
                            _level = get(after.guild.roles, id=_level)
                            if _level in after.roles and _level != role:
                                levels_to_remove.append(_level)
                        db.execute('UPDATE "default".users_levels SET level = %s, xp = %s WHERE server_id = %s and user_id = %s', [role.id, db_xp, db_server_id, db_user_id])
                        embed = discord.Embed(
                            title=":chart_with_upwards_trend: LEVEL UP :chart_with_upwards_trend:",
                            description=f"{after.mention} был повышен модератором {event.user.mention} до уровня {role.mention}. Мои поздравления!\n**level - {role.mention}\nxp - {db_xp}**",
                            colour=colour
                        )
                        embed.set_thumbnail(url=after.avatar_url)
                        await after.remove_roles(*levels_to_remove)
                        return await info_chat.send(embed=embed)
                elif db_xp <= user_xp:
                    async for event in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
                        if event.user.bot:
                            return
                        if event.target.id != before.id:
                            continue
                        db.execute('UPDATE "default".users_levels SET level = %s, xp = %s WHERE server_id = %s and user_id = %s', [0, 0, db_server_id, db_user_id])
                        embed = discord.Embed(
                            title=":chart_with_downwards_trend: LEVEL DOWN :chart_with_downwards_trend:",
                            description=f"{after.mention} был понижен модератором {event.user.mention}.\n**level - 0\nxp - 0**",
                            colour=colour
                        )
                        embed.set_thumbnail(url=after.avatar_url)
                        return await info_chat.send(embed=embed)

    async def leave_join_message(self, member, message):
        with Database() as db:
            server_id = member.guild.id
            db.execute('SELECT join_leave_chat FROM "default".servers_chats WHERE server_id = (SELECT id FROM "default".servers WHERE discord_server_id = %s)', [server_id])
            chat_id = db.fetchone()
            if chat_id:
                channel = self.bot.get_channel(chat_id[0])
                if channel:
                    await channel.send(member.mention, message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member == self.bot.user:
            return
        with Database() as db:
            user_id = member.id
            db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id])
            if db.fetchone() is None:
                db.execute('INSERT INTO "default".users(discord_user_id) VALUES(%s) RETURNING id', [user_id])
            db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id])
            db_user_id = db.fetchone()[0]
            server_id = member.guild.id
            db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id])
            db_server_id = db.fetchone()[0]
            db.execute('SELECT id FROM "default".connect WHERE server_id = %s and user_id = %s', [db_server_id, db_user_id])
            if db.fetchone() is None:
                db.execute('INSERT INTO "default".connect(server_id, user_id) VALUES(%s, %s)', [db_server_id, db_user_id])
            db.execute('SELECT level FROM "default".users_levels WHERE user_id = %s and server_id = %s', [db_user_id, db_server_id])
            if db.fetchone() is None:
                db.execute('INSERT INTO "default".users_levels(server_id, user_id, level, xp) VALUES (%s, %s, %s, %s)', [db_server_id, db_user_id, 0, 0])
        await self.leave_join_message(member, "присоединился к серверу")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member == self.bot.user:
            return
        with Database() as db:
            user_id = member.id
            db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id])
            db_user_id = db.fetchone()[0]
            server_id = member.guild.id
            db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id])
            db_server_id = db.fetchone()[0]
            db.execute('DELETE FROM "default".connect WHERE server_id = %s and user_id = %s', [db_server_id, db_user_id])
            db.execute('DELETE FROM "default".users_levels WHERE user_id = %s and server_id = %s', [db_user_id, db_server_id])
        await self.leave_join_message(member, "покинул сервер")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        members = guild.members
        members_ids = [member.id for member in members]
        server_id = guild.id
        with Database() as db:
            db.execute('INSERT INTO "default".servers(discord_server_id) VALUES(%s) RETURNING id', [server_id])
            db_server_id = db.fetchone()[0]
            db.execute('INSERT INTO "default".servers_languages_and_vibes(server_id) VALUES(%s)', [db_server_id])
            db.execute('INSERT INTO "default".connect_four_game(server_id) VALUES (%s)', [db_server_id])
            for user_id in members_ids:
                if user_id == self.bot.user.id:
                    continue
                db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id])
                if db.fetchone() is None:
                    db.execute('INSERT INTO "default".users(discord_user_id) VALUES(%s) RETURNING id', [user_id])
                db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id])
                db_user_id = db.fetchone()[0]
                db.execute('INSERT INTO "default".connect(server_id, user_id) VALUES(%s, %s)', [db_server_id, db_user_id])
                db.execute('INSERT INTO "default".users_levels(server_id, user_id, level, xp) VALUES (%s, %s, %s, %s)', [db_server_id, db_user_id, 0, 0])

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        members = guild.members
        members_ids = [member.id for member in members]
        server_id = guild.id
        with Database() as db:
            db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id])
            db_server_id = db.fetchone()[0]
            db.execute('DELETE FROM "default".servers_levels WHERE server_id = %s', [db_server_id])
            db.execute('DELETE FROM "default".servers_chats WHERE server_id = %s', [db_server_id])
            db.execute('DELETE FROM "default".servers_languages_and_vibes WHERE server_id = %s', [db_server_id])
            db.execute('DELETE FROM "default".connect_four_game WHERE server_id = %s', [db_server_id])
            for user_id in members_ids:
                db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id])
                db_user_id = db.fetchone()[0]
                db.execute('DELETE FROM "default".connect WHERE server_id = %s and user_id = %s', [db_server_id, db_user_id])
                db.execute('DELETE FROM "default".users_levels WHERE server_id = %s and user_id = %s', [db_server_id, db_user_id])
            db.execute('DELETE FROM "default".servers WHERE id = %s', [db_server_id])
