import discord
import random
import os
from discord.ext import commands

TOKEN = '~~~'

description = '''Overseer Bot'''
client = commands.Bot(command_prefix=']', description=description)

    
@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    await ctx.message.delete()
    client.load_extension(f'cogs.{extension}')
    print(f'Loaded extension: {extension}')
    
@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    await ctx.message.delete()
    client.unload_extension(f'cogs.{extension}')
    print(f'Unloaded extension: {extension}')
        
@client.command()
async def reload(ctx, extension):
    await ctx.message.delete()
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    print(f'Reloaded extension: {extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}') 
    
def is_it_me(ctx):
    return ctx.author.id == 94555965663219712

@client.command()
@commands.check(is_it_me)
async def shutdown(ctx):
    exit()

client.run(TOKEN)