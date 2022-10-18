import os
from discord.ext import commands
import discord

# class BetterMember():
#     '''Wrapper class around discordpy's member class'''
#     def __init__(self, member, isModMuted):
#         self.real = member
#         self.isModMuted = isModMuted
#         self.hasMic = False #Default


class VoiceManager(commands.Cog):

    def __init__(self,bot) -> None:
        self.bot = bot
        self.micHolderID = None
        self.userList = set()

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

        # For now checking if userlist resets or not
        self.userList.add(member.id)

        # Cases:

        if after.channel.name == "General": # We can use a list of practice room channels here
            # Entering the vc -> mute
            # Unless they have the mic
            print("I should mute you now")
            
            if self.micHolderID is None or self.micHolderID != member.id:
                await member.edit(mute = True)
            

            

            
        # elif   before.channel.name == "General":
        #     # Micmember has left

        #     # Reset mic


        

        # elif before.channel.name == "General":

        #     # Regular member/listener has left

       
        
        else:
            # Case when someone joins or does something in any other vc
            # They shouldn't be muted.

            await member.edit(mute = False)
        
        

        print("userList is:", self.userList)
    
    # @commands.command(name="getmic")
    # async def getmic(self, ctx, arg):
    #     if not arg:
    #         if not self.generalList[ctx.author.id]:
    #             await ctx.send(f"You don't seem to be in a practice room, {ctx.author.mention}")
    #         else:
    #             if self.generalListMicTaken:
    #                 await ctx.send(f"Looks like {self.generalListMicTakenMember.real.name} has the mic, please ask them for it :)")
    #             else:
    #                 self.generalList[ctx.author.id].hasMic = True
    #                 self.generalListMicTaken = True
    #                 await self.generalList[ctx.author.id].real.edit(mute = False)
    #                 await ctx.send(f"You're on the mic {ctx.author.mention}!!")
        


        
                




        
            

    

async def setup(bot):
    await bot.add_cog(VoiceManager(bot))
