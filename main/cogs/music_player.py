import asyncio
import datetime as dt
import random
import re
import typing as t
from enum import Enum
import aiohttp
import discord
import wavelink
from discord.ext import commands
from main.cogs.config import colour
from main.cogs.commands import commands_names as cs
from main.cogs.glossary import speech_setting

"""
don't forget to run `java -jar Lavalink.jar` in jdk/bin
"""

commands_names = cs.music_player
URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
LYRICS_URL = "https://some-random-api.ml/lyrics?title="
HZ_BANDS = (20, 40, 63, 100, 150, 250, 400, 450, 630, 1000, 1600, 2500, 4000, 10000, 16000)
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}


class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NoVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTracks(commands.CommandError):
    pass


class InvalidLoopMode(commands.CommandError):
    pass


class VolumeTooLow(commands.CommandError):
    pass


class VolumeTooHigh(commands.CommandError):
    pass


class MaxVolume(commands.CommandError):
    pass


class MinVolume(commands.CommandError):
    pass


class NoLyricsFound(commands.CommandError):
    pass


class InvalidEQPreset(commands.CommandError):
    pass


class NonExistentEQBand(commands.CommandError):
    pass


class EQGainOutOfBounds(commands.CommandError):
    pass


class InvalidTimeString(commands.CommandError):
    pass


class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None

        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()
        self.eq_levels = [0.] * 15

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel

        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if not tracks:
            raise NoTracksFound

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            embed = discord.Embed(
                title=vocabulary.play.success_title,
                description=f"[{tracks[0].title}]({tracks[0].uri})",
                colour=colour
            )
            embed.set_footer(text=vocabulary.play.invoked_by.format(ctx.author.display_name), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif (track := await self.choose_track(ctx, tracks)) is not None:
            self.queue.add(track)
            embed = discord.Embed(
                title=vocabulary.play.success_title,
                description=f"[{track.title}]({track.uri})",
                colour=colour
            )
            embed.set_footer(text=vocabulary.play.invoked_by.format(ctx.author.display_name), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                    r.emoji in OPTIONS.keys()
                    and u == ctx.author
                    and r.message.id == msg.id
            )

        vocabulary = speech_setting(ctx.guild.id).music_player
        embed = discord.Embed(
            title=vocabulary.play.title,
            description=(
                "\n".join(
                    f"**{i + 1}.** {t.title} ({t.length // 60000}:{str(t.length % 60).zfill(2)})"
                    for i, t in enumerate(tracks[:5])
                )
            ),
            colour=colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name=vocabulary.play.query_results)
        embed.set_footer(text=vocabulary.play.invoked_by.format(ctx.author.display_name), icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f" Wavelink node '{node.identifier}' ready.")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Music commands are not available in DMs.")
            return False

        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host":       "127.0.0.1",
                "port":       2333,
                "rest_uri":   "http://127.0.0.1:2333",
                "password":   "youshallnotpass",
                "identifier": "MAIN",
                "region":     "europe",
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.command(name=commands_names.help)
    async def help(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).music_player
        embed = discord.Embed(
            title=vocabulary.help.title,
            description=vocabulary.help.description,
            colour=colour
        )
        embed.add_field(
            name=vocabulary.help.name,
            value=vocabulary.help.value,
            inline=False
        )
        await ctx.send(embed=embed)

    @commands.command(name=commands_names.join)
    async def join(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        await ctx.send(random.choice(vocabulary.join.success).format(channel.mention))

    @join.error
    async def join_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.send(random.choice(vocabulary.join.already_in_channel))
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send(random.choice(vocabulary.join.no_channel))

    @commands.command(name=commands_names.leave)
    async def leave(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)
        await player.teardown()
        await ctx.send(random.choice(vocabulary.leave.success))

    @commands.command(name=commands_names.play)
    async def play(self, ctx, *, query: t.Optional[str]):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)

        if query is None:
            if player.queue.is_empty:
                raise QueueIsEmpty

            await player.set_pause(False)
            await ctx.send(random.choice(vocabulary.play.playback_resumed))

        else:
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"

            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))

    @play.error
    async def play_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, QueueIsEmpty):
            await ctx.send(random.choice(vocabulary.join.queue_is_empty))
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send(random.choice(vocabulary.join.no_channel))

    @commands.command(name=commands_names.pause)
    async def pause(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)

        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_pause(True)
        await ctx.send(random.choice(vocabulary.pause.success))

    @pause.error
    async def pause_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send(random.choice(vocabulary.pause.already_paused))

    @commands.command(name=commands_names.stop)
    async def stop(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        await ctx.send(random.choice(vocabulary.stop.success))

    @commands.command(name=commands_names.skip)
    async def skip(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)

        if not player.queue.upcoming:
            raise NoMoreTracks

        await player.stop()
        await ctx.send(random.choice(vocabulary.skip.success))

    @skip.error
    async def skip_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, QueueIsEmpty) or isinstance(exc, NoMoreTracks):
            await ctx.send(random.choice(vocabulary.skip.queue_is_empty))

    @commands.command(name=commands_names.previous)
    async def previous(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)

        if not player.queue.history:
            raise NoPreviousTracks

        player.queue.position -= 2
        await player.stop()
        await ctx.send(random.choice(vocabulary.previous.success))

    @previous.error
    async def previous_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, QueueIsEmpty) or isinstance(exc, NoPreviousTracks):
            await ctx.send(vocabulary.previous.queue_is_empty)

    @commands.command(name=commands_names.shuffle)
    async def shuffle(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)
        player.queue.shuffle()
        await ctx.send(random.choice(vocabulary.shuffle.success))

    @shuffle.error
    async def shuffle_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, QueueIsEmpty):
            await ctx.send(random.choice(vocabulary.shuffle.queue_is_empty))

    @commands.command(name=commands_names.loop)
    async def loop(self, ctx, mode: str = "all"):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if mode not in ("none", "1", "all"):
            raise InvalidLoopMode

        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)
        if mode == "none":
            await ctx.send(random.choice(vocabulary.loop.success.none))
        elif mode == "1":
            await ctx.send(random.choice(vocabulary.loop.success.one))
        else:
            await ctx.send(random.choice(vocabulary.loop.success.all))

    @loop.error
    async def loop_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, InvalidLoopMode):
            await ctx.send(random.choice(vocabulary.loop.invalid_loop_mode))

    @commands.command(name=commands_names.queue)
    async def queue(self, ctx, show: t.Optional[int] = 10):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title=vocabulary.queue.embed.title,
            description=vocabulary.queue.embed.description.format(show),
            colour=colour,
        )
        embed.set_footer(text=vocabulary.queue.embed.footer.format(ctx.author.display_name), icon_url=ctx.author.avatar_url)
        embed.add_field(
            name=vocabulary.queue.embed.current_field.name,
            value=getattr(player.queue.current_track, "title", random.choice(vocabulary.queue.embed.current_field.value)),
            inline=False
        )
        if upcoming := player.queue.upcoming:
            embed.add_field(
                name=random.choice(vocabulary.queue.embed.upcoming_field.name),
                value="\n".join(t.title for t in upcoming[:show]),
                inline=False
            )

        await ctx.send(embed=embed)

    @queue.error
    async def queue_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, QueueIsEmpty):
            await ctx.send(vocabulary.queue.queue_is_empty)

    @commands.group(name=commands_names.volume, invoke_without_command=True)
    async def volume(self, ctx, volume: int):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)
        if volume < 0:
            raise VolumeTooLow
        if volume > 150:
            raise VolumeTooHigh
        await player.set_volume(volume)
        await ctx.send(vocabulary.volume.success.format(volume))

    @volume.error
    async def volume_group_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, VolumeTooLow):
            await ctx.send(random.choice(vocabulary.volume.volume_too_low))
        elif isinstance(exc, VolumeTooHigh):
            await ctx.send(random.choice(vocabulary.volume.volume_too_high))

    @volume.command(name=commands_names.volume_up)
    async def volume_up(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)

        if player.volume == 150:
            raise MaxVolume

        await player.set_volume(volume := min(player.volume + 10, 150))
        await ctx.send(vocabulary.volume.success.format(volume))

    @volume_up.error
    async def volume_up_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, MaxVolume):
            await ctx.send(random.choice(vocabulary.volume.max_volume))

    @volume.command(name=commands_names.volume_down)
    async def volume_down(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)

        if player.volume == 0:
            raise MinVolume

        await player.set_volume(volume := max(0, player.volume - 10))
        await ctx.send(vocabulary.volume.success.format(volume))

    @volume_down.error
    async def volume_down_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, MinVolume):
            await ctx.send(random.choice(vocabulary.volume.min_volume))

    @commands.command(name=commands_names.lyrics)
    async def lyrics(self, ctx, name: t.Optional[str]):
        player = self.get_player(ctx)
        name = name or player.queue.current_track.title

        async with ctx.typing():
            async with aiohttp.request("GET", LYRICS_URL + name, headers={}) as r:
                if not 200 <= r.status <= 299:
                    raise NoLyricsFound

                data = await r.json()
                embed = discord.Embed(
                    title=data["title"],
                    url=data["links"]["genius"],
                    description=data["lyrics"].replace("\n\n", "\n"),
                    colour=colour,
                )
                embed.set_thumbnail(url=data["thumbnail"]["genius"])
                embed.set_author(name=data["author"])
                await ctx.send(embed=embed)

    @lyrics.error
    async def lyrics_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, NoLyricsFound):
            await ctx.send(random.choice(vocabulary.lyrics.no_lyrics))

    @commands.command(name=commands_names.equalizer)
    async def equalizer(self, ctx, preset: str):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)

        eq = getattr(wavelink.eqs.Equalizer, preset, None)
        if not eq:
            raise InvalidEQPreset

        await player.set_eq(eq())
        await ctx.send(random.choice(vocabulary.equalizer.success).format(preset))

    @equalizer.error
    async def equalizer_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, InvalidEQPreset):
            await ctx.send(random.choice(vocabulary.equalizer.invalid_preset))

    @commands.command(name=commands_names.advanced_equalizer)
    async def advanced_equalizer(self, ctx, band: int, gain: float):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)

        if not 1 <= band <= 15 and band not in HZ_BANDS:
            raise NonExistentEQBand

        if band > 15:
            band = HZ_BANDS.index(band) + 1

        if abs(gain) > 10:
            raise EQGainOutOfBounds

        player.eq_levels[band - 1] = gain / 10
        eq = wavelink.eqs.Equalizer(levels=[(i, gain) for i, gain in enumerate(player.eq_levels)])
        await player.set_eq(eq)
        await ctx.send(random.choice(vocabulary.advanced_equalizer.success))

    @advanced_equalizer.error
    async def advanced_equalizer_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, NonExistentEQBand):
            await ctx.send(random.choice(vocabulary.advanced_equalizer.no_band).format(", ".join(str(b) for b in HZ_BANDS)))
        elif isinstance(exc, EQGainOutOfBounds):
            await ctx.send(random.choice(vocabulary.advanced_equalizer.out_of_bounds))

    @commands.command(name=commands_names.now_playing)
    async def now_playing(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)
        if not player.is_playing:
            raise PlayerIsAlreadyPaused
        embed = discord.Embed(
            title=vocabulary.now_playing.embed.title,
            colour=colour,
        )
        embed.set_footer(text=vocabulary.now_playing.embed.footer.format(ctx.author.display_name), icon_url=ctx.author.avatar_url)
        embed.add_field(name=vocabulary.now_playing.embed.track_title, value=f"[{player.queue.current_track.title}]({player.queue.current_track.uri})", inline=False)
        embed.add_field(name=vocabulary.now_playing.embed.artist, value=player.queue.current_track.author, inline=False)

        position = divmod(player.position, 60000)
        length = divmod(player.queue.current_track.length, 60000)
        embed.add_field(
            name=vocabulary.now_playing.embed.time_position,
            value=f"{int(position[0])}:{round(position[1] / 1000):02}/{int(length[0])}:{round(length[1] / 1000):02}",
            inline=False
        )
        await ctx.send(embed=embed)

    @now_playing.error
    async def now_playing_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send(random.choice(vocabulary.now_playing.no_track))

    @commands.command(name=commands_names.skip_to_current_index)
    async def skipto(self, ctx, index: int):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        if not 0 <= index <= player.queue.length:
            raise NoMoreTracks

        player.queue.position = index - 2
        await player.stop()
        await ctx.send(random.choice(vocabulary.skipto.success))

    @skipto.error
    async def skipto_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, QueueIsEmpty):
            await ctx.send(random.choice(vocabulary.skipto.queue_is_empty))
        elif isinstance(exc, NoMoreTracks):
            await ctx.send(random.choice(vocabulary.skipto.no_more_tracks))

    @commands.command(name=commands_names.restart)
    async def restart(self, ctx):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        await player.seek(0)
        await ctx.send(random.choice(vocabulary.restart.success))

    @restart.error
    async def restart_error(self, ctx, exc):
        vocabulary = speech_setting(ctx.guild.id).music_player
        if isinstance(exc, QueueIsEmpty):
            await ctx.send(random.choice(vocabulary.restart.queue_is_empty))

    @commands.command(name=commands_names.seek)
    async def seek(self, ctx, position: str):
        vocabulary = speech_setting(ctx.guild.id).music_player
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        if not (match := re.match(TIME_REGEX, position)):
            raise InvalidTimeString

        if match.group(3):
            secs = (int(match.group(1)) * 60) + (int(match.group(3)))
        else:
            secs = int(match.group(1))

        await player.seek(secs * 1000)
        await ctx.send(random.choice(vocabulary.seek.success))
