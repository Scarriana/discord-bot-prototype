#@Scarriana#5999
#December 2022
#Monumenta Discord Task Bot Prototype: suggestion cog

import discord
from discord.ext import commands
from discord import ui, app_commands
import config
import traceback



class Suggestion(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@commands.command()
	#sync bot: this is necessary, but also needs more than what I have now
	async def sync_suggestion(self, ctx) -> None:
		await ctx.send('Syncing command recieved')
		fmt = await ctx.bot.tree.sync(guild=ctx.guild)
		await ctx.send(f'Synced {len(fmt)} commands in suggestion.py')
	
	@commands.Cog.listener()
	async def on_ready(self):
		print('Suggestion cog loaded.')


	@app_commands.command(name='suggestion', description='Enter a suggestion of how to improve the game. Bugs should be sent as a bug report.')
	async def bugreport(self, interaction: discord.Interaction, 
		label: str, description: str):

		embed = discord.Embed(title = 'Suggestion', 
			description= label + "\n" + description, 
			color = discord.Color.yellow())

		# print("about to send the embed")
		await interaction.response.send_message(embed=embed)


		#setting up cog for the bot: will need to adjust for which discord servers get passed into guilds
async def setup(bot):
	await bot.add_cog(Suggestion(bot), guilds=[discord.Object(id=config.GUILD_ID)])

