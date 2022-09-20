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
        # print("Type is ",type(before.channel.name))
        print("MEMBER:",member.name, "BEFORE:",before.channel, "AFTER:",after.channel)

        
        # Managing Joining and leaving
        if after.channel.name == "General" and before.channel is None:
            print("MUTED!!!!!!!!!!!")
            self.generalList.append(member)
            await member.edit(mute = True)
        if before.channel.name == "General" and after.channel is None:
            print("UNMUTED!!!!!!!!!!!")
            self.generalList.remove(member)
            await member.edit(mute = False)
            

    

async def setup(bot):
    await bot.add_cog(VoiceManager(bot))
