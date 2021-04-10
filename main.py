import discord
import os
import random
from replit import db
#from keep_alive import keep_alive

client = discord.Client()

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
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Over This Server'))

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

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
    #welcome the member on direct msg
    await member.send(f':computer: Welcome to {guild.name}, {member.name}! :nerd:')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

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
        colour=0x4EE3D9
      )
      helpEmbed.add_field(name="$list", value="Shows all courses in the list", inline=False)
      helpEmbed.add_field(name="$add + link", value="Add a new course", inline=False)
      helpEmbed.add_field(name="del + number", value="Delete corresponding course (list starts in 0)", inline=False)
      helpEmbed.add_field(name="$random", value="Selects a random course", inline=False)
      await message.channel.send(embed=helpEmbed)

#keep_alive()
client.run(os.getenv('TOKEN'))