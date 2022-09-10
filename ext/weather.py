import os
from discord import commands
import discord
import requests, json

from dotenv import load_dotenv
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

class Weather(commands.Cog):
    '''Weather API commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "weather")
    async def weather(self, ctx, cityName):

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

            await ctx.send(reply)
        else:
            reply = "We searched far and wide, but couldn't find this city. Please check your spellings and try again :smiley:"
            await ctx.send(reply)

async def setup(bot):
    await bot.add_cog(Weather(bot))