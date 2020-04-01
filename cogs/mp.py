import discord
import asyncio
import subprocess
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
import os


class VoiceError(Exception):
    pass


class Music_Player(commands.Cog):

    def __init__(self, client):

        self.client = client
        self.source = None
        self.vc = None
        self.vc_text_channel_name = None
        self.player = None
        self.now_playing = None
        self.loop = False
        self.queue = []
        self.next = asyncio.Event()
        self.playing = False
        self.do = True
        self.emojis = ['\u23f9\ufe0f', '\u23f8\ufe0f', '\u25b6\ufe0f', '\u23e9', '\U0001f501', '\U0001f5d2\ufe0f']

    def download_song(self, song):
        search = "ytsearch:" + song
        subprocess.run(['youtube-dl', '-x', '--audio-format', 'mp3', search])  # downloads the song
        queue_dir = "./cogs/queue/"
        files = os.listdir()
        for file in files:
            if file.endswith('.mp3'):
                subprocess.run(['mv', file, queue_dir])
                self.queue.append("./cogs/queue/" + str(file))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, member):

        """
        Acts on reaction added
        :param reaction:
        :param member:
        :return:
        """

        if self.vc is None:
            return

        if not self.do:
            return

        g = ['\u2049\ufe0f', '\U0001f92c']
        channel = reaction.message.channel
        print(ascii(str(reaction.emoji)))
        if str(reaction.emoji) not in g and str(reaction.emoji) not in self.emojis:
            await reaction.message.add_reaction('\u2049\ufe0f')

        if str(reaction.emoji) == '\u23f9\ufe0f':
            await reaction.message.add_reaction('\U0001f92c')
            await self._disconnect(channel)

        if channel == self.vc_text_channel_name and self.playing:


            emoji_name = str(reaction.emoji)
            print(ascii(str(reaction.emoji)))
            if emoji_name == '\u23f8\ufe0f':
                await self._pause(channel)
            if emoji_name == '\u25b6\ufe0f':
                await self._resume(channel)
            if emoji_name == '\u23e9':
                await self._skip(channel)
            if emoji_name == '\U0001f5d2\ufe0f':
                await self._queue(channel)
            if emoji_name == '\U0001f501':
                await self._loop(channel)

    @commands.command(name='connect', aliases=['join'])
    async def _connect(self, ctx):
        """
        Connects or moves bot to the channel
        :param ctx:
        :return:
        """
        subprocess.run(['rm', '-rf', "./cogs/queue/"])
        subprocess.run(['mkdir', "./cogs/queue/"])

        self.vc_text_channel_name = ctx.message.channel

        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("```You are not connected to a voice channe```l")
            return
        self.vc = get(self.client.voice_clients, guild=ctx.guild)
        if self.vc and self.vc.is_connected():
            await self.vc.move_to(channel)
        self.vc = await channel.connect()
        await ctx.send("Ready to play!")

    @commands.command(name='disconnect', aliases=['dc', 'leave', 'exit'])
    async def _disconnect(self, ctx):
        """
        Disconnects bot from the channel
        :param ctx:
        :return:
        """

        if self.vc.is_connected():
            await self.vc.disconnect()
            self.vc = None
            return
        await ctx.send("```Bot is not connected to voice channel```")

    @commands.command(name='play', aliases=['p'])
    async def _p(self, ctx, *, url):
        """
        Plays song or adds it to queue (to add to queue you have to wait till start of playing)
        :param ctx:
        :param url:
        :return:
        """
        if self.vc is None:
            await self._connect(ctx)

        self.playing = True;
        self.download_song(str(url))
        await self._play(ctx)

    async def _play(self, ctx):

        if not self.vc.is_playing() and self.queue:
            temp = 0
            song_short = ""
            for i in range(len(self.queue[0])):
                if self.queue[0][i] == '-':
                    temp += 1
                if temp == 2:
                    break
                song_short += self.queue[0][i]

            self.do = False

            await ctx.send(f"```Now playing {song_short[13:]}```")
            await asyncio.sleep(1.40)
            for emoji in self.emojis:
                await ctx.channel.last_message.add_reaction(emoji)
            await asyncio.sleep(1.20)

            self.do = True

            if not self.loop:
                if self.queue:
                    self.source = FFmpegPCMAudio(self.queue.pop(0))

            if self.loop:
                if self.queue:
                    self.source = FFmpegPCMAudio(self.queue[0])

            self.vc.play(self.source, after=self.next_song)

    def next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        if self.queue:
            self.vc.play(FFmpegPCMAudio(self.queue.pop(0)), after=self.next_song)

    @commands.command(name='skip', aliases=['s', 'next'])
    async def _skip(self, ctx):

        """
        Plays next song from queue
        :param ctx:
        :return:
        """
        self.vc.stop()
        if self.queue:
            await ctx.send("```Skipped!```")
            await self._play(ctx)
        else:
            self.playing = False
            await ctx.send("```Queue is empty!```")

    @commands.command(name='pause')
    async def _pause(self, ctx):

        """
        Pause, if playing
        :param ctx:
        :return:
        """

        if not self.vc.is_playing():
            await ctx.send("```Bot is not currently playing```")
            return
        self.vc.pause()

    @commands.command(name='resume')
    async def _resume(self, ctx):

        """
        Resume play, if not playing
        :param ctx:
        :return:
        """

        if self.vc.is_paused():
            self.vc.resume()
            return
        await ctx.send("```Bot is not currently paused```")

    @commands.command(name='queue', aliases=['list'])
    async def _queue(self, ctx):

        """
        Shows queue
        :param ctx:
        :return:
        """

        if not self.queue:
            await ctx.send(f'```Queue is empty```')
        temp = 0
        temp2 = 1
        final = ""
        for song in self.queue:
            song_short = ""
            for i in range(len(song)):
                if song[i] == '-':
                    temp += 1
                if temp == 2:
                    break
                song_short += song[i]
            temp = 0
            output = song_short + "\n"
            final += str(temp2) + ". " + output[13:]
            temp2 += 1

        await ctx.send(f'```Queue: \n{final}```')

    @commands.command(name='loop')
    async def _loop(self, ctx):
        """
        Loops current playing song
        :param ctx:
        :return:
        """
        if self.loop:
            await ctx.send("```Unlooped!```")
            if self.queue:
                self.queue.pop(0)
            self.loop = False
            return
        else:
            await ctx.send("```Looped!```")
            self.loop = True


def setup(client):
    client.add_cog(Music_Player(client))
