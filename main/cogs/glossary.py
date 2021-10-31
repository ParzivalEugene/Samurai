from random import choice
import discord
from discord.ext import commands
from cogs.commands import commands_names as cs
from cogs.database_connector import Database
from cogs.vocabulary import vocabulary as vb
from cogs.config import colour

commands_names = cs.glossary


def speech_setting(server_id):
    with Database() as db:
        language, vibe = db.execute('SELECT language, vibe FROM "default".servers_languages_and_vibes '
                                    'WHERE server_id = (SELECT id FROM "default".servers WHERE discord_server_id = %s)', [server_id]).fetchone()
        return getattr(vb[language], vibe)


def current_language(server_id):
    with Database() as db:
        language = db.execute('SELECT language FROM "default".servers_languages_and_vibes '
                              'WHERE server_id = (SELECT id FROM "default".servers WHERE discord_server_id = %s)', [server_id]).fetchone()[0]
        return language


def current_vibe(server_id):
    with Database() as db:
        vibe = db.execute('SELECT vibe FROM "default".servers_languages_and_vibes '
                          'WHERE server_id = (SELECT id FROM "default".servers WHERE discord_server_id = %s)', [server_id]).fetchone()[0]
        return vibe


class Glossary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(commands_names.help)
    async def glossary_help(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).glossary
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
        embed.add_field(
            name=vocabulary.help.language_field.name,
            value="\n".join(vb.keys())
        )
        embed.add_field(
            name=vocabulary.help.vibe_field.name,
            value="\n".join(vb[current_language(ctx.guild.id)].__dict__.keys())
        )
        await ctx.send(embed=embed)

    @commands.command(commands_names.view_status)
    async def view_status(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).glossary
        with Database() as db:
            language, vibe = db.execute(
                'SELECT language, vibe FROM "default".servers_languages_and_vibes '
                'WHERE server_id = ('
                '   SELECT id FROM "default".servers'
                '   WHERE discord_server_id = %s)', [ctx.guild.id]
            ).fetchone()
            embed = discord.Embed(
                title=vocabulary.view_status.title.format(ctx.guild.name),
                description=vocabulary.view_status.description.format(language, vibe),
                colour=colour
            )
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.send(embed=embed)

    @commands.command(commands_names.set_language)
    async def set_language(self, ctx, language: str):
        vocabulary = speech_setting(ctx.guild.id).glossary
        if language not in vb.keys():
            return await ctx.send(choice(vocabulary.set_language.incorrect_language).format(", ".join(vb.keys())))
        with Database() as db:
            db.execute(
                'UPDATE "default".servers_languages_and_vibes '
                'SET language = %s WHERE server_id = ('
                '    SELECT id FROM "default".servers'
                '    WHERE discord_server_id = %s'
                ')', [language, ctx.guild.id]
            )
        vocabulary = speech_setting(ctx.guild.id).glossary
        await ctx.send(choice(vocabulary.set_language.success))

    @set_language.error
    async def set_language_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.view_status(ctx)

    @commands.command(commands_names.set_vibe)
    async def set_vibe(self, ctx, vibe: str):
        vocabulary = speech_setting(ctx.guild.id).glossary
        if vibe not in vb[current_language(ctx.guild.id)].__dict__.keys():
            return await ctx.send(choice(vocabulary.set_vibe.incorrect_vibe).format(", ".join(vb[current_language(ctx.guild.id)].__dict__.keys())))
        with Database() as db:
            db.execute(
                'UPDATE "default".servers_languages_and_vibes '
                'SET vibe = %s WHERE server_id = ('
                '    SELECT id FROM "default".servers'
                '    WHERE discord_server_id = %s'
                ')', [vibe, ctx.guild.id]
            )
        vocabulary = speech_setting(ctx.guild.id).glossary
        await ctx.send(choice(vocabulary.set_vibe.success))

    @set_vibe.error
    async def set_vibe_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.view_status(ctx)
