from discord.ext import commands
import discord

class Conversation(commands.Cog):
    '''Basic Conversational Commands'''
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(name = "hello")
    async def hello(self, ctx):
        print("Bro detected hello")
        await ctx.send("Hello back!")

    @commands.command(name = "hi")
    async def hi(self, ctx):
        print("Bro detected hi")
        await ctx.send(f"Hello there, {ctx.author.mention}")
    
async def setup(bot):
    await bot.add_cog(Conversation(bot))
