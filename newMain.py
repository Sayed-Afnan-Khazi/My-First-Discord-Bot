# Discord bot
import asyncio
from discord.ext import commands
import discord
import os
import requests
import json
import aiohttp
from dotenv import load_dotenv
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
botToken = os.getenv("TOKEN")

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

extensions = [
    'ext.weather',
    'ext.hello',
    'ext.voicemanager',
    'ext.modtools',
]

command_prefix = commands.when_mentioned_or('!')

class AshBot(commands.Bot):
    def __init__(self):
        # Setting up the bot
        super().__init__(command_prefix=command_prefix,
                         intents=intents,
                        )
    
    async def on_ready(self):
        # Logging in message
        print(f'We are logged in! \n {self.user} has connected to Discord!')

    async def setup_hook(self):
        for extension in extensions:
            await self.load_extension(extension)
        # For aihttp's sessions
        self.session = aiohttp.ClientSession()
    
    async def on_message(self, message: discord.Message):
        # We don't want to reply to ourselves
        if message.author.bot:
            return
        print("Bro detected some message has been sent")
        print(message.content)

        ctx = await self.get_context(message, cls = commands.Context)
        if ctx.valid:
            await self.invoke(ctx)

    async def start(self):
        await super().start(token = botToken, reconnect = True)


async def run_bot():
    async with AshBot() as bot:
        await bot.start()

def start_bot():
    asyncio.run(run_bot())

if __name__ == '__main__':
    start_bot()

        
        