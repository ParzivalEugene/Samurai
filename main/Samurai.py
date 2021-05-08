import discord
from discord.ext import commands
from cogs.config import *
from cogs.tic_tac_toe import TicTacToe
from cogs.connect_four import ConnectFour
from cogs.chatting import Chatting
from cogs.mini_cogs import MiniCogs
from cogs.birthdays import Birthdays
from cogs.music_player import Player
from cogs.translator import DeepTranslator
from cogs.click_to_roles import ClickToRoles
from cogs.level_system import LevelSystem
from cogs.wiki_pedia import Wikipedia
from keep_alive import keep_alive


bot = commands.Bot(command_prefix=prefix, help_command=None, intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f"{prefix}help - INVINCIBLE WARRIORS")
    )
    await Birthdays(bot).check_birthday.start()


bot.add_cog(Birthdays(bot))
bot.add_cog(MiniCogs(bot))
bot.add_cog(Chatting(bot))
bot.add_cog(ConnectFour(bot))
bot.add_cog(TicTacToe(bot))
bot.add_cog(Player(bot))
bot.add_cog(DeepTranslator(bot))
bot.add_cog(ClickToRoles(bot))
bot.add_cog(Wikipedia(bot))
bot.add_cog(LevelSystem(bot))
keep_alive()
bot.run(token_for_bot)
