import discord
import requests
from discord.ext import commands, tasks

class Weather(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    #Weather using openweathermap API
    
    @commands.command(aliases=['Weather'], help="Find the weather based on city")
    async def weather(self, ctx, *, location: str):
        await ctx.message.delete(delay=10)
        city = location.capitalize()
        #link + key + location
        this_url = "http://api.openweathermap.org/data/2.5/weather?appid=" + "aaf78cda84f74532d900942b29bc44a0" + "&q=" + city
        reply = requests.get(this_url)
        json = reply.json()
        channel = ctx.message.channel
        if json["cod"] != "404":
            async with channel.typing():
                #Gathering weather info from json
                country = json["sys"]["country"]
                weather = json["main"]
                temp = str(round((9/5)*(weather["temp"]-273.15)+32))
                celsius = str(round(weather["temp"]-273.15))
                humidity = weather["humidity"]
                description = json["weather"][0]["description"]
                icon = json["weather"][0]["icon"]
                icon_url = "http://openweathermap.org/img/w/" + icon + ".png"
                #Adding info into embed message
                embed = discord.Embed(title=f"Weather in {city}, {country}",
                                      color=0xd192ce,
                                      timestamp=ctx.message.created_at)
                embed.add_field(name="Description", value = f"**{description}**", inline=False)
                embed.add_field(name="Temperature (F°)", value = f"**{temp}**", inline=False)
                embed.add_field(name="Temperature (C°)", value = f"**{celsius}**", inline=False)
                embed.add_field(name="Humidity", value = f"**{humidity}%**", inline=False)
                embed.set_thumbnail(url=icon_url)
                embed.set_footer(text=f"Prompted by {ctx.author.name}")
                await channel.send(embed=embed, delete_after=30)
        else: #code returns 404
            await channel.send("Error! City not found.", delete_after=10)
            
def setup(client):
    client.add_cog(Weather(client))