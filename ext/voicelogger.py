import os
from discord.ext import commands
import discord

'''Handles the voice state updates logger for moderation purposes.
Built with Love <3 by Afnan for the Piano Planet Discord Server.'''

# Dictionary of Guild IDs and their corresponding logs channel IDs
# Used to route the logs to the correct logging channel
# Format:
# {Guild_Id : Logs_Channel_Id}
VC_LOGS_CHANNEL_IDS = {1012056613798019092:1066056878242680935, # Oofnan's Bot Playground
                        686016539094417478:849320334641463356, # Piano-Planet-Staging
                        }

class voiceChannelsLogger(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        ## Sending info to the logs channel

        # Getting the logs channel for that server
        try:
            logs_channel_id = VC_LOGS_CHANNEL_IDS[member.guild.id]
        except KeyError:
            print("Logging Channel not found for this guild. Please set it up.")
            return

        # Getting the logs channel object
        logs_channel = self.bot.get_channel(logs_channel_id) # Is this inefficient? Getting the channel every time?
        # Getting the timestamp
        utc_time_now = discord.utils.utcnow()
        the_time_now = discord.utils.format_dt(utc_time_now, style='T') # Formatting the datetime

        # bulk_insert = '' # here or global?
        if after.channel and before.channel:
            # Avoiding mute/unmute/deafen/undeafen stuff
            if before.channel.id == after.channel.id:
                return
            # Moving between channels
            send_msg = f"[{the_time_now}] {member.mention} has moved from {before.channel.mention} to {after.channel.mention}"
            await logs_channel.send(send_msg)
        elif after.channel is None and before.channel:
            # Leaving the vc
            send_msg = f"[{the_time_now}] {member.mention} has left {before.channel.mention}"
            await logs_channel.send(send_msg)
        elif after.channel:
            # Joining the vc
            send_msg = f"[{the_time_now}] {member.mention} has joined {after.channel.mention}"
            await logs_channel.send(send_msg)
        # For DEBUGGING:
        print("A VC Log message was sent.")

        ## Need to implement a cooldown here:
        # bulk_insert = bulk_insert + '\n' + send_msg
        #1 Check for a cooldown - Otherwise, the Bot might get flagged for spamming
        #2 send the bulk insert and reset it
        #3 or send a single message


async def setup(bot):
    await bot.add_cog(voiceChannelsLogger(bot))