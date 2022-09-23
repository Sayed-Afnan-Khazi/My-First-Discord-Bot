import os
from discord.ext import commands
import discord

class BetterMember():
    '''Wrapper class around discordpy's member class'''
    def __init__(self, member, isModMuted):
        self.real = member
        self.isModMuted = isModMuted
        self.hasMic = False #Default


class VoiceManager(commands.Cog):

    def __init__(self,bot) -> None:
        self.bot = bot
        self.generalList = {} # hashtable id:BetterMember object
        self.generalListMicTaken = False
        self.generalListMicTakenMember = None # BetterMember object

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

        # if they do not have a bettermember obj yet, make one
        # Otherwise, get their previously stored object
        if not self.generalList[member.id]:
            thismember = BetterMember(member,member.voice.mute)
        else:
            thismember = self.generalList[member.id]


        # Cases:

        if after.channel.name == "General": # We can use a list of practice room channels here
            # Entering a vc -> mute
            # Unless they have the mic
            print("I should mute you now")

            self.generalList[thismember.real.id] = thismember
            if not thismember.hasMic:
                await member.edit(mute = True)

            
        elif thismember.hasMic and before.channel.name == "General":
            # Micmember has left

            # Reset mic
            self.generalListMicTaken = False
            self.generalListMicTakenMember = None

            # Deleting their bettermember obj
            del self.generalList[thismember.real.id]
            if not thismember.isModMuted: # is this even needed??
                await member.edit(mute = False)

        elif before.channel.name == "General":
            # Regular member/listener has left
            # Deleting their bettermember obj

            del self.generalList[thismember.real.id]
            if not thismember.isModMuted:
                await member.edit(mute = False)
        
        else:
            # Case when someone joins or does something in any other vc
            # They shouldn't be muted.

            if not thismember.isModMuted:
                await member.edit(mute = False)
        
        

        # print("GeneralList is:", self.generalList)
    
    @commands.command(name="getmic")
    async def getmic(self, ctx, arg):
        if not arg:
            if not self.generalList[ctx.author.id]:
                await ctx.send(f"You don't seem to be in a practice room, {ctx.author.mention}")
            else:
                if self.generalListMicTaken:
                    await ctx.send(f"Looks like {self.generalListMicTakenMember.real.name} has the mic, please ask them for it :)")
                else:
                    self.generalList[ctx.author.id].hasMic = True
                    self.generalListMicTaken = True
                    await self.generalList[ctx.author.id].real.edit(mute = False)
                    await ctx.send(f"You're on the mic {ctx.author.mention}!!")
        


        
                




        
            

    

async def setup(bot):
    await bot.add_cog(VoiceManager(bot))
