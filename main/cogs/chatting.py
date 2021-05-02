import discord
from discord.ext import commands
from cogs.config import *
from cogs.commands import commands_names
from random import choice
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

        # url = "https://dog.ceo/api/breeds/image/random"
        # response = requests.get(url=url).json()
        # data = response["message"]
        data = url
        embed = discord.Embed(
            title="Пёсик :smiling_face_with_3_hearts:",
            description=f"Прямо как ты {author.mention}",
            colour=discord.Colour.purple()
        )
        embed.set_image(url=data)
        embed.set_footer(text="")
        return embed

    @commands.command(name=commands_names["chatting"]["help"])
    async def my_help(self, ctx):
        embed = discord.Embed(
            title=f"SAMURAI",
            description="Я пиздатый, на хуйню я слил зарплату. Братик я заменю тебе мать и отца блять, я умею все. Какой-нибудь пидорас обижает, пиши мне - разобьем ему ебало. Можешь играть через "
                        f"меня в игры с друзьями (если есть {self.get_emoji('kavo')}). Могу тебе на шарманочке поиграть, монетку подкинуть или судьбу рассказать. Хочешь перевести что-нибудь, "
                        f"или определить, что за язык, пиши мне ебана, все расскажу. Тебе нужна система уровней и модерация на сервере, ебать есть я. Хочешь чтобы твои друзья знали когда у кого "
                        f"день рождения, ебать да я создам отдельную базу данных для тебя. Как ты понял я бля ахуенный, вот список комманд.",
            colour=discord.Colour.purple()
        )
        embed.set_footer(text="Say your prayers, Moron!")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/783747422898880533/828266665602580500/ghostrunner-review.jpg")
        embed.add_field(
            name="Воспроизведение музыки :track_previous: :stop_button: :play_pause:",
            value=f"""Этот модуль был создан, чтобы ты мог чилить со своими друзьями в голосовом канале и параллельно слушать любимый музон {self.get_emoji("sadpanda")}
**{prefix}{commands_names["music player"]["help"]}** - отдельный эмбед для вывода помощи по плэеру
**{prefix}{commands_names["music player"]["join"]}** - зайду в голосовой канала, в котором находится автор сообщения.
**{prefix}{commands_names["music player"]["leave"]}** - уйду из голосового канала
**{prefix}{commands_names["music player"]["queue"]}** - выведу очередь треков
**{prefix}{commands_names["music player"]["queue"]} <url>** - добавлю в очередь трек
**{prefix}{commands_names["music player"]["remove"]} <number>** - удалю трек под номером <number>
**{prefix}{commands_names["music player"]["play"]}** - начну играть музыку из очереди
**{prefix}{commands_names["music player"]["pause"]}** - поставлю на паузу шарманку
**{prefix}{commands_names["music player"]["resume"]}** - воспроизведу воспроизведение {self.get_emoji('sho')}
**{prefix}{commands_names["music player"]["stop"]}** - уберу трек из очереди и остановлю проигрывание""",
            inline=False
        )
        embed.add_field(
            name="Крестики-нолики :negative_squared_cross_mark: :o2:",
            value=f"""Модуль с крестиками-ноликами для игр с друзьями или мной
**{prefix}{commands_names["tic tac toe"]["help"]}** - отдельный эмбед для вывода инфы о крестиках ноликах
**{prefix}{commands_names["tic tac toe"]["rules"]}** - отдельный эмбед для вывода правил крестиков ноликов
**{prefix}{commands_names["tic tac toe"]["init game"]} <member1> <member2>** - начало игры с указанием двух юзеров
**{prefix}{commands_names["tic tac toe"]["place"]} <number>** - поместит нужный символ в клетку
:one: :two: :three:
:four: :five: :six:
:seven: :eight: :nine:
**{prefix}{commands_names["tic tac toe"]["lose"]}** - текущий игрок сдастся""",
            inline=False
        )
        embed.add_field(
            name="Четыре в ряд :blue_square: :yellow_square:",
            value=f"""Аналогичный модуль крестикам-ноликам, катай с друзьями или со мной
**{prefix}{commands_names["connect four"]["help"]}** - отдельный эмбед для вывода инфы о четыре в ряд
**{prefix}{commands_names["connect four"]["rules"]}** - отдельный эмбед для вывода правил четыре в ряд
**{prefix}{commands_names["connect four"]["init game"]} <member1> <member2>** - начало игры с указанием двух участников
**{prefix}{commands_names["connect four"]["place"]} <number>** - бросок фишки в колонку с указанным номером
**{prefix}{commands_names["connect four"]["lose"]}** - текущий игрок сдастся""",
            inline=False
        )
        embed.add_field(
            name=f"Дни рождения {self.get_emoji('wowcry')}",
            value=f"""Я, в отличии от друзей, всегда поздравлю тебя в тот самый день
**{prefix}{commands_names["birthdays"]["help"]}** - поможет тебе понять как устроен модуль Birthdays.
**{prefix}{commands_names["birthdays"]["add"]} <year> <month> <day>** - внос в базу данных с указанием года, месяца и дня.
**{prefix}{commands_names["birthdays"]["up"]} <year> <month> <day>** - обновит текущую дату.
**{prefix}{commands_names["birthdays"]["delete"]}** - удалит данные из базы.
**{prefix}{commands_names["birthdays"]["show bd"]}** - выведет эмбед о вас.
**{prefix}{commands_names["birthdays"]["show bds"]}** - выводит список всех дней рождений сервера.""",
            inline=False
        )
        embed.add_field(
            name=f"{self.get_emoji('reeee')} Модуль переводчик {self.get_emoji('thinksmart1')}",
            value=f"""Я смогу перевести все что ты захочешь с любого на любой язык, определить язык тоже не проблема. Также можем поиграть в игру угадай язык.
**{prefix}{commands_names["translator"]["help"]}** - помогу тебе отдельным эмбедом со всеми командами
**{prefix}{commands_names["translator"]["list of languages"]}** - в следующих командах и играх ты должен будешь вводить язык и для упрощения я ввел систему кратких обозначений, эта команда выведет их
**{prefix}{commands_names["translator"]["translate"]} <source lang> <target lang> <message>** - переведу фразу с исходного языка на итоговый
**{prefix}{commands_names["translator"]["translate"]} <target lang> <message>** - сам определю исходный язык и переведу тебе все на указанный язык (иногда могу ошибаться, тогда юзай команду выше)
**{prefix}{commands_names["translator"]["detect language"]} <message>** - выведу тебе язык исходного сообщения
**{prefix}{commands_names["translator"]["game detect languages"]}** - начну игру "угадай язык" и буду ждать твоего ответа""",
            inline=False
        )
        embed.add_field(
            name="Система уровней :bar_chart:",
            value=f"""Модуль, созданный для создания классового неравенста на сервере, повышения активности в чатах и конкурентности.
**{prefix}{commands_names["level"]["help"]}** - поможет тебе понять как устроен модуль LevelSystem.
**{prefix}{commands_names["level"]["add"]} <role> <xp>** - внос в базу данных с указанием роли и количество опыта для ее получения.
**{prefix}{commands_names["level"]["up"]} <role> <xp>** - обновит данную роль.
**{prefix}{commands_names["level"]["delete"]}** - удалит роль из базы данных.
**{prefix}{commands_names["level"]["show levels"]}** - выведет список всех уровней сервера и количество опыта для их получения.
**{prefix}{commands_names["level"]["show level"]}** - выведет эмбед о вашем уровне.
**{prefix}{commands_names["level"]["dashboard"]}** - выведет топ участников сервера."""
        )
        embed.add_field(
            name=f"Прочие команды {self.get_emoji('peepoban')}",
            value=f"""Команды, которые я в душе не ебу в какой модуль пихать, поэтому считай что это некий unsorted. Сборник мелких забавных команд.
**{prefix}{commands_names["mini cogs"]["head or tails"]}** - подкинет монетку
**{prefix}{commands_names["mini cogs"]["magic ball"]} <message>** - дам тебе ответы на все вопросы {self.get_emoji('reeee')}
**{prefix}{commands_names["mini cogs"]["get forecast"]} <place>** - выведу прогноз погоды в заданном месте
**{prefix}{commands_names["mini cogs"]["quote"]}** - вдохновлю тебя на великие свершения""",
            inline=False
        )
        embed.add_field(
            name=f"Реакции на сообщения {self.get_emoji('peepohappy')}",
            value=f"Я блять считай как живой, реагирую на все обращения к себе. Будете обижать меня - буду хуярить в ответ у бля {self.get_emoji('fuck')}. Если тебе грустно - кину тебе котика. "
                  f"Скажешь что я пиздатый - я тебя расцелую сладенький мой {self.get_emoji('giggle')}. Напишешь кот или кошка - кину котика, такая же хуйня с собакой или песиком. Короче будь "
                  "лапочкой, я слежу за тобой, малыш."
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(choice([
                "Внучок, я таких команд не знаю", "Боевой это чо за команда", "*\Бип\* - *\Боп\* неизвестная мне команда"
            ]))
        if error:
            raise error

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(783742051556655174)  # участники
        await channel.send(member.mention, "присоединлся к серверу")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(783742051556655174)  # участники
        await channel.send(member.mention, "покинул сервер")

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

        """Reacting on basic phrases -------------------------------------------------------------"""

        if msg.startswith("привет"):
            await message.channel.send("Приветствую вас!")
        elif msg.startswith("нахуй юлю"):
            await message.channel.send("туда ее")
            await message.channel.send(self.get_emoji("julia"))
        elif any(phrase in msg for phrase in self.phrases["insults"]):
            await message.channel.send(choice([
                f"Блять обижать старого решил сука, я же тебе ебальник набью, понял? Я уже договорился, за тобой едут, последний понедельник блять живешь {self.get_emoji('ahuet')}",
                f"Мать твоя блять сын собаки {self.get_emoji('kavo')}", f"Попущенных никто не спрашивал {self.get_emoji('fuck')}"
            ]))
        elif any(phrase in msg for phrase in self.phrases["compliments"]):
            await message.channel.send(choice([
                f"Ты же мой пупсик сладенький, люблю тебя {self.get_emoji('wowcry')}", f"Бля я тебя обожаю солнышко мое {self.get_emoji('pandalove')}",
                f"Блять какой же ты зайка, ты меня смущаешь {self.get_emoji('giggle')}", "Целую мое солнышко в лобик", "Ты экстра супер пупсик :heart:"
            ]))
        elif any(phrase in msg for phrase in self.phrases["sad"]):
            await message.channel.send("не грусти зайка, вот тебе котик")
            await message.channel.send(embed=self.embed_cat(message.author))
        elif msg.startswith("арина сука"):
            await message.channel.send("согласен")
            await message.channel.send(self.get_emoji("ahuet"))

    @commands.has_permissions(administrator=True)
    @commands.command(name="print_click_to_role")
    async def test(self, ctx):
        embed = discord.Embed(
            title="Click to role",
            description=f"**Wassup mate**{self.get_emoji('hattip')}! Если ты не хочешь остаться голым пупсиком без роли, то тебе несказанно повезло. Снизу ты видишь список из эмодзи, нажав на которые"
                        f" , ты щас ахуеешь, **ТЫ ПОЛУЧИШЬ РОЛЬ**. Я знаю, что ты в ахуе {self.get_emoji('kavo')}, поэтому забирай роли быстрее, пока я не передумал!!! \n\n" +
                        f"""{self.get_emoji("peepohappy")} - **Minecraft**

{self.get_emoji("body")} - **CS:GO**

{self.get_emoji("wowcry")} - **Valorant**

{self.get_emoji("sho")} - **Mafia**

{self.get_emoji("peepoban")} - **Dying Light**

{self.get_emoji("angryping")} - **Warzone**

{self.get_emoji("nigger")} - **GTA V**

{self.get_emoji("gomer")} - **Among Us**""",
            colour=discord.Colour.purple()
        )
        message = await ctx.send(embed=embed)
        await message.add_reaction(self.get_emoji("peepohappy"))
        await message.add_reaction(self.get_emoji("body"))
        await message.add_reaction(self.get_emoji("wowcry"))
        await message.add_reaction(self.get_emoji("sho"))
        await message.add_reaction(self.get_emoji("peepoban"))
        await message.add_reaction(self.get_emoji("angryping"))
        await message.add_reaction(self.get_emoji("nigger"))
        await message.add_reaction(self.get_emoji("gomer"))

    @commands.has_permissions(administrator=True)
    @commands.command(name="print_greeting_message")
    async def greet(self, ctx):
        embed = discord.Embed(
            title="ДОБРО ПОЖАЛОВАТЬ В INVINCIBLE WARRIORS",
            description=f"**Wassup samurai!** Приветствуем тебя на великолемном сервере {self.get_emoji('bulka')}\nЗдесь ты найдешь все что необходимо: **друзей, общение и голые сиськи** "
                        f"{self.get_emoji('giggle')}\n\nПо всем интересующим тебя вопросам ты можешь обращаться к {discord.utils.get(ctx.guild.roles, name='SHOGUNS').mention} или к пожилому "
                        f"{self.bot.get_user(414105456907386886).mention}\n\nОбщая информация сервера:",
            colour=discord.Colour.purple()
        )
        embed.add_field(
            name="Уведомления стримов",
            value=f"{self.bot.get_channel(783744382569676850).mention} Здесь будут отображаться активные трансляции элиты сервера",
            inline=False
        )
        embed.add_field(
            name="Уведомления сервера",
            value=f"{self.bot.get_channel(783721528532926494).mention} Важная инфа о событиях на сервере",
            inline=False
        )
        embed.add_field(
            name="Click to role",
            value=f"{self.bot.get_channel(783744626338037850).mention} Канал для получения необходимой роли",
            inline=False
        )
        embed.add_field(
            name="Главная зона для общения",
            value=f"{self.bot.get_channel(690640059015102485).mention} Канал для получения необходимой роли",
            inline=False
        )
        embed.add_field(
            name="Инфа обо мне",
            value=f"Я - старичок {self.bot.user.mention}. Умею делать все и даже больше. Введи .help, чтобы узнать, что я умею"
        )
        await ctx.send(embed=embed)
