import discord
import random
from discord.ext import commands, tasks

class Games(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    #commands
        
    #8ball
    @commands.command(aliases=['8ball'], help="Ask 8ball a question, receive an answer. Can use ']8ball' to trigger")
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain',
                 'Without a doubt',
                 'You may rely on it',
                 'Yes definitely',
                 'It is decidedly so',
                 'As I see it, yes',
                 'Most likely',
                 'Yes',
                 'Outlook good',
                 'Signs point to yes',
                 'Reply hazy try again',
                 'Better not tell you now',
                 'Ask again later',
                 'Cannot predict now',
                 'Concentrate and ask again',
                 'Don’t count on it',
                 'Outlook not so good',
                 'My sources say no',
                 'Very doubtful',
                 'My reply is no']
        await ctx.message.delete(delay=5)
        await ctx.send(f'{ctx.author.mention} asked: "{question}" \n{random.choice(responses)}', delete_after=15)
        
def setup(client):
    client.add_cog(Games(client))