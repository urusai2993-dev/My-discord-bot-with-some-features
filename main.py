import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import urllib.request
import json
import random
import requests
import time

intents = discord.Intents.all()  #.all() if you want all permissions
intents.message_content = True       # needed to read messages from discord
load_dotenv()

# to extract the bot token
TOKEN = os.getenv('DISCORD_TOKEN') # MAKE SURE TO SAVE YOUR DISCORD BOT TOKEN IN A .ENV FILE

# assigning a prefix
bot = commands.Bot(command_prefix="*", intents=intents)

# funtion to calculate a and b number
@bot.command(name='operacion')
async def operacion(ctx, a, operar, b):
    try:
        a = int(a)
        b = int(b)

        if operar == "+":
            response = a + b
        elif operar == "-":
            response = a - b
        elif operar == "*":
            response = a * b
        elif operar == "/":
            response = a / b
        else:
            response = "⚠️ Please, write a valid operator.  (+ - / *)"

    except ZeroDivisionError:
        response = "⚠️ You cant divide by zero, pls insert another number."
    except ValueError:
        response = "⚠️ You must enter valid numbers."

    await ctx.send(f"📌 Result: {response}")


# funcion de lovecalc 
@bot.command(name='lovecalc')
async def lovecalc(ctx, user1 : discord.Member, user2 : discord.Member):
    porcentaje = random.randint(0, 100)  # random number 0-100
    if porcentaje == 100:
        mensaje = f"💘 {user1.mention} and {user2.mention}, you are {porcentaje}% compatible. YOU'RE THE PERFECT COUPLE!"
    elif porcentaje in range(80,99):
        mensaje = f"💘 {user1.mention} and {user2.mention} have a {porcentaje}% chance. Youre made for each other!"
    elif porcentaje in range(60,79):
        mensaje = f"💘 {user1.mention} and {user2.mention} have a {porcentaje}% chance. You really like each other!"
    elif porcentaje in range(30,59):
        mensaje = f"💘 {user1.mention} and {user2.mention} have a {porcentaje}% chance. Have you thought about meeting someone else?"
    elif porcentaje in range(10,29):
        mensaje = f"💘 {user1.mention} and {user2.mention} have a {porcentaje}% chance. You dont love each other. Go find another soulmate, losers."
    else:
        mensaje = f"💘 {user1.mention} and {user2.mention} have a {porcentaje}% chance. Just end it already."
    await ctx.send(mensaje)


# # funcion de youtube
# key =''
# @bot.command(name='subs')
# async def subs(ctx, username):
#     data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=" + username + "&key=" + key).read()
#     subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
#     response = username + " tiene " + "{:,d}".format(int(subs)) + " suscriptores!"
#     await ctx.send(response)    


# flip coin
@bot.command(name='flip')
async def flip(ctx):
    hola = random.randint(1, 2)
    if hola == 1:
        mensaje = "heads"
    elif hola == 2:
        mensaje = "tails"
    await ctx.send(mensaje)


# funtion random meme
@bot.command(name="meme")
async def meme(ctx):
    url = "https://meme-api.com/gimme"
    response = requests.get(url).json()
    meme_url = response["url"]

    embed = discord.Embed(title="😂 Meme random", color=discord.Color.random())
    embed.set_image(url=meme_url)

    await ctx.send(embed=embed)


# function: random jokes 
@bot.command(name="chiste")
async def chiste(ctx):
    url = 'https://official-joke-api.appspot.com/random_joke'
    response = requests.get(url).json()
    setup = response["setup"]
    punchline = response["punchline"]
    embed = discord.Embed(
        title="chiste random",
        description = f"{setup}\n\n**{punchline}**",
        color=discord.Color.random())
    await ctx.send(embed=embed)


# function: random dogs
@bot.command(name = "perritos")
async def perritos(ctx):
    url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(url).json()
    message = response["message"]
    embed = discord.Embed(
        title = "perrito random",
        color = discord.Color.random(),
)
    embed.set_image(url=message)
    await ctx.send(embed=embed)


# Function: ping-pong!
@bot.command(name = "ping")
async def ping(ctx):
    inicio = time.time()                 
    msg = await ctx.send("⏳ loading...")  
    fin = time.time()                    
    
    final = fin - inicio
    await msg.edit(content=f"🏓 Pong!\nIt took: {final:.2f} seconds")


# function: dice
@bot.command(name="dice")
async def dice(ctx):
    random_number = random.randint(1, 6)
    await ctx.send(f"🎲 You rolled a {random_number}!")

# function: userinfo
@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    embed = discord.Embed(title=f"Info about {member.name}:", color=discord.Color.random())
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="- User ID: ", value=member.id, inline=False)
    embed.add_field(name="- Joined the server: ", value=member.joined_at.strftime("%d/%m/%Y"), inline=False)
    embed.add_field(name="- Account created: ", value=member.created_at.strftime("%d/%m/%Y"), inline=False) 
    await ctx.send(embed=embed)


# function: weather
@bot.command(name="weather")
async def weather(ctx, city: str):
    API_KEY = "put your api key here"  # I used OpenWeather API
    url_weather = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=en"
    response = requests.get(url_weather)
    data = response.json()
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"].title()

    embed = discord.Embed(title=f"Weather Forecast for {city.title()}", color=discord.Color.random())
    embed.set_thumbnail(url='https://cdn.jim-nielsen.com/ios/512/weather-2021-12-07.png?rf=1024')
    embed.add_field(name="Temperature", value=f"The current temperature is: {temp} °C", inline=False)
    embed.add_field(name="Description", value=description, inline=False)
    await ctx.send(embed=embed)

# para iniciar el bot
bot.run(TOKEN)
