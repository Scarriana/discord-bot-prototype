#@Scarriana#5999
#December 2022
#Monumenta Discord Task Bot Prototype: bug report cog


import discord
from discord.ext import commands


class Bug_Report(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	
	@commands.Cog.listener()
	async def on_ready(self):
		print('Bug Report cog loaded.')

	@commands.command()
	async def bugreport(self, ctx):
		embed=discord.Embed(description='bug report')
		await ctx.channel.send(embed=embed)

	
async def setup(bot):
		await bot.add_cog(Bug_Report(bot))
