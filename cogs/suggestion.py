#@Scarriana#5999
#December 2022
#Monumenta Discord Task Bot Prototype: suggestion cog

import discord
from discord.ext import commands
from discord import ui, app_commands
from datetime import datetime


class suggestion_Modal(discord.ui.Modal, title="Suggestion Form"):
	category = discord.ui.TextInput(label='Category', style=discord.TextStyle.short, placeholder='Label must be one of: misc plugin item class boss quest build mob cmd discord advancement delve server npc enchantment gui website', default='misc', required = True, max_length=11)
	response = discord.ui.TextInput(label='Suggestion', style=discord.TextStyle.paragraph,required = True, max_length=1800)
	async def on_submit(self, interaction: discord.Interaction):
		#embeded answer
		embed = discord.Embed(title = self.title, description = (f"**{self.category.label}**\n{self.category}\n" + f"**{self.response.label}**\n{self.response}"), timestamp= datetime.now(), color = discord.Color.blue())
		embed.set_author(name=interaction.user, icon_url= interaction.user.avatar)
		await interaction.response.send_message(embed=embed)


class Suggestion(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	
	@commands.Cog.listener()
	async def on_ready(self):
		print('Suggestion cog loaded.')

	@commands.command(name="suggest", description="suggestion form")
	async def suggest(self, interaction: discord.Interaction):
		await interaction.response.send_modal(suggestion_Modal)

		# user = interaction.user
		# guild = interaction.guild
		# channel = interaction.channel

	@commands.command()
	#sync bot: this is necessary, but also needs more than what I have now
	async def sync_sug(self, ctx) -> None:
		fmt = await ctx.bot.tree.sync(guild=ctx.guild)
		await ctx.send(f'Synced {len(fmt)} commands.')

	# @commands.command()
	# async def hello(self, ctx):
	# 	await interaction.response.send_message("I am here I am seen I am synced")

	
async def setup(bot):
		await bot.add_cog(Suggestion(bot))


		

