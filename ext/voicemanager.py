import os
from discord.ext import commands
import discord

class VoiceManager(commands.Cog):

    def __init__(self,bot) -> None:
        self.bot = bot
        self.generalList = []

    @commands.command(name="invoice")
    async def invoice(self, ctx):
        voiceChannelName = ctx.author.voice.channel
        if voiceChannelName:
            await ctx.send(f"You are in the voice channel: {voiceChannelName}")
        else:
            ctx.send(f"You are currently not in a voice/stage channel {ctx.author.mention}")
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        print("MEMBER:",member.name, "BEFORE:",before.channel, "AFTER:",after.channel)
        
        if after.channel.name == "General": # We can use a list of practice room channels here
            self.generalList.append(member)
        else:
            self.generalList.remove(member)

        print("GeneralList is:", self.generalList)


        for x in self.generalList:
            if x and not x.voice.mute:
                x.edit(mute = True)


        
            

    

async def setup(bot):
    await bot.add_cog(VoiceManager(bot))
