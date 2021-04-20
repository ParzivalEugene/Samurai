import discord
from discord.ext import commands
from deep_translator import GoogleTranslator, single_detection
from cogs.config import *
from random import choice
import requests
import json


class DeepTranslator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.native_language = "ru"
        self.active_game = False
        self.google_translator_keys = {'af': 'afrikaans',
                                       'am': 'amharic',
                                       'ar': 'arabic',
                                       'az': 'azerbaijani',
                                       'be': 'belarusian',
                                       'bg': 'bulgarian',
                                       'bn': 'bengali',
                                       'bs': 'bosnian',
                                       'ca': 'catalan',
                                       'ceb': 'cebuano',
                                       'co': 'corsican',
                                       'cs': 'czech',
                                       'cy': 'welsh',
                                       'da': 'danish',
                                       'de': 'german',
                                       'el': 'greek',
                                       'en': 'english',
                                       'eo': 'esperanto',
                                       'es': 'spanish',
                                       'et': 'estonian',
                                       'eu': 'basque',
                                       'fa': 'persian',
                                       'fi': 'finnish',
                                       'fil': 'Filipino',
                                       'fr': 'french',
                                       'fy': 'frisian',
                                       'ga': 'irish',
                                       'gd': 'scots gaelic',
                                       'gl': 'galician',
                                       'gu': 'gujarati',
                                       'ha': 'hausa',
                                       'haw': 'hawaiian',
                                       'he': 'Hebrew',
                                       'hi': 'hindi',
                                       'hmn': 'hmong',
                                       'hr': 'croatian',
                                       'ht': 'haitian creole',
                                       'hu': 'hungarian',
                                       'hy': 'armenian',
                                       'id': 'indonesian',
                                       'ig': 'igbo',
                                       'is': 'icelandic',
                                       'it': 'italian',
                                       'iw': 'hebrew',
                                       'ja': 'japanese',
                                       'jw': 'javanese',
                                       'ka': 'georgian',
                                       'kk': 'kazakh',
                                       'km': 'khmer',
                                       'kn': 'kannada',
                                       'ko': 'korean',
                                       'ku': 'kurdish (kurmanji)',
                                       'ky': 'kyrgyz',
                                       'la': 'latin',
                                       'lb': 'luxembourgish',
                                       'lo': 'lao',
                                       'lt': 'lithuanian',
                                       'lv': 'latvian',
                                       'mg': 'malagasy',
                                       'mi': 'maori',
                                       'mk': 'macedonian',
                                       'ml': 'malayalam',
                                       'mn': 'mongolian',
                                       'mr': 'marathi',
                                       'ms': 'malay',
                                       'mt': 'maltese',
                                       'my': 'myanmar (burmese)',
                                       'ne': 'nepali',
                                       'nl': 'dutch',
                                       'no': 'norwegian',
                                       'ny': 'chichewa',
                                       'pa': 'punjabi',
                                       'pl': 'polish',
                                       'ps': 'pashto',
                                       'pt': 'portuguese',
                                       'ro': 'romanian',
                                       'ru': 'russian',
                                       'sd': 'sindhi',
                                       'si': 'sinhala',
                                       'sk': 'slovak',
                                       'sl': 'slovenian',
                                       'sm': 'samoan',
                                       'sn': 'shona',
                                       'so': 'somali',
                                       'sq': 'albanian',
                                       'sr': 'serbian',
                                       'st': 'sesotho',
                                       'su': 'sundanese',
                                       'sv': 'swedish',
                                       'sw': 'swahili',
                                       'ta': 'tamil',
                                       'te': 'telugu',
                                       'tg': 'tajik',
                                       'th': 'thai',
                                       'tl': 'filipino',
                                       'tr': 'turkish',
                                       'uk': 'ukrainian',
                                       'ur': 'urdu',
                                       'uz': 'uzbek',
                                       'vi': 'vietnamese',
                                       'xh': 'xhosa',
                                       'yi': 'yiddish',
                                       'yo': 'yoruba',
                                       'zh-cn': 'chinese (simplified)',
                                       'zh-tw': 'chinese (traditional)',
                                       'zu': 'zulu'}

    @commands.command(name="translate")
    async def translate(self, ctx, *words):
        """"""
        async with ctx.typing():
            if not words:
                return await ctx.send(choice([
                    "Молодой я не умею переводить пустоту", "Блять тебе нихуя перевести?", "Переводить то чо ебана", "Ты нихуя не написал, чо мне переводить"
                ]))
            if len(words) == 1 and words[0] in self.google_translator_keys.keys():
                return await ctx.send(choice([
                    "Бля ты умница конечно указал на какой язык переводить, но переводить то нехуй ебана", "Заебца, я понял куда переводить, только переводить нехуй",
                    "Блять заебца я на волну этого языка настроился и перевел тишину, обращайся сука"
                ]))
            if len(words) == 1:
                return await ctx.send(choice([
                    "Ахуенное слово, жалко не ебу на какой язык переводить", "Бля слово топ, только куда сука переводить", "Сука на какой язык то переводить твое слово ебучее"
                ]))
            if len(words) == 2 and all(i in self.google_translator_keys for i in words):
                return await ctx.send(choice([
                    "Вау ебать ты даже указал куда и откуда, но что переводить то ебана", "Братик я не телепат, что переводить то",
                    "Еба, я тебя конечно уважаю, что указал куда и откуда, но что блять переводить"
                ]))
            if len(words) >= 2 and not any(i in self.google_translator_keys for i in words):
                return await ctx.send(choice([
                    "Просто ахуенное сообщение, еще бы ебать с какого и на какой язык его переводить", "Ого похуй! Укажи с какого на какой язык переводить",
                    "Молодой ебана чо мне с этим сообщением делать, с какого на какой язык его переводить", "Внучок блять языки то какие ебана"
                ]))

        if words[0] in self.google_translator_keys and words[1] in self.google_translator_keys:
            source, target = words[:2]
        else:
            source, target = "auto", words[0]
        message = " ".join(filter(lambda x: x not in self.google_translator_keys, words))

        if target == source:
            translated_message = message
        else:
            print(source, "-->", target)
            translator = GoogleTranslator(source=source, target=target)
            translated_message = translator.translate(message)

        embed = discord.Embed(
            title=":loudspeaker: Перевод :loudspeaker:",
            description=translated_message,
            colour=discord.Colour.purple()
        )
        embed.set_footer(text=f"оригинал: {message}")
        async with ctx.typing():
            await ctx.send(embed=embed)

    @commands.command(name="get_lang")
    async def detect_language(self, ctx, *message):
        language = single_detection(" ".join(message), api_key=api_key_for_single_detection)
        embed = discord.Embed(
            title=":notebook_with_decorative_cover: Язык :ledger:",
            description=self.google_translator_keys[language],
            colour=discord.Colour.purple()
        )
        async with ctx.typing():
            await ctx.send(embed=embed)

    @commands.command(name="lang_list")
    async def language_list(self, ctx):
        embed = discord.Embed(
            title=":a: Список кратких обозначений языков :b:",
            description="\n".join([f"{i} - {j}" for i, j in self.google_translator_keys.items()]),
            colour=discord.Colour.purple()
        )
        await ctx.send(embed=embed)

    @commands.command(name="what_the_lang")
    async def what_the_language_game(self, ctx):
        def check(text):
            return text.author != self.bot.user and not text.content.startswith(".")

        if self.active_game:
            return await ctx.send(choice([
                "Пожилой ты еще предыдущий язык не угадал", "Не торопись молодеж, ты старый еще не угадал", "Старую игру доиграй, а потом стартуй новую", "Старичок закончу старую игру сначалу"
            ]))

        language = choice(list(self.google_translator_keys.keys()))

        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q']

        self.active_game = True
        embed = discord.Embed(
            title=":question: Какой язык :question:",
            description=GoogleTranslator(source="en", target=language).translate(quote),
            colour=discord.Colour.purple()
        )
        await ctx.send(embed=embed)
        msg = await self.bot.wait_for("message", check=check, timeout=30)
        self.active_game = False
        print(msg.content)
        if msg.content == language:
            return await ctx.send([
                "Молодец боевой угадал", "Уважаю внучок, правильно ответил", "Абсолютно верно молодеж", "Порадовали деда, правильно сказали"
            ])
        await ctx.send(choice([
            "Бля расстроили деда, не угадал. ", "Сука неверно ебана, грустно мне( ", "Обижают старичка, неверно нихуя. "
        ]) + f"Верный ответ: {language} - {self.google_translator_keys[language]}")

    @what_the_language_game.error
    async def what_the_language_game_error(self, ctx, error):
        if isinstance(error, TimeoutError):
            ctx.send(choice([
                "Проиграл молодой, время вышло", "Габела, время истекло", "Пососал внучок, время вышло"
            ]))
