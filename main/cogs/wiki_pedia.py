import discord
from discord.ext import commands
import wikipedia
from random import choice
from cogs.commands import commands_names
from cogs.config import prefix


class Wikipedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.site = "https://samuraibot.brizy.site/"
        wikipedia.set_lang("ru")

    @commands.command(name="wp")
    async def wikipedia_search(self, ctx, *message):
        try:
            if message[0] == "<@!825433682205606000>":
                embed = discord.Embed(
                    description=choice([
                        f"Внучок, не льсти мне, про меня еще нет википедии, зато ты можешь рассказать обо мне своим друзьям, вот [сайтик про меня]({self.site})",
                        f"Зайка не льсти мне, про меня еще нет вики, зато ты можешь посмотреть на [сайт про меня]({self.site}) и рассказать друзьям"
                    ]),
                    colour=discord.Colour.purple()
                )
                return await ctx.send(embed=embed)
            await ctx.send(wikipedia.summary(message))
        except Exception:
            await ctx.send(choice([
                "Внучок, я не ебу что это", "Сынок, нихуя не нашел", "Малыш, в душе не ебу что ты мне накакал"
            ]))
