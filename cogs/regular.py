import discord
import random
import datetime
from itertools import cycle
from discord.ext import commands, tasks

status = cycle(['Work in progress', 'Running on Raspberry pi', 'Request a feature @Danny#3645'])

class Regular(commands.Cog):
    
    def __init__(self, client):
        self.client = client

#above this is always needed
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online)
        self.change_status.start()
        self.terminal_timer.start()
        print('Logged in as ' + self.client.user.name)
    
    #changes status every 60 seconds
    @tasks.loop(seconds=60)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(status)))
        
    @tasks.loop(minutes=60)
    async def terminal_timer(self):
        d = datetime.datetime.now()
        now = d.strftime("%Y-%m-%d %I:%M:%S")
        print(f"Current time is {now}")
    
    #sends to terminal when member enters server
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} joined the server.')
    
    #sends to terminal when member leaves server
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} left the server.')
    
    @commands.command(help="Just a test command")
    async def botTest(self, ctx):
        await ctx.message.delete(delay=5)
        await ctx.send("Hello!", delete_after=5)
        
    @commands.command(aliases=['Ping'], help="Tests bot ping")
    async def ping(self, ctx):
        await ctx.message.delete(delay=5)
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms', delete_after=5)
            
    
#below here is always needed
def setup(client):
    client.add_cog(Regular(client))