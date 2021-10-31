import re
import discord
import requests
from discord.ext import commands
from cogs.config import colour
from cogs.commands import commands_names as cs
from cogs.glossary import speech_setting, vb, current_language

commands_names = cs.chatting


class Chatting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_emoji(self, name):
        return discord.utils.get(self.bot.emojis, name=name)

    @staticmethod
    def embed_cat(author):
        vocabulary = speech_setting(author.guild.id).chatting
        response = requests.get("https://aws.random.cat/meow")
        data = response.json()
        embed = discord.Embed(
            title=vocabulary.embed_cat.title,
            description=vocabulary.embed_cat.description.format(author.mention),
            colour=colour
        )
        embed.set_image(url=data["file"])
        return embed

    @staticmethod
    def embed_meme(author):
        vocabulary = speech_setting(author.guild.id).chatting
        response = requests.get("https://some-random-api.ml/meme").json()
        url = response["image"]
        embed = discord.Embed(
            title=vocabulary.embed_meme.title,
            description=vocabulary.embed_meme.description.format(author.mention),
            colour=colour
        )
        embed.set_image(url=url)
        return embed

    @staticmethod
    def embed_dog(author):
        vocabulary = speech_setting(author.guild.id).chatting
        allowed_extension = ['jpg', 'jpeg', 'png']
        file_extension, url = '', ''
        while file_extension not in allowed_extension:
            contents = requests.get('https://some-random-api.ml/img/dog').json()
            url = contents['link']
            file_extension = re.search("([^.]*)$", url).group(1).lower()
        data = url
        embed = discord.Embed(
            title=vocabulary.embed_dog.title,
            description=vocabulary.embed_dog.description.format(author.mention),
            colour=colour
        )
        embed.set_image(url=data)
        return embed

    @commands.command(name=commands_names.help)
    async def my_help(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).chatting
        embed = discord.Embed(
            title=vocabulary.help.title,
            description=vocabulary.help.description,
            colour=colour
        )
        embed.set_footer(text=vocabulary.help.footer)
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        vocabulary = speech_setting(ctx.guild.id)
        embed.add_field(
            name=vocabulary.glossary.help.title + " " + vocabulary.glossary.help.description,
            value=vocabulary.glossary.help.value,
            inline=False
        )
        embed.add_field(
            name=vocabulary.glossary.help.language_field.name,
            value="\n".join(vb.keys())
        )
        embed.add_field(
            name=vocabulary.glossary.help.vibe_field.name,
            value="\n".join(vb[current_language(ctx.guild.id)].__dict__.keys())
        )
        embed.add_field(
            name=vocabulary.music_player.help.title + " " + vocabulary.music_player.help.description,
            value=vocabulary.music_player.help.value,
            inline=False
        )
        embed.add_field(
            name=vocabulary.tic_tac_toe_game.game_help.title + " " + vocabulary.tic_tac_toe_game.game_help.description,
            value=vocabulary.tic_tac_toe_game.game_help.value,
            inline=False
        )
        embed.add_field(
            name="ЧЕТЫРЕ В РЯД",
            value="В разработке",
            inline=False
        )
        embed.add_field(
            name=vocabulary.birthdays.help.title,
            value=vocabulary.birthdays.help.value,
            inline=False
        )
        embed.add_field(
            name=vocabulary.translator.help.title + " " + vocabulary.translator.help.description,
            value=vocabulary.translator.help.value,
            inline=False
        )
        embed.add_field(
            name=vocabulary.level_system.help.title + " " + vocabulary.level_system.help.description,
            value=vocabulary.level_system.help.value
        )
        embed.add_field(
            name=vocabulary.mini_cogs.help.title,
            value=vocabulary.mini_cogs.help.value,
            inline=False
        )
        await ctx.send(embed=embed)

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     """Reacting on messages and send request by phrase"""
    #     msg = message.content.lower()
    #     if message.author == self.bot.user:
    #         return
    #
    #     """Commands ------------------------------------------------------------------------------"""
    #
    #     if any(msg.startswith(i) for i in ("кот", "кош", "cat", "kitty")):
    #         await message.channel.send(embed=self.embed_cat(message.author))
    #     elif any(msg.startswith(i) for i in ("пес", "соба", "dog", "woof")):
    #         await message.channel.send(embed=self.embed_dog(message.author))
    #     elif any(msg.startswith(i) for i in ("meme", "мем", "мемчик", "мемас")):
    #         await message.channel.send(embed=self.embed_meme(message.author))
    #
    #     """Reacting on basic phrases -------------------------------------------------------------"""
    #
    #     if any(phrase in msg for phrase in self.phrases["insults"]):
    #         await message.channel.send(choice([
    #             f"Блять обижать старого решил сука, я же тебе ебальник набью, понял? Я уже договорился, за тобой едут, последний понедельник блять живешь {self.get_emoji('ahuet')}",
    #             f"Мать твоя блять сын собаки {self.get_emoji('kavo')}", f"Попущенных никто не спрашивал {self.get_emoji('fuck')}"
    #         ]))
    #     elif any(phrase in msg for phrase in self.phrases["compliments"]):
    #         await message.channel.send(choice([
    #             f"Ты же мой пупсик сладенький, люблю тебя {self.get_emoji('wowcry')}", f"Бля я тебя обожаю солнышко мое {self.get_emoji('pandalove')}",
    #             f"Блять какой же ты зайка, ты меня смущаешь {self.get_emoji('giggle')}", "Целую мое солнышко в лобик", "Ты экстра супер пупсик :heart:"
    #         ]))
    #     elif any(phrase in msg for phrase in self.phrases["sad"]):
    #         await message.channel.send("не грусти зайка, вот тебе котик")
    #         await message.channel.send(embed=self.embed_cat(message.author))

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
            colour=colour
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
            description=f"**Wassup samurai!** Приветствуем тебя на великолепном сервере {self.get_emoji('bulka')}\nЗдесь ты найдешь все что необходимо: **друзей, общение и голые сиськи** "
                        f"{self.get_emoji('giggle')}\n\nПо всем интересующим тебя вопросам ты можешь обращаться к {discord.utils.get(ctx.guild.roles, name='SHOGUNS').mention} или к пожилому "
                        f"{self.bot.get_user(414105456907386886).mention}\n\nОбщая информация сервера:",
            colour=colour
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
