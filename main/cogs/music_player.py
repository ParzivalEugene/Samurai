import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
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

    @commands.command(name="join")
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

    @commands.command(name="leave")
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

    @commands.command(name="queue")
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

    @commands.command(name="remove")
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

    @commands.command(name="play")
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

    @commands.command(name="pause")
    async def pause(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.pause()
        await ctx.message.add_reaction("⏸")

    @commands.command(name="resume")
    async def resume(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.resume()
        await ctx.message.add_reaction("▶️")

    @commands.command(name="stop")
    async def stop(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.stop()
        await ctx.message.add_reaction("⏹")

    @commands.command(name="player_help")
    async def player_help(self, ctx):
        pass
