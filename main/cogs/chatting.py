import discord
from discord.ext import commands
import json
import requests
import re


class Chatting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.phrases = {
            "insults": [
                "ботяра пидор", "бот говно", "говно бот", "долбаеб бот", "бот долбаеб", "бот пидор"
            ],
            "compliments": ["бот " + i for i in "ахуенный, классный, крутой, заебатый, милый, пиздатый".split(", ")] + [i + " бот" for i in "ахуенный, классный, крутой, заебатый, милый, "
                                                                                                                                            "пиздатый".split(", ")],
            "sad": [
                "грустно", "одиноко", "печально", "горько", "тоскливо", "хуево", "умираю"
            ]
        }

    @staticmethod
    def get_quote():
        """Return random quote"""
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = ' - '.join([json_data[0]['q'], json_data[0]['a']])
        return quote

    def get_emoji(self, name):
        """Return emoji by name"""
        return discord.utils.get(self.bot.emojis, name=name)

    @staticmethod
    def embed_cat(author):
        """Return the embed with random kitty"""
        response = requests.get("https://aws.random.cat/meow")
        data = response.json()
        embed = discord.Embed(
            title="Котик :smiling_face_with_3_hearts:",
            description=f"Прямо как ты {author.mention}",
            colour=discord.Colour.purple()
        )
        embed.set_image(url=data["file"])
        embed.set_footer(text="")
        return embed

    @staticmethod
    def embed_dog(author):
        """Return the embed with random doggy"""
        allowed_extension = ['jpg', 'jpeg', 'png']
        file_extension, url = '', ''
        while file_extension not in allowed_extension:
            contents = requests.get('https://random.dog/woof.json').json()
            url = contents['url']
            file_extension = re.search("([^.]*)$", url).group(1).lower()
        data = url
        embed = discord.Embed(
            title="Пёсик :smiling_face_with_3_hearts:",
            description=f"Прямо как ты {author.mention}",
            colour=discord.Colour.purple()
        )
        embed.set_image(url=data)
        embed.set_footer(text="")
        return embed

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.bot.get_channel(783742051556655174).send(member.name, "присоединлся к серверу")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.bot.get_channel(783742051556655174).send(member.name, "покинул сервер")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Reacting on messages and send request by phrase"""
        msg = message.content.lower()
        if message.author == self.bot.user:
            return

        """Commands ------------------------------------------------------------------------------"""

        if msg.startswith("кот"):
            await message.channel.send(embed=self.embed_cat(message.author))
        elif any(msg.startswith(i) for i in ("пес", "соба")):
            await message.channel.send(embed=self.embed_dog(message.author))
        elif msg.startswith("вдохновение"):
            await message.channel.send(self.get_quote())

        """Reacting on basic phrases -------------------------------------------------------------"""

        if msg.startswith("привет"):
            await message.channel.send("Приветствую вас!")
        elif msg.startswith("нахуй юлю"):
            await message.channel.send("туда ее")
            await message.channel.send(self.get_emoji("julia"))
        elif any(phrase in msg for phrase in self.phrases["insults"]):
            await message.channel.send("мать твоя блять, сын собаки")
            await message.channel.send(self.get_emoji('kavo'))
        elif any(phrase in msg for phrase in self.phrases["compliments"]):
            await message.channel.send("люблю тебя зайка " + str(self.get_emoji("wowcry")))
        elif any(phrase in msg for phrase in self.phrases["sad"]):
            await message.channel.send("не грусти зайка, вот тебе котик")
            await message.channel.send(embed=self.embed_cat(message.author))
        elif msg.startswith("арина сука"):
            await message.channel.send("согласен")
            await message.channel.send(self.get_emoji("ahuet"))
