import discord
import os
import random
import requests
import json
from replit import db
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="!", intents = intents)

status = cycle(['with fire', 'with knives', 'with feelings', 'with hearts', 'with myself', 'dead'])
locations = ['oshawa', 'toronto', 'mississauga', 'brampton', 'scarborough']

def update_courses(course_link):
  if "courses" in db.keys():
    courses = db["courses"]
    courses.append(course_link)
    db["courses"] = courses
  else:
    db["courses"] = [course_link]

def delete_course(index):
  courses = db["courses"]
  if len(courses) > index:
    del courses[index]
    db["courses"] = courses

def get_weather(location):
  url = 'https://community-open-weather-map.p.rapidapi.com/find'
  querystring = {"q":location,"lat":"0","lon":"0","callback":"test","id":"2172797","lang":"null","units":"\"metric\" or \"imperial\"","mode":"xml, html"}
  headers = {
    'x-rapidapi-key': f"{os.getenv('W-CREDENTIALS')}",
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
  }
  response = requests.get(url, headers=headers, params=querystring)
  jsonData = json.loads(response.text[5:len(response.text) - 1])
  #print(len(response.text))
  return(jsonData['list'][0])

def get_temperature(location):
  weather = get_weather(location)
  tempK = float(weather['main']['temp'])
  tempC = round(tempK - float(273.15), 2)
  return tempC

def get_location(message):
  msg = message.lower().split()
  for location in locations:
    for word in msg:
      if location == word:
        return location

@client.event
async def on_ready():
  change_status.start()
  print('Logged in as {0.user}'.format(client))
  

#responding new joiner
@client.event
async def on_member_join(member): 
                         
    #guild = client.get_guild(814620705425195049)   #serverID
    #channel = guild.get_channel(814620705794687017)   #channelID
    
    #testing server
    guild = client.get_guild(829803116270190663)
    channel = guild.get_channel(829803116270190666)

    print('join info: ',member.name)

    #welcome the member on server
    await channel.send(f':computer: Welcome, its COMP216/SEC401 Group 2 {member.mention} ! :nerd:')
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.lower() == '$hi':
        await message.channel.send('Hello! We are group 2')

    if msg.lower().startswith('$members'):
        await message.channel.send('Aloy, Alussius\nCordeiro de Souza Puttomatti, Amanda\nKhaira, Gurkirat\nSeo, Anna Eunbi\nVolpe, Joseph')

    if msg.lower().startswith('$description'):
        await message.channel.send('The goal of our project is making a Discord Bot that will perform automated processes. Automated programs that look and act like users and automatically respond to events and commands on Discord are called bots. Discord bot users (or just bots) have nearly unlimited applications due to its “middle man”, like nature. This allows for flexable ideas/features which can be as simple as a string response when messaging the bot with a user, or using the bot to connect and display data on a database site.')

    if msg.lower().startswith('$list'):
        courses = []
        if "courses" in db.keys():
            courses = db["courses"]
        for x in courses:
          await message.channel.send(x)

    if msg.lower().startswith('$add'):
      course_link = msg.split("$add ",1)[1]
      update_courses("<"+course_link+">")
      await message.channel.send("New course added")

    if msg.lower().startswith('$del'):
      courses = []
      if "courses" in db.keys():
        index = int(msg.split("$del",1)[1])
        delete_course(index)
        courses = db["courses"]
      await message.channel.send("Course removed")
    
    if msg.lower().startswith('$random'):
      await message.channel.send(random.choice(db["courses"]))

    if msg.lower().startswith('$temperature'):
      if any(word in msg.lower() for word in locations):
        loc = get_location(msg)
        temp = get_temperature(loc)
        reply = f"The temperature in {loc} is {temp} degree Celsius"
        await message.channel.send(reply)

    if msg.lower().startswith("?help"):
      helpEmbed = discord.Embed(
        title="Commands list",
        colour=0x4EE3D9
      )
      helpEmbed.add_field(name="--------------------------------------------------------------------------------------------------", value="Project commands", inline=False)
      helpEmbed.add_field(name="$hi", value="Greeting", inline=True)
      helpEmbed.add_field(name="$members", value="Show team members names", inline=True)
      helpEmbed.add_field(name="$description", value="Show project description", inline=True)
      helpEmbed.add_field(name="--------------------------------------------------------------------------------------------------", value="Courses commands", inline=False)
      helpEmbed.add_field(name="$list", value="Shows all courses in the list", inline=True)
      helpEmbed.add_field(name="$add + link", value="Add a new course", inline=True)
      helpEmbed.add_field(name="del + number", value="Delete corresponding course (list starts in 0)", inline=True)
      helpEmbed.add_field(name="$random", value="Selects a random course", inline=True)
      helpEmbed.add_field(name="--------------------------------------------------------------------------------------------------", value="Temperature commands", inline=False)
      helpEmbed.add_field(name="$temperature + location", value="Display the temperature, in Celsius, of the location", inline=False)
      helpEmbed.add_field(name="Locations available: ", value="Oshawa, Toronto, Mississauga, Brampton, Scarborough", inline=False)
      helpEmbed.add_field(name="--------------------------------------------------------------------------------------------------", value="Admin commands", inline=False)
      helpEmbed.add_field(name="!clear", value="Clear the last 5 messages", inline=True)
      helpEmbed.add_field(name="!kick + @member name", value="Kick the member from the server", inline=True)
      helpEmbed.add_field(name="!ban + @member name", value="Ban the member from the server", inline=True)
      
      await message.channel.send(embed=helpEmbed)

    responses = ["If I were any better, I'd be you.",
                 'Average. Not terrific, not terrible, just average.',
                 "I’ve been going through some crests and troughs in my life. Is everything stable at your end?",
                 "Overworked and underpaid.",
                 "Like you, but better.",
                 "Can't complain. Nobody listens to me anyway.",
                 "All the better, now that you asked.",
                 "I don't know, you tell me. How am I right now?",
                 "I love you.",
                 "Not so well, does that bother you?",
                 "Somewhere between better and best.",
                 "I was fine until you asked.",
                 "Better now that I'm talking to you.",
                 "Well, I haven't had my morning coffee yet and no one has gotten hurt, so I'd say pretty good at this point in time.",
                 "Good at minding my own business? Better than most people.",
                 "I can't complain! It's against the Company Policy.",
                 "Well, unless the weather has different plans in store."]

    if msg.lower() == 'how are you?' or msg.lower() == 'how are you' or msg.lower() == 'how r u' or msg.lower() == 'how are u' or msg.lower() == 'how u doing' or msg.lower() == 'how are you doing':
      response = random.choice(responses)
      await message.channel.send(response)             

    await client.process_commands(message)

@client.command()
async def ping(ctx):
  await ctx.send(f'{round(client.latency * 1000)}ms')

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)

@tasks.loop(seconds=30)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

keep_alive()
client.run(os.getenv('TOKEN'))