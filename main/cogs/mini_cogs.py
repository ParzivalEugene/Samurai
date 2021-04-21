import discord
from discord.ext import commands
import random
import requests
from cogs.config import *
from cogs.commands import commands_names
import json
from random import choice
from deep_translator import GoogleTranslator


class MiniCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=commands_names["mini cogs"]["head or tails"])
    async def heads_or_tails(self, ctx):
        answers = [":bird: Орел :bird:", ":coin: Решка :coin:"]
        await ctx.send(random.choice(answers))

    @commands.command(name=commands_names["mini cogs"]["magic ball"])
    async def magic_ball(self, ctx, *message):
        message = " ".join(message)
        embed = discord.Embed(
            title=":crystal_ball: говорит: " + random.choice("да; нет; возможно; я не знаю; скорее всего да; скорее всего нет; мать ставлю, что нет; 50/50; мать ставлю, что да".split("; ")),
            colour=discord.Colour.purple()
        )
        embed.set_footer(text=f"Вопрос: {message}")
        await ctx.send(embed=embed)

    @commands.command(name=commands_names["mini cogs"]["get forecast"])
    async def get_forecast(self, ctx, *, place: str):
        response = requests.get("http://api.openweathermap.org/data/2.5/find",
                                params={
                                    "q": place,
                                    "lang": "ru",
                                    "units": "metric",
                                    "APPID": app_id_for_forecast
                                }).json()
        if response["cod"] != "200":
            await ctx.send("Не удалось найти информацию")
            return
        response = response["list"][0]
        embed = discord.Embed(
            title=f"Погода в {place}",
            description=f"В {place} сейчас {response['main']['temp']}°С, {response['weather'][0]['description']}",
            colour=discord.Colour.purple()
        )
        embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{response['weather'][0]['icon']}.png")
        await ctx.send(embed=embed)

    @commands.command(name=commands_names["mini cogs"]["quote"])
    async def get_quote(self, ctx):
        """Return random quote"""
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = ' - '.join([json_data[0]['q'], json_data[0]['a']])
        translated_message = GoogleTranslator(source="en", target="ru").translate(quote)
        embed = discord.Embed(
            title="Вдохновение",
            description=translated_message,
            colour=discord.Colour.purple()
        )
        embed.set_footer(text=f"original: {quote}")
        await ctx.send(embed=embed)

    @get_forecast.error
    async def get_forecast_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(choice([
                "Молодой я ебу в каком городе ты хочешь узнать прогоз", "Внучок а место то какое", "Сынок а где город то"
            ]))
        if isinstance(error, commands.BadArgument):
            await ctx.send("Вы неверно указали место")
