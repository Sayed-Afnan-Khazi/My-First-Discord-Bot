import os
from discord.ext import commands
import discord


AUDIENCE_ROLE_ID = 1045963196881707009 
PERFORMER_ROLE_ID = 1045963339634835507
GENERAL_CHANNEL_ID = 1012056614238441605

# What happens if the bot shuts down??
class VoiceManager(commands.Cog):

    def __init__(self,bot) -> None:
        self.bot = bot
        self.performer = None

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


        # Cases:
        # 1. You are joining the vc from outside
        # 2. You are joining the vc from some other vc
        # 3. You are leaving the vc to outside
        # 4. You are leaving the vc to some other vc

        if after.channel is None and before.channel.id == GENERAL_CHANNEL_ID:
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
                print("REMOVED PERFORMANCE ROLE")

        elif after.channel.id == GENERAL_CHANNEL_ID:
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
        
        elif before.channel.id == GENERAL_CHANNEL_ID:
            # Case 4:
            # Leaving the vc -> remove audience and performer
            # if they are a performer -> also reset performer
            print("YIIIIIKEEEEeeeeeeeeees")
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
                print("REMOVED PERFORMANCE ROLE")

async def setup(bot):
    await bot.add_cog(VoiceManager(bot))
