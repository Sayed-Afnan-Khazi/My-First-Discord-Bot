import os
from discord.ext import commands
import discord


AUDIENCE_ROLE_ID = 1045963196881707009 
PERFORMER_ROLE_ID = 1045963339634835507


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

            isAudience = False
            isPerformer = False

            for role in member.roles:
                if role.id == AUDIENCE_ROLE_ID:
                    isAudience = True
                if role.id == PERFORMER_ROLE_ID:
                    isPerformer = True

            if not isAudience and not isPerformer:
                print("NEITHER AUDIENCE NOR PERFORMER")
                await member.add_role(AUDIENCE_ROLE_ID) # WHY DOES THIS NOT WORK
        

async def setup(bot):
    await bot.add_cog(VoiceManager(bot))
