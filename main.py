import discord
import os
import random
from replit import db
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle
#from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=".", intents = intents)

status = cycle(['with fire', 'with knives', 'with feelings', 'with hearts', 'with myself', 'dead'])

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

@client.event
async def on_ready():
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

    if msg.lower().startswith("?help"):
      helpEmbed = discord.Embed(
        title="Commands list",
        colour=0x4EE3D9,
        description="-----------------------------------"
      )
      helpEmbed.add_field(name="$hi", value="Greeting", inline=False)
      helpEmbed.add_field(name="$members", value="Show team members names", inline=False)
      helpEmbed.add_field(name="$description", value="Show project description", inline=False)
      helpEmbed.add_field(name="$list", value="Shows all courses in the list", inline=False)
      helpEmbed.add_field(name="$add + link", value="Add a new course", inline=False)
      helpEmbed.add_field(name="del + number", value="Delete corresponding course (list starts in 0)", inline=False)
      helpEmbed.add_field(name="$random", value="Selects a random course", inline=False)
      
      await message.channel.send(embed=helpEmbed)

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

#keep_alive()
client.run(os.getenv('TOKEN'))