import discord
from discord.ext import commands
from cogs.birthdays import Birthdays
# from cogs.tic_tac_toe_game import TicTacToeGame
# from cogs.connect_four import ConnectFour
from cogs.chatting import Chatting
from cogs.click_to_roles import ClickToRoles
from cogs.config import *
from cogs.glossary import Glossary
from cogs.level_system import LevelSystem
from cogs.mini_cogs import MiniCogs
from cogs.on_events_checker import OnEventsChecker
from cogs.music_player import Music
from cogs.translator import DeepTranslator
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
    await Birthdays(bot).check_birthdays.start()


bot.add_cog(Birthdays(bot))
bot.add_cog(MiniCogs(bot))
bot.add_cog(Chatting(bot))
# bot.add_cog(ConnectFour(bot))
# bot.add_cog(TicTacToeGame(bot))
bot.add_cog(Music(bot))
bot.add_cog(DeepTranslator(bot))
bot.add_cog(ClickToRoles(bot))
bot.add_cog(Wikipedia(bot))
bot.add_cog(LevelSystem(bot))
bot.add_cog(OnEventsChecker(bot))
bot.add_cog(Glossary(bot))
keep_alive()
bot.run(token_for_bot)
