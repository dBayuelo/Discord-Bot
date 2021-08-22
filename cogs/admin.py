import discord
import random
from discord.ext import commands, tasks

class Admin(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    #commands
    @commands.command(aliases=['Kick'], help="Kicks member")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}')
    
    @commands.command(aliases=['Ban'], help="Bans member")
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')
    
    @commands.command(aliases=['Unban'], help="Unbans member")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.name}.')
                return
    
    @commands.command(help="Clears specified messages. Defaults to 5")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"{amount} messages deleted by {ctx.author.mention}", delete_after=30)
        
    #Censorship test
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id == self.client.user.id:
            return
        content = msg.content.lower()
        
        blacklist = ["goober", "jimbob"]
        if any(word in content for word in blacklist):
            await msg.delete()
            channel = msg.channel
            await channel.send(f":rage: {msg.author} watch your language! :angry:")

    
def setup(client):
    client.add_cog(Admin(client))
