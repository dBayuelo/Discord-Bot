import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #Error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        message = ""
        if isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing arguments: {error.param}. Check ]help"
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            message = "Insufficient permissions."
        elif isinstance(error, commands.CommandOnCooldown):
            message = "Command still on cooldown."
        elif isinstance(error, commands.UserInputError):
            message = "Check your input, something went wrong."
        else:
            message = "Error."
            
        await ctx.message.delete(delay=10)
        await ctx.send(message, delete_after=10)

def setup(client):
    client.add_cog(ErrorHandler(client))