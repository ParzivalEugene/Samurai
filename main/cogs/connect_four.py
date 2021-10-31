import discord
from discord.ext import commands
from random import choice
from cogs.config import colour
from cogs.commands import commands_names
from cogs.config import colour
from cogs.commands import commands_names as cs
from cogs.glossary import speech_setting


commands_names = cs.music_player
BOARD_CELLS = {
    0: ":white_large_square:",
    1: ":blue_square:",
    2: ":yellow_square:"
}
GAME_TYPES = {
    0: "PvP",
    1: "PvRandom",
    2: "PvAI"
}


class ConnectFour(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(name=commands_names.)
