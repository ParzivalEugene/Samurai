import discord
from discord.ext import commands


class ClickToRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message = 836281009757618248
        self.roles = {
            "peepohappy": "minecraft",
            "body": "CS:GO",
            "wowcry": "valorant",
            "sho": "MAFIA",
            "peepoban": "dying light",
            "angryping": "warzone",
            "nigger": "GTA V",
            "gomer": "among us"
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.message == payload.message_id:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda x: x.id == guild_id, self.bot.guilds)
            if payload.emoji.name in self.roles.keys():
                role = discord.utils.get(guild.roles, name=self.roles[payload.emoji.name])
                member = discord.utils.find(lambda x: x.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if self.message == payload.message_id:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda x: x.id == guild_id, self.bot.guilds)
            if payload.emoji.name in self.roles.keys():
                role = discord.utils.get(guild.roles, name=self.roles[payload.emoji.name])
                member = discord.utils.find(lambda x: x.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
