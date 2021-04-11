import discord
from discord.ext import commands
import json


class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles = ["SAMURAI", "DAIMYO", "METSUKE"]
        self.level_num = [5, 50, 100]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        with open("database/levels.json") as info:
            levels = json.load(info)
            if any(str(message.author.id) in i.keys() for i in levels["levels"]):
                levels["levels"][str(message.author.id)]["xp"] += 5
                xp = levels["levels"][0][str(message.author.id)]["xp"]
                level = 0
                while True:
                    if xp < 50 * (level ** 2) + 50 * (level - 1):
                        break
                    level += 1
                xp -= 50 * ((level - 1) ** 2) + 50 * (level - 1)
                if not xp:
                    await message.channel.send(f"Ебать пожилой {message.author.mention}, ты апнулся на **level: {level}**!")
                    levels["level"][]
                    for i in range(len(self.roles)):
                        if level == self.level_num[i]:
                            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=self.roles[i]))
                            embed = discord.Embed(
                                description=f"{message.author.mention} Поздравляю с новой ролью братик **{self.roles[i]}**"
                            )
                            embed.set_thumbnail(url=message.author.avatar_url)
                            await message.channel.send(embed=embed)
            else:
                levels.append({str(message.author.id): {"xp": 100, "level": 0}})
            with open("database/levels.json", "w") as outfile:
                json.dump(levels, outfile)

    @commands.command()
    async def rank(self, ctx):
        with open("database/levels.json") as info:
            levels = json.load(info)
            if any(str(ctx.author.id) in i.keys() for i in levels["levels"]):
                xp = levels["levels"][0][str(ctx.author.id)]["xp"]
                xp = levels["levels"][0][str(message.author.id)]["xp"]
                level = 0
                while True:
                    if xp < 50 * (level ** 2) + 50 * (level - 1):
                        break
                    level += 1
                xp -= 50 * ((level - 1) ** 2) + 50 * (level - 1)
                if not xp:
                    await message.channel.send(f"Ебать пожилой {message.author.mention}, ты апнулся на **level: {level}**!")
                    for i in range(len(self.roles)):
                        if level == self.level_num[i]:
                            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=self.roles[i]))
                            embed = discord.Embed(
                                description=f"{message.author.mention} Поздравляю с новой ролью братик **{self.roles[i]}**"
                            )
                            embed.set_thumbnail(url=message.author.avatar_url)
                            await message.channel.send(embed=embed)
            else:
                await ctx.send("Братик ты еще ничего писал, какой нахуй ранг")
