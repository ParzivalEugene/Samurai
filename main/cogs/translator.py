import json
from random import choice

import discord
import requests
from deep_translator import GoogleTranslator, single_detection
from discord.ext import commands

from cogs.commands import commands_names as cs
from cogs.config import *
from cogs.database_connector import Database
from cogs.glossary import speech_setting

commands_names = cs.translator


class DeepTranslator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.google_translator_keys = {'af':  'afrikaans',
                                       'am':  'amharic',
                                       'ar':  'arabic',
                                       'az':  'azerbaijani',
                                       'be':  'belarusian',
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

    @commands.command(name=commands_names.help)
    async def translator_help(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).translator
        embed = discord.Embed(
            title=vocabulary.help.title,
            description=vocabulary.help.description,
            colour=discord.Colour.purple()
        )
        embed.add_field(
            name=vocabulary.help.name,
            value=vocabulary.help.value
        )
        await ctx.send(embed=embed)

    @commands.command(name=commands_names.translate)
    async def translate(self, ctx, *words):
        vocabulary = speech_setting(ctx.guild.id).translator
        if not words:
            return await ctx.send(choice([vocabulary.translate.no_words]))
        if len(words) == 1 and words[0] in self.google_translator_keys.keys():
            return await ctx.send(choice([vocabulary.translate.no_words_plus_languages]))
        if len(words) == 1:
            return await ctx.send(choice([vocabulary.translate.word_without_language]))
        if len(words) == 2 and all(i in self.google_translator_keys for i in words):
            return await ctx.send(choice([vocabulary.translate.only_languages]))
        if len(words) >= 2 and not any(i in self.google_translator_keys for i in words):
            return await ctx.send(choice([vocabulary.translate.no_languages]))
        if words[0] in self.google_translator_keys and words[1] in self.google_translator_keys:
            source, target = words[:2]
        else:
            source, target = "auto", words[0]
        message = " ".join(filter(lambda x: x not in self.google_translator_keys, words))

        if target == source:
            translated_message = message
        else:
            translator = GoogleTranslator(source=source, target=target)
            translated_message = translator.translate(message)

        embed = discord.Embed(
            title=vocabulary.translate.title,
            description=translated_message,
            colour=discord.Colour.purple()
        )
        embed.set_footer(text=vocabulary.translate.footer.format(message))
        async with ctx.typing():
            await ctx.send(embed=embed)

    @commands.command(name=commands_names.detect_language)
    async def detect_language(self, ctx, *message):
        vocabulary = speech_setting(ctx.guild.id).translator
        language = single_detection(" ".join(message), api_key=api_key_for_single_detection)
        embed = discord.Embed(
            title=vocabulary.translate.detect_language.title,
            description=self.google_translator_keys[language],
            colour=discord.Colour.purple()
        )
        async with ctx.typing():
            await ctx.send(embed=embed)

    @commands.command(name=commands_names.languages_list)
    async def language_list(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).translator
        embed = discord.Embed(
            title=vocabulary.language_list.title,
            description="\n".join([f"{i} - {j}" for i, j in self.google_translator_keys.items()]),
            colour=discord.Colour.purple()
        )
        await ctx.send(embed=embed)

    @commands.command(name=commands_names.game_detect_languages)
    async def what_the_language_game(self, ctx):
        def check(text):
            return text.author != self.bot.user and not text.content.startswith(".")

        vocabulary = speech_setting(ctx.guild.id).translator
        with Database() as db:
            server_id = db.execute('SELECT id FROM "default".servers WHERE discord_server_id = %s', [ctx.guild.id]).fetchone()[0]
            language = db.execute('SELECT language FROM "default".detect_language_game WHERE server_id = %s', [server_id]).fetchone()[0]
            if language != "no_lang":
                return await ctx.send(choice(vocabulary.what_the_language_game.active_game))

            language = choice(list(self.google_translator_keys.keys()))
            counter = 3
            response = requests.get("https://zenquotes.io/api/random")
            json_data = json.loads(response.text)
            quote = json_data[0]['q']

            db.execute('UPDATE "default".detect_language_game SET language = %s WHERE server_id = %s', [language, server_id])
            embed = discord.Embed(
                title=vocabulary.what_the_language_game.title,
                description=GoogleTranslator(source="en", target=language).translate(quote),
                colour=discord.Colour.purple()
            )
            await ctx.send(embed=embed)
            while counter:
                print(language)
                counter -= 1
                msg = await self.bot.wait_for("message", check=check, timeout=30)
                if msg.content == db.execute('SELECT language FROM "default".detect_language_game WHERE server_id = %s', [server_id]).fetchone()[0]:
                    db.execute('UPDATE "default".detect_language_game SET language = %s WHERE server_id = %s', ["no_lang", server_id])
                    return await ctx.send(choice(vocabulary.what_the_language_game.win))
                if counter:
                    await ctx.send(vocabulary.what_the_language_game.tries.format(counter))
            await ctx.send(choice(vocabulary.what_the_language_game.lose_start) + vocabulary.what_the_language_game.lose_end.format(language, self.google_translator_keys[language]))
            db.execute('UPDATE "default".detect_language_game SET language = %s WHERE server_id = %s', ["no_lang", server_id])

    @what_the_language_game.error
    async def what_the_language_game_error(self, ctx, error):
        vocabulary = speech_setting(ctx.guild.id).translator
        if isinstance(error, TimeoutError):
            ctx.send(choice([vocabulary.what_the_language_game_error.TimeoutError]))
