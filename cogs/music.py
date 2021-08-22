import discord
from discord.ext import commands
import youtube_dl

class Music(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def connect(self, ctx):
        await ctx.message.delete(delay=10)
        if ctx.author.voice is None:
            await ctx.send("Please join a Voice channel.", delete_after=10)
        vChannel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await vChannel.connect()
        else:
            await ctx.voice_client.move_to(vChannel)
    
    @commands.command()
    async def disconnect(self, ctx):
        await ctx.message.delete(delay=10)
        await ctx.voice_client.disconnect()
            
    @commands.command()
    async def pause(self, ctx):
        await ctx.message.delete(delay=10)
        await ctx.voice_client.pause()
        await ctx.send("Paused", delete_after=10)
    
    @commands.command()
    async def resume(self, ctx):
        await ctx.message.delete(delay=10)
        await ctx.voice_client.resume()
        await ctx.send("Resumed", delete_after=10)
        
    @commands.command()
    async def play(self, ctx, url):
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format':"bestaudio"}
        vc = ctx.voice_client
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)
    
    


def setup(client):
    client.add_cog(Music(client))