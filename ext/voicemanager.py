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
            # Entering the vc -> make audience
            # Unless they are a performer

            print(member.roles)
            # print(type(member.roles))
            # print(member.roles[2])
            isAudience = False
            isPerformer = False
            for role in member.roles:
                print(role)
                print(type(role))
                # Note to self: this is a role object of it's own. Going to have to use an API function to check against this
                # if 'Role id=1045963196881707009' in role: # Audience Role ID
                #     isAudience = True
                # if "Role id=1045963339634835507" in role: # Performer Role ID
                #     isPerformer = True

            print("DONE WITH FOR LOOP")
            if not isAudience and not isPerformer:
                print("NEITHER AUDIENCE NOR PERFORMER")
                await member.add_role('Audience')
            

            
            

            

            
        # elif   before.channel.name == "General":
        #     # Micmember has left

        #     # Reset mic


        

        # elif before.channel.name == "General":

        #     # Regular member/listener has left

       
        
        # else:
            # Case when someone joins or does something in any other vc
            # They shouldn't be muted.

            # await member.edit(mute = False)
        
        

        # print("userList is:", self.userList)
    
    # @commands.command(name="getmic")
    # async def getmic(self, ctx, arg):
    #     if not arg
        


        
                




        
            

    

async def setup(bot):
    await bot.add_cog(VoiceManager(bot))
