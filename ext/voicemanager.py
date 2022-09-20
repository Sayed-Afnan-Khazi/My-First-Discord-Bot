import os
from discord.ext import commands
import discord

class VoiceManager(commands.Cog):

    def __init__(self,bot) -> None:
        self.bot = bot

    @commands.command(name="invoice")
    async def invoice(self, ctx):
        voiceChannelName = ctx.author.voice.channel
        if voiceChannelName:
            await ctx.send(f"You are in the voice channel: {voiceChannelName}")
        else:
            ctx.send(f"You are currently not in a voice/stage channel {ctx.author.mention}")
    
    @commands.Cog.listener()
    async def on_voice_state_update(member, before, after):
        print(member.name, before, after)
        await member.edit(mute = True)

    

async def setup(bot):
    await bot.add_cog(VoiceManager(bot))
