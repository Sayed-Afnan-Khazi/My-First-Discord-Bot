import os
import base64
from discord.ext import commands
import discord
import requests, json

from dotenv import load_dotenv
load_dotenv()


# Links, keys and stuff

VIRUS_TOTAL_API_KEY = os.getenv("VIRUS_TOTAL_API_KEY")
# VT_url = "https://www.virustotal.com/api/v3/urls/"

headers = {
    "accept": "application/json",
    "x-apikey": VIRUS_TOTAL_API_KEY
}


class ModTools(commands.Cog):
    '''Mod Tools like: link checker'''
    def __init__(self,bot):
        self.bot = bot
    
    # Doesn't work
    @commands.command(name = "malcheck")
    async def malcheck(self, ctx, check_url):
        # print("CheckURL is",check_url,"it's type is", type(check_url))
        url_id = base64.urlsafe_b64encode(check_url.encode()).decode().strip("=")
        VT_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        # print(f"VT URL SET! {VT_url}")

        # response = requests.get(VT_url, headers=headers)
        # print("GET request SUCCESS!")
        async with self.bot.session.get(VT_url, headers=headers) as response:
            j =  await response.json()
            # print("JSON formed!!")

        # print("ASYNC SUCCESS!!")
        votes = j["data"]["attributes"]["total_votes"]

        if votes['harmless'] > votes['malicious']:
            # print("ABOUT TO SEND SOMETHING")
            await ctx.send("This link is safe")
        else:
            # print("ABOUT TO SEND SOMETHING")
            await ctx.send("This link is not safe")

async def setup(bot):
    await bot.add_cog(ModTools(bot))
