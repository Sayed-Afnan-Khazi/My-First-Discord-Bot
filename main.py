# Discord bot

import discord
import os
from dotenv import load_dotenv
load_dotenv()

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'We are logged in! \n {client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        print("Message author is of the type:",type(message.author))
        return
    # # elif 
    # print(message.content.startswith('sa'))
    print(message.content)
    if True: #message.content.startswith("$")
        print("Sending a message!")
        await message.channel.send("Hello back!")
        print("Message sent")



botToken = os.getenv("TOKEN")
client.run(botToken)