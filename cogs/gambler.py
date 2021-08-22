import discord
import mysql.connector as mariadb
import random
from discord.ext import commands, tasks

db_connection = mariadb.connect(user='ForDiscord', database = 'Discord', password='~~~', host='localhost', port='3306')
cursor = db_connection.cursor()

emojis = {'\U0001F311':10000, '\U0001F312': 1000, '\U0001F318': 1000, '\U0001F313': 250, '\U0001F317': 250, '\U0001F314': 50, '\U0001F316': 50, '\U0001F315':1}
index = [0, 1, 2, 3, 4, 5, 6, 7]

#checks if user is in database table
def userExists(ID):
    sql_statement = f"SELECT user_id from UserInfo WHERE user_id = '{ID}'"
    cursor.execute(sql_statement)
    results = cursor.fetchone()
    if results is None:
        return False
    elif (str(ID) == str(results[0])):
        return True
    
#add points to the csv file of the user in case of bot crash
def modUserPoints(ID, points):
    sql_statement = f"SELECT user_points from UserInfo WHERE user_id = '{ID}'"
    cursor.execute(sql_statement)
    results = cursor.fetchone()
    user_points = results[0]
    newPoints = int(user_points) + points
    items = (str(newPoints), str(ID))
    sql_statement = 'UPDATE UserInfo SET user_points=%s WHERE USER_ID = %s';
    cursor.execute(sql_statement, items)
    db_connection.commit();

#add new line to the csv file with user info in case of bot crash
def addUser(ID, points):
    items = (str(ID), str(points))
    sql_statement = 'INSERT INTO UserInfo (user_id, user_points) VALUES (%s, %s)';
    cursor.execute(sql_statement, items)
    db_connection.commit();

#returns points user currently has
def userPoints(ID):
    sql_statement = f"SELECT user_points from UserInfo WHERE user_id = '{ID}'"
    cursor.execute(sql_statement)
    results = cursor.fetchone()
    return results[0]

# Returns result of coinflip, Low in case the user bet more than they have
def coinFlip(ID, points):
    sql_statement = f"SELECT user_points from UserInfo WHERE user_id = '{ID}'"
    cursor.execute(sql_statement)
    results = cursor.fetchone()
    user_points = results[0]
    if int(user_points) < points:
        return "Low"
    if random.choice([True,False]):
        return "Won"
    else:
        return "Lost"
    
#edits user's points in database based on win/loss
def coinFlipResult(ID, points, coinF):
    if coinF == "Won":
        sql_statement = f"SELECT user_points from UserInfo WHERE user_id = '{ID}'"
        cursor.execute(sql_statement)
        results = cursor.fetchone()
        user_points = results[0]
        newPoints = int(user_points) + points
        items = (str(newPoints), str(ID))
        sql_statement = 'UPDATE UserInfo SET user_points=%s WHERE USER_ID = %s';
        cursor.execute(sql_statement, items)
        db_connection.commit();
        return userPoints(ID)
    else:
        sql_statement = f"SELECT user_points from UserInfo WHERE user_id = '{ID}'"
        cursor.execute(sql_statement)
        results = cursor.fetchone()
        user_points = results[0]
        newPoints = int(user_points) - points
        items = (str(newPoints), str(ID))
        sql_statement = 'UPDATE UserInfo SET user_points=%s WHERE USER_ID = %s';
        cursor.execute(sql_statement, items)
        db_connection.commit();
        return userPoints(ID)
    
class Gambler(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.pointDrop.start()
    
    #Periodically drops a moon in chat for X seconds for points
    @tasks.loop(seconds=360)
    async def pointDrop(self):
        channel = self.client.get_channel(873664939762520064)
        msg = await channel.send("Who's gonna reach the moon first?!", delete_after=3)
        choice = random.choices(index, weights=(1, 5, 5, 25, 25, 100, 100, 1000), k=1)
        idx = choice[0]
        i = 0
        for x in emojis:
            if i == idx:
                await msg.add_reaction(x)
            i += 1
    
    #Monitors for a user catching a moon
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        emoji = reaction.emoji
        if user.id == 873658394790227998:
            return
        if emoji in emojis.keys():
            channel = self.client.get_channel(873664939762520064)
            caughtMsg = await channel.send(f"Caught! You gained {emojis[emoji]} point(s)!", delete_after=20)
            #modifies users points in dictionary
            userExisted = userExists(user.id)
            #checks if user exists from return value of userManager
            if userExisted:
                modUserPoints(user.id, emojis[emoji])
            else:
                addUser(user.id, emojis[emoji])
    
    #Defaults to the user that sent the message
    @commands.command(help="Returns points of user with the bot")
    async def points(self, ctx, member : discord.Member=None):        
        if member is not None:
            user_points = userPoints(member.id)
            channel = ctx.message.channel
            await channel.send(f"{member.name} has a total of {user_points} point(s)!")
        else:
            user_points = userPoints(ctx.message.author.id)
            channel = ctx.message.channel
            await channel.send(f"You have a total of {user_points} point(s)!")
    
    #using helper commands above
    @commands.command(help="Flip a coin potentially to double your points")
    async def flip(self, ctx, amount: int):
        coinF = coinFlip(ctx.message.author.id, amount)
        channel = ctx.message.channel
        if amount < 0:
            await channel.send("Cant bet negative numbers!")
            return
        if coinF == "Low":
            await channel.send("You need more points to gamble that!")
        else:
            pointsLeft = coinFlipResult(ctx.message.author.id, amount, coinF)
            if coinF == "Lost":
               await channel.send(f"Unlucky! You now have {pointsLeft} point(s)")
            else:
                await channel.send(f"Lets go!! You now have {pointsLeft} point(s)")
        

def setup(client):
    client.add_cog(Gambler(client))