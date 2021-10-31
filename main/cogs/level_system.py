from random import choice
import discord
from discord.ext import commands
from discord.utils import get
from cogs.config import colour
from cogs.commands import commands_names as cs
from cogs.database_connector import Database
from cogs.glossary import speech_setting

commands_names = cs.level


class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=commands_names.help)
    async def level_help(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).level_system
        embed = discord.Embed(
            title=vocabulary.help.title,
            description=vocabulary.help.description,
            colour=colour
        )
        embed.add_field(name=vocabulary.help.name,
                        value=vocabulary.help.value,
                        inline=False)
        await ctx.send(embed=embed)

    @commands.Cog.listener("on_message")
    async def check_level_up(self, message):
        vocabulary = speech_setting(message.guild.id).level_system
        if message.author.bot:
            return
        user = message.author
        user_id = user.id
        server = message.guild
        server_id = server.id
        with Database() as db:
            db_server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id]).fetchone()[0]
            levels = db.execute('SELECT level_id, level_xp FROM "default".servers_levels WHERE server_id = %s ORDER BY level_xp DESC ', [db_server_id]).fetchall()
            if not levels:
                return
            db_user_id = db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id]).fetchone()[0]
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
                        title=vocabulary.check_level_up.title,
                        description=choice(vocabulary.check_level_up.description_start).format(mention) + vocabulary.check_level_up.description_end.format(role.mention, user_xp),
                        colour=colour
                    )
                    embed.set_thumbnail(url=user.avatar_url)
                    info_chat = db.execute('SELECT info_chat FROM "default".servers_chats WHERE server_id = %s', [db_server_id]).fetchone()[0]
                    if info_chat:
                        return await self.bot.get_channel(info_chat).send(embed=embed)
                    return await message.channel.send(embed=embed)

    @commands.command(name=commands_names.add)
    @commands.has_permissions(manage_roles=True)
    async def level_add(self, ctx, role: discord.Role, level_xp: int):
        vocabulary = speech_setting(ctx.guild.id).level_system
        level_id = role.id
        server_id = role.guild.id
        with Database() as db:
            db_server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id]).fetchone()[0]
            db_level_id = db.execute('SELECT level_id FROM "default".servers_levels WHERE server_id = %s and level_id = %s', [db_server_id, level_id]).fetchone()
            db_level_id = db_level_id[0] if isinstance(db_level_id, tuple) else db_level_id
            if db_level_id:
                return await ctx.send(choice(vocabulary.level_add.the_same_data_start) + vocabulary.level_add.the_same_data_end)
            db.execute('INSERT INTO "default".servers_levels(server_id, level_id, level_xp) VALUES (%s, %s, %s)', [db_server_id, level_id, level_xp])
            await ctx.send(choice(vocabulary.level_add.success).format(role.mention))

    @commands.has_permissions(manage_roles=True)
    @commands.command(name=commands_names.up)
    async def level_update(self, ctx, role: discord.Role, level_xp: int):
        vocabulary = speech_setting(ctx.guild.id).level_system
        level_id = role.id
        server_id = role.guild.id
        with Database() as db:
            db_server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id]).fetchone()[0]
            db_level_id = db.execute('SELECT level_id FROM "default".servers_levels WHERE server_id = %s and level_id = %s', [db_server_id, level_id]).fetchone()
            db_level_id = db_level_id[0] if isinstance(db_level_id, tuple) else db_level_id
            if not db_level_id:
                return await ctx.send(choice(vocabulary.level_update.level_does_not_exist_start) + vocabulary.level_update.level_does_not_exist_end)
            db_level_xp = db.execute('SELECT level_xp FROM "default".servers_levels WHERE server_id = %s and level_id = %s', [db_server_id, level_id]).fetchone()[0]
            if db_level_xp == level_xp:
                return await ctx.send(choice(vocabulary.level_update.the_same_data))
            db.execute('UPDATE "default".servers_levels SET level_xp = %s WHERE server_id = %s and level_id = %s', [level_xp, db_server_id, level_id])
            await ctx.send(choice(vocabulary.level_update.success_start) + vocabulary.level_update.success_end.format(role.mention, level_xp))

    @level_update.error
    @level_add.error
    async def level_add_or_update_error(self, ctx, error):
        vocabulary = speech_setting(ctx.guild.id).level_system
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(choice(vocabulary.level_add_or_update_error.MissingPermissions))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(choice(vocabulary.level_add_or_update_error.MissingRequiredArgument))
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(choice(vocabulary.level_add_or_update_error.RoleNotFound))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(choice(vocabulary.level_add_or_update_error.BadArgument))

    @commands.has_permissions(manage_roles=True)
    @commands.command(name=commands_names.delete)
    async def level_delete(self, ctx, role: discord.Role):
        vocabulary = speech_setting(ctx.guild.id).level_system
        level_id = role.id
        server_id = role.guild.id
        with Database() as db:
            db_server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id]).fetchone()[0]
            db_level_id = db.execute('SELECT level_id FROM "default".servers_levels WHERE server_id = %s and level_id = %s', [db_server_id, level_id]).fetchone()
            db_level_id = db_level_id[0] if isinstance(db_level_id, tuple) else db_level_id
            if not db_level_id:
                return await ctx.send(choice(vocabulary.level_delete.level_does_not_exist_start) + vocabulary.level_delete.level_does_not_exist_end)
            db.execute('DELETE FROM "default".servers_levels WHERE server_id = %s and level_id = %s', [db_server_id, level_id])
            await ctx.send(choice(vocabulary.level_delete.success))

    @level_delete.error
    async def level_delete_error(self, ctx, error):
        vocabulary = speech_setting(ctx.guild.id).level_system
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(choice(vocabulary.level_delete_error.MissingPermissions))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(choice(vocabulary.level_delete_error.MissingRequiredArgument))
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(choice(vocabulary.level_delete_error.RoleNotFound))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(choice(vocabulary.level_delete_error.BadArgument))

    @commands.command(name=commands_names.show_levels)
    async def level_show(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).level_system
        server = ctx.guild
        server_id = server.id
        with Database() as db:
            db_server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id]).fetchone()[0]
            levels = db.execute('SELECT level_id, level_xp FROM "default".servers_levels WHERE server_id = %s ORDER BY level_xp DESC', [db_server_id]).fetchall()
            if not levels:
                data = choice(vocabulary.level_show.no_info)
            else:
                data = ""
                for level, xp in levels:
                    role = get(server.roles, id=level)
                    data += f"\n**{role.mention}** - **{xp} xp**"
            embed = discord.Embed(
                title=choice(vocabulary.level_show.title),
                description=data,
                colour=colour
            )
            embed.set_thumbnail(url=server.icon_url)
            embed.set_footer(text=vocabulary.level_show.footer)
            await ctx.send(embed=embed)

    @commands.command(name=commands_names.show_level)
    async def level(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).level_system
        server = ctx.guild
        server_id = server.id
        user = ctx.message.author
        user_id = user.id
        with Database() as db:
            db_user_id = db.execute('SELECT id FROM "default".users WHERE discord_user_id = %s', [user_id]).fetchone()[0]
            db_server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id]).fetchone()[0]
            db_server_levels = db.execute('SELECT level_id FROM "default".servers_levels WHERE server_id = %s', [db_server_id]).fetchall()
            if not db_server_levels:
                return await ctx.send(choice(vocabulary.level.no_info))
            db_user_level, db_user_xp = db.execute('SELECT level, xp FROM "default".users_levels WHERE server_id = %s and user_id = %s', [db_server_id, db_user_id]).fetchone()
            db_user_level = vocabulary.level.no_level if not get(server.roles, id=db_user_level) else get(server.roles, id=db_user_level).mention
            embed = discord.Embed(
                title=vocabulary.level.title.format(user.name),
                description=choice(vocabulary.level.description_start) + vocabulary.level.description_end.format(user.mention, db_user_level, db_user_xp),
                colour=colour
            )
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(name=commands_names.dashboard)
    async def level_dashboard(self, ctx, limit=10):
        vocabulary = speech_setting(ctx.guild.id).level_system
        server = ctx.guild
        server_id = server.id
        with Database() as db:
            db_server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [server_id]).fetchone()[0]
            db_server_levels = db.execute('SELECT level_id FROM "default".servers_levels WHERE server_id = %s', [db_server_id]).fetchall()
            if not db_server_levels:
                return await ctx.send(choice(vocabulary.level_dashboard.no_info))
            embed = discord.Embed(
                title=vocabulary.level_dashboard.title,
                colour=colour
            )
            embed.set_thumbnail(url=server.icon_url)
            db.execute('SELECT user_id, level, xp FROM "default".users_levels WHERE server_id = %s ORDER BY xp DESC LIMIT %s', [db_server_id, limit])
            data = []
            for db_user_id, db_user_level, db_user_xp in db.fetchall():
                user_id = db.execute('SELECT discord_user_id FROM "default".users WHERE id = %s', [db_user_id]).fetchone()[0]
                user = get(server.members, id=user_id)
                print(user, user_id)
                level = vocabulary.level_dashboard.no_level if not get(server.roles, id=db_user_level) else get(server.roles, id=db_user_level).mention
                data.append([user, level, db_user_xp])
            for i in range(min(3, len(data))):
                user, level, xp = data[i]
                embed.add_field(
                    name=f"{i + 1}. {user.name}",
                    value=f"{getattr(vocabulary.level_dashboard.top_three_phrases, str(i + 1))} {user.mention}\n**level: {level}\nxp: {xp}**",
                    inline=False
                )
            data = data[min(3, len(data)):]
            output = []
            for pos, line in enumerate(data):
                user, level, xp = line
                output.append(f"**{pos + 4}.{user.mention}** - {' '.join([level, f'**{xp} xp**'])}")
            if output:
                embed.add_field(
                    name=choice(vocabulary.level_dashboard.embed_field_title),
                    value="\n".join(output),
                    inline=False
                )
            await ctx.send(embed=embed)
