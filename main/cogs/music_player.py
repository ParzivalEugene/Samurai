import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
from cogs.config import *
from cogs.commands import commands_names
import youtube_dl
import random
import asyncio
import pafy

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        super().__init__(source, volume)

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @commands.command(name=commands_names["music player"]["help"])
    async def player_help(self, ctx):
        embed = discord.Embed(
            title="Player help",
            description=":track_previous: :stop_button: :play_pause:",
            colour=discord.Colour.purple()
        )
        embed.add_field(name="Команды",
                        value=f"""Этот модуль был создан, чтобы ты мог чилить со своими друзьями в голосовом канале и параллельно слушать любимый музон
**{prefix}{commands_names["music player"]["help"]}** - отдельный эмбед для вывода помощи по плэеру
**{prefix}{commands_names["music player"]["join"]}** - зайду в голосовой канала, в котором находится автор сообщения.
**{prefix}{commands_names["music player"]["leave"]}** - уйду из голосового канала
**{prefix}{commands_names["music player"]["queue"]}** - выведу очередь треков
**{prefix}{commands_names["music player"]["queue"]} <url>** - добавлю в очередь трек
**{prefix}{commands_names["music player"]["remove"]} <number>** - удалю трек под номером <number>
**{prefix}{commands_names["music player"]["play"]}** - начну играть музыку из очереди
**{prefix}{commands_names["music player"]["pause"]}** - поставлю на паузу шарманку
**{prefix}{commands_names["music player"]["resume"]}** - воспроизведу воспроизведение
**{prefix}{commands_names["music player"]["stop"]}** - уберу трек из очереди и остановлю проигрывание""",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(name=commands_names["music player"]["join"])
    async def join(self, ctx):
        if not ctx.message.author.voice:
            return await ctx.send(random.choice(
                ["дядя ты не в голосовом канале", "заходить некуда пожилой, ты не в голосовом канале", "я не смогу зайти, пока ты не в голосовом канале", "блять куда идти то"]
            ))
        else:
            channel = ctx.message.author.voice.channel
        await ctx.send(random.choice(
            ["залетаю пожилой", "уже еду", "скоро буду", "обосраться уже лечу"]
        ))
        await channel.connect()

    @commands.command(name=commands_names["music player"]["leave"])
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if not voice_client:
            await ctx.send(random.choice(
                ["ахуеть уже из ниоткуда прогоняют", "старичка не любят настолько, что из пустоты кикают", "мать свою покикай, и так один сижу", "обижают пожилого"]
            ))
            return
        await ctx.send(random.choice(
            ["прогнали старого", "туда меня", "обижают старичка", "ну и не надо"]
        ))
        await voice_client.disconnect()

    @commands.command(name=commands_names["music player"]["queue"])
    async def queue(self, ctx, url):
        video_title = pafy.new(url).title
        self.queue.append([url, "".join(video_title)])
        embed = discord.Embed(
            title="Добавил композицию в очередь",
            description=f"[{''.join(video_title)}]({url}) - {ctx.author.mention}",
            colour=discord.Colour.purple()
        )
        await ctx.send(embed=embed)

    @queue.error
    async def queue_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if not self.queue:
                await ctx.send("В очереди пусто братик")
                return
            embed = discord.Embed(
                title="Текущая очередь",
                description="\n".join([f"{i + 1} - [{self.queue[i][1]}]({self.queue[i][0]})" for i in range(len(self.queue))]),
                colour=discord.Colour.purple()
            )
            await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            await ctx.send("Хуевый аргумент я сломался")

    @commands.command(name=commands_names["music player"]["remove"])
    async def remove(self, ctx, number):
        if not len(self.queue):
            await ctx.send("пустая очередь, нихуя я не удалю")
            return
        elif int(number) > len(self.queue) or 0 < int(number):
            await ctx.send("неверный номер")
            return
        del(self.queue[int(number)])
        await ctx.send(f"удалил всякую хуйню.")

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("ты не указал номер элемента братка")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Хуевый аргумент я сломался")

    @commands.command(name=commands_names["music player"]["play"])
    async def play(self, ctx):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if not (voice_client and voice_client.is_connected()):
            await self.join(ctx)
        if not len(self.queue):
            await ctx.send("пожилой очередь пустая, шарманку не заведу")
            return
        await ctx.message.add_reaction("▶️")
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            player = await YTDLSource.from_url(self.queue[0][0], loop=self.bot.loop)
            voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        embed = discord.Embed(
            title="Сейчас проигрывается",
            description=f"[{self.queue[0][1]}]({self.queue[0][0]}) - {ctx.author.mention}",
            colour=discord.Colour.purple()
        )
        await ctx.send(embed=embed)
        del self.queue[0]

    @commands.command(name=commands_names["music player"]["pause"])
    async def pause(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.pause()
        await ctx.message.add_reaction("⏸")

    @commands.command(name=commands_names["music player"]["resume"])
    async def resume(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.resume()
        await ctx.message.add_reaction("▶️")

    @commands.command(name=commands_names["music player"]["stop"])
    async def stop(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.stop()
        await ctx.message.add_reaction("⏹")
