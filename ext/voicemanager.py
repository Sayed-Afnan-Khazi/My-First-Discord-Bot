import os
from discord.ext import commands
import discord

'''Handles the performer and audience roles for selected voice channels'''

AUDIENCE_ROLE_ID = 1045963196881707009 
PERFORMER_ROLE_ID = 1045963339634835507
GENERAL_CHANNEL_ID = 1012056614238441605
FESTIVAL_CHANNEL_ID = 1054704196206727261

# What happens if the bot shuts down??

class VoiceManager(commands.Cog):

    def __init__(self,bot) -> None:
        self.bot = bot
        self.channels = [GENERAL_CHANNEL_ID, FESTIVAL_CHANNEL_ID]
        # For Multiple voice channels?? - self.performer as a dictionary with channel ID as keys, channel checking as a list
        self.performer = {GENERAL_CHANNEL_ID:None,
                        FESTIVAL_CHANNEL_ID:None} # Stores the channel ID:user ID of the performer

    @commands.command(name="invoice")
    async def invoice(self, ctx):
        if ctx.author.voice:
            voiceChannelName = ctx.author.voice.channel
            await ctx.send(f"You are in the voice channel: {voiceChannelName}")
        else:
            await ctx.send(f"You are currently not in a voice/stage channel {ctx.author.mention}")
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Note: VC Logger has been moved to voicelogger.py

        ## Performer and audience roles management:

        # Cases:
        # 1. You are joining the vc from outside
        # 2. You are joining the vc from some other vc
        # 3. You are leaving the vc to outside
        # 4. You are leaving the vc to some other vc

        if after.channel is None and before.channel.id in self.channels:
            channelID = before.channel.id
            # Case 3:
            # Leaving the vc -> remove audience and performer
            # if they are a performer -> also reset performer
            isAudience = False
            isPerformer = False

            for role in member.roles:
                if role.id == AUDIENCE_ROLE_ID:
                    isAudience = True
                if role.id == PERFORMER_ROLE_ID:
                    isPerformer = True

            if isAudience and not isPerformer:
                print("AUDIENCE BUT NOT PERFORMER")
                myRoleobj = discord.Object(id=AUDIENCE_ROLE_ID)
                await member.remove_roles(myRoleobj)
                print("REMOVED AUDIENCE ROLE")
            
            if isPerformer:
                print("THE PERFORMER HAS LEFT.")
                myRoleobj = discord.Object(id=PERFORMER_ROLE_ID)
                await member.remove_roles(myRoleobj)
                self.performer[channelID] = None
                print("REMOVED PERFORMANCE ROLE")

        elif after.channel.id in self.channels:
            channelID = after.channel.id
            # Case 1 and 2:
            # Entering the vc -> make audience

            isAudience = False
            isPerformer = False

            for role in member.roles:
                if role.id == AUDIENCE_ROLE_ID:
                    isAudience = True
                if role.id == PERFORMER_ROLE_ID:
                    isPerformer = True

            if not isAudience and not isPerformer:
                print("NEITHER AUDIENCE NOR PERFORMER")
                myRoleobj = discord.Object(id=AUDIENCE_ROLE_ID)
                await member.add_roles(myRoleobj)
                print("ADDED AUDIENCE ROLE")
            if isPerformer:
                pass
        
        elif before.channel.id in self.channels:
            channelID = before.channel.id
            # Case 4:
            # Leaving the vc -> remove audience and performer
            # if they are a performer -> also reset performer
            isAudience = False
            isPerformer = False

            for role in member.roles:
                if role.id == AUDIENCE_ROLE_ID:
                    isAudience = True
                if role.id == PERFORMER_ROLE_ID:
                    isPerformer = True

            if isAudience and not isPerformer:
                print("AUDIENCE BUT NOT PERFORMER")
                myRoleobj = discord.Object(id=AUDIENCE_ROLE_ID)
                await member.remove_roles(myRoleobj)
                print("REMOVED AUDIENCE ROLE")
            
            if isPerformer:
                print("THE PERFORMER HAS LEFT.")
                myRoleobj = discord.Object(id=PERFORMER_ROLE_ID)
                await member.remove_roles(myRoleobj)
                self.performer[channelID] = None
                print("REMOVED PERFORMANCE ROLE")

    @commands.command(name="getperformer")
    async def getperformer(self,ctx):
        # Checking if they are in the vc
        if ctx.author.voice:
            if ctx.author.voice.channel.id in self.channels:
                channelID = ctx.author.voice.channel.id
                if self.performer[channelID] is None:
                    # Adding the performer role
                    myRoleobj = discord.Object(id=PERFORMER_ROLE_ID)
                    self.performer[channelID] = ctx.author.id
                    await ctx.author.add_roles(myRoleobj)
                    print("ADDED PERFORMER ROLE.")
                    # Removing the pre-added audience role
                    myRoleobj = discord.Object(id=AUDIENCE_ROLE_ID)
                    await ctx.author.remove_roles(myRoleobj)
                    print("REMOVED AUDIENCE ROLE")
                else:
                    await ctx.send(f"Sorry, the role is taken for this channel by <@{self.performer}>. To reset the role, please ask them to leave the channel.")
        else:
            await ctx.send("You are not in the voice channel.")

    @commands.command(name="resetperformer")
    async def resetperformer(self,ctx):
        # Checking if they are in the vc
        if ctx.author.voice:
            if ctx.author.voice.channel.id in self.channels:
                channelID = ctx.author.voice.channel.id
                if self.performer[channelID] is None:
                    await ctx.send("There is no performer to reset.")
                else:
                    # Removing the performer role
                    myRoleobj = discord.Object(id=PERFORMER_ROLE_ID)
                    await ctx.author.remove_roles(myRoleobj)
                    print("REMOVED PERFORMER ROLE.")
                    # Adding the pre-added audience role
                    myRoleobj = discord.Object(id=AUDIENCE_ROLE_ID)
                    await ctx.author.add_roles(myRoleobj)
                    print("ADDED AUDIENCE ROLE")
                    self.performer[channelID] = None
        else:
            await ctx.send("You are not in the voice channel.")


async def setup(bot):
    await bot.add_cog(VoiceManager(bot))
