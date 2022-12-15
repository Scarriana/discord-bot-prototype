#@Scarriana#5999
#December 2022
#Monumenta Discord Task Bot Prototype: suggestion cog

import discord
from discord.ext import commands
from discord import ui, app_commands
import config
import traceback


class suggestion_Modal(discord.ui.Modal, title="Suggestion Form"):
	# category = discord.ui.TextInput(label='Category', style=discord.TextStyle.short, placeholder='Label must be one of: misc plugin item class boss quest build mob cmd discord advancement delve server npc enchantment gui website', default='misc', required = True, max_length=11)
	# response = discord.ui.TextInput(label='Suggestion', style=discord.TextStyle.paragraph,required = True, max_length=1800)
	# async def on_submit(self, interaction: discord.Interaction):
	# 	#embeded answer
	# 	embed = discord.Embed(title = self.title, description = (f"**{self.category.label}**\n{self.category}\n" + f"**{self.response.label}**\n{self.response}"), timestamp= datetime.now(), color = discord.Color.blue())
	# 	embed.set_author(name=interaction.user, icon_url= interaction.user.avatar)
	# 	await interaction.response.send_message(embed=embed)

	name=discord.ui.TextInput(
		label='suggestion', placeholder='aaaaaaa')

	feedback = discord.ui.TextInput(
		label='please work',
		placeholder = 'geedback here pls')

	async def on_submit(self, interaction: discord.Interaction):
		await interaction.response.send_message(f'Thanks for your feedback')



class Suggestion(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@commands.command()
	#sync bot: this is necessary, but also needs more than what I have now
	async def sync_sug(self, ctx) -> None:
		fmt = await ctx.bot.tree.sync(guild=ctx.guild)
		await ctx.send(f'Synced {len(fmt)} commands in suggestion.py')
	
	@commands.Cog.listener()
	async def on_ready(self):
		print('Suggestion cog loaded.')


	@app_commands.command(name="suggestion", description="suggestion form")
	async def suggestion(self, interaction: discord.Interaction):
		await interaction.response.send_modal(suggestion_Modal())

		# user = interaction.user
		# guild = interaction.guild
		# channel = interaction.channel


		#setting up cog for the bot: will need to adjust for which discord servers get passed into guilds
async def setup(bot):
	await bot.add_cog(Suggestion(bot), guilds=[discord.Object(id=config.GUILD_ID)])

