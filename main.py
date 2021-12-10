import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

gmessages = joined = 0

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_member_join(member):
  for channel in member.guild.channels:
    if str(channel) == "general":
      await channel.send_message(f"""Welcome to the server {member.mention}""")


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  global gmessages
  gmessages += 1
  if message.author == client.user:
    return

  msg = message.content

  id = client.get_guild(int(os.getenv("ID")))
  channels = ["general"]
  valid_users = ["extreme1337#5244"]

  if str(message.channel) in channels and str(message.author) in valid_users:
        if msg.find("!hello") != -1:
            await message.channel.send("Hi") 
        elif msg == "!users":
            await message.channel.send(f"""# of Members: {id.member_count}""")
  
  if msg.startswith("$inspire"):
    quote = get_quote()
    await message.channel.send(quote)


  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options+list(db["encouragements"])
    
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = list(db["encouragements"])
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = list(db["encouragements"])
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]
    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN'))

