import discord
from discord.ext import commands
import wikipedia
from random import choice
from cogs.commands import commands_names
from cogs.config import prefix


class Wikipedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        wikipedia.set_lang("ru")

    @commands.command(name="wp")
    async def wikipedia_search(self, ctx, *message):
        try:
            await ctx.send(wikipedia.summary(message))
        except Exception:
            await ctx.send(choice([
                "Внучок, я не ебу что это", "Сынок, нихуя не нашел", "Малыш, в душе не ебу что ты мне накакал"
            ]))
