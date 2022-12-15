#@Scarriana#5999
#December 2022
#Monumenta Discord Task Bot Prototype: bug report cog
import discord
#from discord import app_commands
from discord.ext import commands
from discord import ui, app_commands
# from discord app_commands import Choice
import datetime
import config

class Bug_Report(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot



	#sync bot: this is necessary, but also needs more than what I have now
	@commands.command()
	async def sync_report(self, ctx) -> None:
		fmt = await ctx.bot.tree.sync(guild=ctx.guild)
		await ctx.send(f'Synced {len(fmt)} commands.')
	
	#on ready
	@commands.Cog.listener()
	async def on_ready(self):
		print('Bug Report cog loaded.')

	@app_commands.command(name='bugreport', description='Enter a description of your bug. Game breaking or exploits bugs should be DM\'d to a moderator')
	async def bugreport(self, interaction: discord.Interaction, 
		label: str, description: str, file: discord.Attachment=None):

		embed = discord.Embed(title = 'Bug Report', 
			description= label + "\n" + description, 
			color = discord.Color.purple())
		# embed.set_author(name=interaction.user_url)
		# print(interaction.user + "\n")
		# report_embed = discord.Embed(title = 'Bug Report', 
		# 	description = description, 
		# 	color = discord.Color.purple())

		#embed.set_author(name=interaction.user, icon_url= interaction.user.avatar)

		# print("about to send the embed")
		await interaction.response.send_message(embed=embed)

#setting up cog for the bot: will need to adjust for which discord servers get passed into guilds
async def setup(bot):
	await bot.add_cog(Bug_Report(bot), guilds=[discord.Object(id=config.GUILD_ID)])