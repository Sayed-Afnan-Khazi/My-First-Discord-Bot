import os
from discord.ext import commands
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

        # response = requests.get(complete_url)
        async with self.bot.session.get(complete_url) as response:
            x = await response.json()

        if x["cod"] != "404": # Error code if city not found or something else happened
            y = x["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            weatherObj = x["weather"]
            weather_description = weatherObj[0]["description"]
            # Subtract 273 because API returns kelvin. Here we return celcius.
            current_temperature_celcius = current_temperature -273
            reply = " ``` Temperature = " + str(current_temperature_celcius) + "\n atmospheric pressure (in hPa unit) = " + str(current_pressure) + "\n humidity (in percentage) = " + str(current_humidity) + "\n description = " + str(weather_description) + "```"
            # await ctx.send(reply)
            if current_temperature_celcius>=40:
                embedEmoji = "🥵"
            elif current_temperature_celcius>=30:
                embedEmoji = "😎"
            elif current_temperature_celcius>=10:
                embedEmoji = "😄"
            elif current_temperature_celcius<=10:
                embedEmoji = "🥶"
            print("Sending an embed now!")
            embed = discord.Embed(title=f"Weather report for {cityName}", description = embedEmoji+"\n"+reply,  ) # icon = "/istockphoto-1187576166-612x612.jpg"
            embed.set_author(name = "AshBot Weather Reporter", icon_url = "https://cdn.discordapp.com/attachments/1012056614238441604/1019658018239021097/istockphoto-1187576166-612x612.jpg") #icon = "/istockphoto-1187576166-612x612.jpg"
            # print(embed)
            await ctx.send(embed = embed)
        else:
            reply = "We searched far and wide, but couldn't find this city. Please check your spellings and try again :smiley:"
            await ctx.send(reply)

async def setup(bot):
    await bot.add_cog(Weather(bot))