import discord
from discord.ext import commands
import random
import requests
from cogs.config import *


class MiniCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="toss")
    async def heads_or_tails(self, ctx):
        answers = [":bird: Орел :bird:", ":coin: Решка :coin:"]
        await ctx.send(random.choice(answers))

    @commands.command(name="8ball")
    async def magic_ball(self, ctx, *message):
        message = " ".join(message)
        embed = discord.Embed(
            title=":crystal_ball: говорит: " + random.choice("да, нет, возможно, я не знаю, скорее всего да, скорее всего нет, определенно нет, определенно да, 50/50, лучше вам не знать".split(", ")),
            colour=discord.Colour.purple()
        )
        embed.set_footer(text=f"Вопрос: {message}")
        await ctx.send(embed=embed)

    @commands.command(name="forecast")
    async def get_forecast(self, ctx, *, place: str):
        place = " ".join(place)
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

    @get_forecast.error
    async def get_forecast_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Вы не указали место")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Вы неверно указали место")
