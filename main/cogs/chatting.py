import discord
from discord.ext import commands
from cogs.config import *
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

    @commands.command(name="help")
    async def my_help(self, ctx):
        embed = discord.Embed(
            title=f"SAMURAI",
            description="Я пиздатый, на хуйню я слил зарплату. Братик я заменю тебе мать и отца блять, я умею все. "
                        "Какой-нибудь пидорас обижает, пиши мне - разобьем ему ебало. Можешь играть через меня в игры "
                        f"с друзьями (если есть {self.get_emoji('kavo')}). Могу тебе на шарманочке поиграть, "
                        f"монетку подкинуть или судьбу рассказать. Как ты понял я бля ахуенный, вот список комманд.",
            colour=discord.Colour.purple()
        )
        embed.set_footer(text="Say your prayers, Moron!")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/783747422898880533/832654922952474674/20200121_182041.jpg")
        embed.set_image(url="https://cdn.discordapp.com/attachments/783747422898880533/828266665602580500/ghostrunner-review.jpg")
        embed.add_field(
            name="Воспроизведение музыки",
            value=f"""**{prefix}player_help** - отдельный эмбед для вывода помощи по плэеру
**{prefix}join** - зайду в голосовой канала, в котором находится автор сообщения.
**{prefix}leave** - уйду из голосового канала
**{prefix}queue** - выведу очередь треков
**{prefix}queue <url>** - добавлю в очередь трек
**{prefix}remove <number>** - удалю трек под номером <number>
**{prefix}play** - начну играть музыку из очереди
**{prefix}pause** - поставлю на паузу шарманку
**{prefix}resume** - воспроизведу воспроизведение {self.get_emoji('sho')}
**{prefix}stop** - уберу трек из очереди и остановлю проигрывание""",
            inline=False
        )
        embed.add_field(
            name="Крестики-нолики :negative_squared_cross_mark: :o2:",
            value=f"""**{prefix}xo_rules** - отдельный эмбед для вывода инфы о крестиках ноликах
**{prefix}xo <member1> <member2>** - начало игры с указанием двух юзеров
**{prefix}xo_place <number>** - поместит нужный символ в клетку
:one: :two: :three:
:four: :five: :six:
:seven: :eight: :nine:""",
            inline=False
        )
        embed.add_field(
            name="Четыре в ряд :blue_square: :yellow_square:",
            value=f"""**{prefix}c4_rules** - отдельный эмбед для вывода инфы о четыре в ряд
**{prefix}c4 <member1> <member2>** - начало игры с указанием двух участников
**{prefix}c4_place <number>** - бросок фишки в колонку с указанным номером""",
            inline=False
        )
        embed.add_field(
            name=f"Дни рождения {self.get_emoji('wowcry')}",
            value=f"""**{prefix}bd_help** - выведу тебе отдельную помощь по дням рождениям
**{prefix}bd <month> <day>** - для пользователей с высокой ролью есть возможность получить поздравления от меня, используя эту команду
**{prefix}bd_show** - выводит список дней рождений юзеров""",
            inline=False
        )
        embed.add_field(
            name=f"Прочие команды {self.get_emoji('peepoban')}",
            value=f"""**{prefix}toss** - подкинет монетку
**{prefix}8ball <message>** - дам тебе ответы на все вопросы {self.get_emoji('reeee')}
**{prefix}forecast <place>** - выведу прогноз погоды в заданном месте""",
            inline=False
        )
        embed.add_field(
            name="Реакции на сообщения",
            value=f"""Будете обижать меня - буду хуярить в ответ у бля {self.get_emoji("fuck")}.
Если тебе грустно - кину тебе котика. Скажешь что я пиздатый - я тебя расцелую сладенький мой {self.get_emoji("giggle")}.
Напишешь кот или кошка - кину котика, такая же хуйня с собакой или песиком.
Короче будь лапочкой, я слежу за тобой, малыш."""
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Пожилой, я таких команд не знаю")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, name='server_test')
        await channel.send(member.name, "присоединлся к серверу")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.channels, name='server_test')
        await channel.send(member.name, "покинул сервер")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Reacting on messages and send request by phrase"""
        msg = message.content.lower()
        if message.author == self.bot.user:
            return

        """Commands ------------------------------------------------------------------------------"""

        if any(msg.startswith(i) for i in ("кот", "кош", "cat", "kitty")):
            await message.channel.send(embed=self.embed_cat(message.author))
        elif any(msg.startswith(i) for i in ("пес", "соба", "dog", "woof")):
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

    @commands.command(name="r_test")
    async def test(self, ctx):
        await ctx.send("sh")
        print(1)
        await self.test1(ctx)

    async def test1(self, ctx):
        await ctx.send("sho???")
