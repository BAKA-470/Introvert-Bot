import discord
import os 
from discord import message
from discord.ext import commands
import requests
import json
import random
from replit import db
from keep_server_on import keep_server_on


intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents = intents)

sad_words = ["sad", "depressed","unhappy", "angry","miserable","depressing", "crying", "sorrowful", "sorrow", "beaten","pissed off","cry" ,"good as dead","ugly"]

starter_encouragements =[
"Cheer up!",
  "Hang in there",
  "It's just a bad day",
  "You're a great person",
  "There are always some bad days",
  "You're amazing",
  "Chin up hero!!"
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

def delete_encouragements(index):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    if len(encouragements) > index:
      del encouragements[index]
      db["encouragements"] = encouragements
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  if db["responding"]: 
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])
    if any(word in message.content for word in sad_words):
      await message.channel.send(random.choice(options))
  if message.content.startswith('$new'):
    encouraging_message = message.content.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")
  
  
  if any(word in message.content for word in sad_words):
    await message.channel.send(random.choice(options))
  
  if message.content.startswith('$new'):
    encouraging_message = message.content.split("$new ",1)[1]
    await message.channel.send(encouraging_message)
  if message.content.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(message.content.split("$del",1)[1])
      delete_encouragements(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  if message.content.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  if message.content.startswith("$responding"):
    value = message.content.split("$responding ",1)[1]
    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")
    

keep_server_on()
client.run(os.environ['TOKEN'])

