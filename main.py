# Discord bot

import discord
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

intents = discord.Intents(
    guilds=True,
    members=True,
    bans=True,
    emojis=True,
    voice_states=True,
    guild_messages=True,
    guild_reactions=True,
    message_content=True,
)

client = discord.Client(intents=intents)

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
    # print("Message content:",message.content)
    # print("Message itself:",message)
    # print(message.content.split()[1])
    if message.content.startswith("!"): #message.content.startswith("$")
        print("Sending a message!")
        if message.content.startswith("!hello"):
            await message.channel.send("Hello back!")
            print("Message sent")
        elif message.content.startswith("!hi"):
            await message.channel.send(f"Hello there, {message.author.mention}")
            print("Message sent")
        elif message.content.startswith("!weather"):
            cityName = message.content.split()[1]
            base_url = "http://api.openweathermap.org/data/2.5/weather?"

            complete_url = base_url + "appid=" + WEATHER_API_KEY + "&q=" + cityName

            response = requests.get(complete_url)
            x = response.json()

            if x["cod"] != "404": # Error code if city not found or something else happened
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                weatherObj = x["weather"]
                weather_description = weatherObj[0]["description"]
                # Subtract 273 because API returns kelvin. Here we return celcius.
                reply = " ``` Temperature = " + str(current_temperature -273) + "\n atmospheric pressure (in hPa unit) = " + str(current_pressure) + "\n humidity (in percentage) = " + str(current_humidity) + "\n description = " + str(weather_description) + "```"

                await message.channel.send(reply)
            else:
                reply = "We searched far and wide, but couldn't find this city. Please check your spellings and try again :smiley:"
                await message.channel.send(reply)


        


if __name__ == '__main__':
    botToken = os.getenv("TOKEN")
    client.run(botToken)