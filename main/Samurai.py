import discord
from discord.ext import commands, tasks
from cogs.config import *
from cogs.level_system import LevelSystem
from cogs.tic_tac_toe import TicTacToe
from cogs.connect_four import ConnectFour
from cogs.chatting import Chatting
from cogs.mini_cogs import MiniCogs
from cogs.birthdays import Birthdays
from keep_alive import keep_alive

bot = commands.Bot(command_prefix=prefix, help_command=None)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f"{prefix}help - INVINCIBLE WARRIORS")
    )
    await Birthdays(bot).check_birthday.start()


@bot.command(name="help")
async def my_help(ctx):
    embed = discord.Embed(
        title=f"Информация обо мне",
        description="Распиздатый ботяра! За себя постою, нахуй пошлю, в игры поиграю... блять да я все умею",
        colour=discord.Colour.purple()
    )
    embed.set_footer(text="Say your prayers, Moron!")
    embed.set_image(url="https://cdn.discordapp.com/attachments/783747422898880533/828266665602580500/ghostrunner-review.jpg")
    embed.add_field(name="Команды",
                    value=f"""**{prefix}help** - вывод информации о боте.
**{prefix}xo_rules** - вывод информации о крестиках-ноликах.
**{prefix}bd_rules** - вывод информации о днях рождения.
**{prefix}c4_rules** - вывод информации о 4 в ряд.
**{prefix}forecast <place>** - вывод прогноза погоды в указанном месте.
**{prefix}8ball <message>** - магический ответит на вопрос.
**{prefix}toss** - орел или решка.
__Все команды вводятся **латинскими буквами**__""",
                    inline=False)
    await ctx.send(embed=embed)


bot.add_cog(Birthdays(bot))
bot.add_cog(MiniCogs(bot))
bot.add_cog(Chatting(bot))
bot.add_cog(ConnectFour(bot))
bot.add_cog(TicTacToe(bot))
bot.add_cog(LevelSystem(bot))
keep_alive()
bot.run(token_for_bot)
