#@Scarriana#5999
#December 2022
#Monumenta Discord Task Bot Prototype: suggestion cog

import discord
from discord.ext import commands


class Suggestion(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	
	@commands.Cog.listener()
	async def on_ready(self):
		print('Suggestion cog loaded.')

	@commands.command()
	async def suggestion(self, ctx):
		embed=discord.Embed(description='suggestion')
		await ctx.channel.send(embed=embed)

	
async def setup(bot):
		await bot.add_cog(Suggestion(bot))

		

