import os
from discord.ext import commands
import discord

'''Handles unloading and reloading of cogs and other admin features.'''

class admin(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='reload')
    @commands.is_owner()
    async def reload(self, ctx, cog):
        '''Reloads the specified cog or all cogs if cogs="all".'''
        if cog.lower()=="all":
            try: 
                reloadCount = 0
                cogsCount = 0
                for filename in os.listdir('./ext/'):
                    if filename.endswith('.py') and not filename.startswith('_'):
                        cogsCount += 1
                        print(f"Reloading...{filename}")
                        await self.bot.unload_extension(f'ext.{filename[:-3]}')
                        await self.bot.load_extension(f'ext.{filename[:-3]}')
                        reloadCount += 1
                await ctx.send(f'Reloaded {reloadCount}/{cogsCount} cogs.')
            except Exception as e:
                await ctx.send(f'Error: {e}')
        else:
            try:
                await self.bot.unload_extension(f'ext.{cog}')
                await self.bot.load_extension(f'ext.{cog}')
                await ctx.send(f'Cog {cog} reloaded.')
            except Exception as e:
                await ctx.send(f'Error: {e}')
    

async def setup(bot):
    await bot.add_cog(admin(bot))