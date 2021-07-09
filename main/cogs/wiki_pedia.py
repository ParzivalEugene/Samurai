from random import choice
import discord
import wikipedia
from discord.ext import commands
from main.cogs.commands import commands_names as cs
from main.cogs.glossary import speech_setting, current_language
from main.cogs.config import colour

commands_names = cs.wikipedia


class Wikipedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=commands_names.wikipedia_search)
    async def wikipedia_search(self, ctx, *message):
        wikipedia.set_lang(current_language(ctx.guild.id))
        vocabulary = speech_setting(ctx.guild.id).wikipedia
        if not message:
            return await self.wikipedia_search_error(ctx, commands.MissingRequiredArgument)
        try:
            if message[0] == "<@!825433682205606000>":
                site = "https://samuraibot.brizy.site/"
                embed = discord.Embed(
                    description=choice(vocabulary.wikipedia_search.description_about_me).format(site),
                    colour=colour
                )
                return await ctx.send(embed=embed)
            await ctx.send(wikipedia.summary(message))
        except Exception:
            await ctx.send(choice(vocabulary.wikipedia_search.error))

    @wikipedia_search.error
    async def wikipedia_search_error(self, ctx, error):
        vocabulary = speech_setting(ctx.guild.id).wikipedia
        if isinstance(error, commands.MissingRequiredArgument) or error == commands.MissingRequiredArgument:
            return await ctx.send(choice(vocabulary.wikipedia_search_error.MissingRequiredArgument))
        if isinstance(error, commands.BadArgument):
            await ctx.send(choice(vocabulary.wikipedia_search_error.BadArgument))
