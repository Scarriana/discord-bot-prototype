#@Scarriana#5999
#December 2022
#Monumenta Discord Task Bot Prototype: bug report cog
#contains the commands to make, edit, and remove bugs
#along with the json handling to save these actions

import discord
from discord.ext import commands
from discord import ui, app_commands
import config
import traceback
import os
import json


class Bug_Report(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._json_path = config.JSON_PATH_BUG

    def save(self, entry, next_index, labels, complexities, priorities, notifications_disabled):
        savedata = {
            'entries': entry,
            'next_index': next_index,
            'labels': labels,
            'complexities': complexities,
            'priorities': priorities,
            'notifications_disabled': list(notifications_disabled),
        }
        
        with open(self._json_path, 'w') as f:
            json.dump(savedata, f, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))
            
    def load(self):
        if not os.path.exists(self.json_path):
            self._entries = {}
            self._next_index = 1
            self._labels = [
                "misc",
            ]
            self._priorities = [
                "Critical",
                "High",
                "Medium",
                "Low",
                "Zero",
                "N/A",
            ]
            self._complexities = {
                "easy":     ":green_circle:",
                "moderate": ":orange_circle:",
                "hard":     ":red_circle:",
                "unknown":  ":white_circle:"
            }
            self._notifications_disabled = set([])
            self.save()
            print("Initialized new {} database".format(self._descriptor_single), flush=True)
        else:
            with open(self.json_path, 'r') as f:
                data = json.load(f)

            # Must exist
            self._entries = data['entries']
            self._next_index = data['next_index']

            # TODO: Scan through and add all labels
            if 'labels' in data:
                self._labels = data['labels']
            else:
                self._labels = [
                    "misc",
                ]
            if 'priorities' in data:
                self._priorities = data['priorities']
            else:
                self._priorities = [
                    "Critical",
                    "High",
                    "Medium",
                    "Low",
                    "Zero",
                    "N/A",
                ]

            if 'complexities' in data:
                self._complexities = data['complexities']
            else:
                self._complexities = {
                    "easy":     ":green_circle:",
                    "moderate": ":orange_circle:",
                    "hard":     ":red_circle:",
                    "unknown":  ":white_circle:"
                }

            self._notifications_disabled = set([])

            if 'notifications_disabled' in data:
                for author in data['notifications_disabled']:
                    self._notifications_disabled.add(int(author))

            changed = False
            for item_id in self._entries:
                entry = self._entries[item_id]
                if "pending_notification" not in entry:
                    entry["pending_notification"] = True
                    changed = True
                if "complexity" not in entry:
                    entry["complexity"] = "unknown"
                    changed = True

            if changed:
                self.save()

            print("Loaded {} database".format(self._descriptor_single), flush=True)

    def get_entry(self, index_str):
        """
        Gets an entry for a given string index number
        Throws ValueError if it does not exist or parsing fails
        """

        try:
            index = int(index_str)
        except:
            raise ValueError("{!r} is not a number".format(index_str))

        # json keys need to be strings, not numbers
        index = str(index)

        if index not in self._entries:
            raise ValueError('{proper} #{index} not found!'.format(proper=self._descriptor_proper, index=index))

        return index, self._entries[index]

    #sync bot: this is necessary, but also needs more than what I have now
    @commands.command()
    async def sync_report(self, ctx) -> None:
        await ctx.send('Syncing command recieved')
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f'Synced {len(fmt)} commands in bug_report.py')
    
    #on ready
    @commands.Cog.listener()
    async def on_ready(self):
        self.load()
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


    @app_commands.command(name='editbug', description='Enter a description of your bug. Game breaking or exploits bugs should be DM\'d to a moderator')
    async def editbug(self, interaction: discord.Interaction, 
        bugnumber: int, description: str):

        embed = discord.Embed(title = 'Bug Report', 
            description= description, 
            color = discord.Color.purple())
        # embed.set_author(name=interaction.user_url)
        # print(interaction.user + "\n")
        # report_embed = discord.Embed(title = 'Bug Report', 
        # 	description = description, 
        # 	color = discord.Color.purple())

        #embed.set_author(name=interaction.user, icon_url= interaction.user.avatar)

        # print("about to send the embed")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='removebug', description='Reject / Remove a bug (must have permissions or be the bug author)')
    async def removebug(self, interaction: discord.Interaction, 
        bugnumber: int, reason: str):

        embed = discord.Embed(title = 'Bug Report', 
            description= reason, 
            color = discord.Color.green())
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