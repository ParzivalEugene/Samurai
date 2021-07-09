import discord
from discord.ext import commands
import json
from random import choice
import requests
from deep_translator import GoogleTranslator
from main.cogs.config import colour
from main.cogs.commands import commands_names as cs
from main.cogs.config import *
from main.cogs.glossary import speech_setting

commands_names = cs.mini_cogs


class MiniCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=commands_names.help)
    async def help(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).mini_cogs
        embed = discord.Embed(
            title=vocabulary.help.title,
            colour=colour
        )
        embed.add_field(
            name=vocabulary.help.name,
            value=vocabulary.help.value,
            inline=False
        )
        await ctx.send(embed=embed)

    @commands.command(name=commands_names.head_or_tails)
    async def heads_or_tails(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).mini_cogs
        await ctx.send(choice(vocabulary.heads_or_tails))

    @commands.command(name=commands_names.magic_ball)
    async def magic_ball(self, ctx, *message):
        vocabulary = speech_setting(ctx.guild.id).mini_cogs
        message = " ".join(message)
        embed = discord.Embed(
            title=vocabulary.magic_ball.title_start + choice(vocabulary.magic_ball.title_end),
            colour=colour
        )
        embed.set_footer(text=vocabulary.magic_ball.footer.format(message))
        await ctx.send(embed=embed)

    @commands.command(name=commands_names.get_forecast)
    async def get_forecast(self, ctx, *, place: str):
        vocabulary = speech_setting(ctx.guild.id).mini_cogs
        response = requests.get("http://api.openweathermap.org/data/2.5/find",
                                params={
                                    "q":     place,
                                    "lang":  vocabulary.get_forecast.lang,
                                    "units": "metric",
                                    "APPID": app_id_for_forecast
                                }).json()
        if response["cod"] != "200":
            await ctx.send(choice(vocabulary.get_forecast.error))
            return
        response = response["list"][0]
        embed = discord.Embed(
            title=vocabulary.get_forecast.title.format(place),
            description=vocabulary.get_forecast.description.format(place, response['main']['temp'], response['weather'][0]['description']),
            colour=colour
        )
        embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{response['weather'][0]['icon']}.png")
        await ctx.send(embed=embed)

    @commands.command(name=commands_names.get_quote)
    async def get_quote(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).mini_cogs
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = ' - '.join([json_data[0]['q'], json_data[0]['a']])
        translated_message = GoogleTranslator(source="en", target=vocabulary.get_quote.target).translate(quote)
        embed = discord.Embed(
            title=vocabulary.get_quote.title,
            description=translated_message,
            colour=colour
        )
        if vocabulary.get_quote.target != "en":
            embed.set_footer(text=vocabulary.get_quote.footer.format(quote))
        await ctx.send(embed=embed)

    @get_forecast.error
    async def get_forecast_error(self, ctx, error):
        vocabulary = speech_setting(ctx.guild.id).mini_cogs
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(choice(vocabulary.get_forecast_error.MissingRequiredArgument))
        if isinstance(error, commands.BadArgument):
            await ctx.send(choice(vocabulary.get_forecast_error.BadArgument))
