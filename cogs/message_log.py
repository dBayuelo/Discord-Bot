import discord
import random
from discord.ext import commands, tasks

class Msg_Log(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        user = msg.author
        content = msg.content
        if (msg.author.id == 873658394790227998) or (content[0] == "]"):
            return
        msg_ID = msg.id 
        msg_channel = msg.channel
        guild = msg.guild
        #specifying channel for specific servers
        if guild.id == 832869333390589972: #lin's server
            channel = discord.utils.get(guild.channels, id=865056632811290684)
        elif guild.id == 242712607889293322: #my server
            channel = discord.utils.get(guild.channels, id=875827704375701525)
        else: #other server
            channel = discord.utils.get(guild.channels, name="logs")
        
        #sending the deleted message info
        embed = discord.Embed(title=f"Message sent by {user} deleted in #{msg_channel}", description=content, color=0xFF0000)
        embed.add_field(name=f"user ID: {msg.author.id}", value=f"message ID: {msg_ID}", inline=True)
        await channel.send(embed=embed)
        
def setup(client):
 client.add_cog(Msg_Log(client))