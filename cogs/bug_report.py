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
import os
import traceback
import json

class Json_Handler():
    def __init__(self):
        self.json_path = './files/bug_reports.json'


    def save_entry(self, entry):
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

    def save(self):
        savedata = {
            'entries': self._entries,
            'next_index': self._next_index,
            'labels': self._labels,
            'complexities': self._complexities,
            'priorities': self._priorities,
            'notifications_disabled': list(self._notifications_disabled),
        }

        with open(self._database_path, 'w') as f:
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
            #potentially a problem line here
            self.save()
            #print("Initialized new {} database".format(self._descriptor_single), flush=True)
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

            # print("Loaded {} database".format(self._descriptor_single), flush=True)

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


    def add_entry(self, description, labels=["misc"], author=None, image=None, priority="N/A", complexity="unknown"):
        entry = {
            "description": description,
            "labels": labels,
        }

        if author is None:
            entry["author"] = 0
        else:
            entry["author"] = author.id

        if image is not None:
            entry["image"] = image

        entry["priority"] = priority
        entry["complexity"] = complexity
        entry["pending_notification"] = False

        index = self._next_index

        self._next_index += 1
        self._entries[str(index)] = entry

        self.save()

        return (index, entry)


class Bug_Report(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        json_handler = Json_Handler()
        json_handler.load()
        print('Bug report\'s json handler loaded')




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
    @app_commands.describe(label='Pick the label that best describes this bug-')
    @app_commands.choices(label=[
        discord.app_commands.Choice(name='misc', value=1),
        discord.app_commands.Choice(name='advancement', value=2),
        discord.app_commands.Choice(name='boss', value=3),
        discord.app_commands.Choice(name='build', value=4),
        discord.app_commands.Choice(name='class', value=5),
        discord.app_commands.Choice(name='cmd', value=6),
        discord.app_commands.Choice(name='delve', value=7),
        discord.app_commands.Choice(name='depths', value=8),
        discord.app_commands.Choice(name='discord', value=9),
        discord.app_commands.Choice(name='enchantment', value=10),
        discord.app_commands.Choice(name='gui', value=11),
        discord.app_commands.Choice(name='item', value=12),
        discord.app_commands.Choice(name='mob', value=13),
        discord.app_commands.Choice(name='npc', value=14),
        discord.app_commands.Choice(name='plugin', value=15),
        discord.app_commands.Choice(name='quest', value=16),
        discord.app_commands.Choice(name='server', value=17),
        discord.app_commands.Choice(name='website', value=18),

            ])
    async def bugreport(self, interaction: discord.Interaction, 
        label: discord.app_commands.Choice[int], description: str, file: discord.Attachment=None, ):

        #concerns: pinging users (labeling covered the slash command)

        bug_embed = discord.Embed(title = label.name, 
            description= description, 
            color = discord.Color.purple())

        bug_embed.set_author(name=interaction.user.display_name, icon_url= interaction.user.avatar)
        
        # next line breaks the code: have tried it with / without the if file != None (required it in async def bugreport)
        if file != None:
            bug_embed.set_image(interaction.message.attachments[0].url)


        #do some more checks, but then call add_entry(self, description, 
        #   labels=["misc"], author=None, image=None, priority="N/A", complexity="unknown"):

        # index, entry = json_handler.add_entry(description=description, labels=label.name, author=interaction.user.name)
        # #and save it with save_entry(self, entry, next_index, labels, complexities, priorities, notifications_disabled):
        # json_handler.save_entry(entry=entry, next_index=index, labels=label.name, complexities="unknown", priorities="N/A", notifications_disabled=False)


        await interaction.response.send_message(embed=bug_embed)

    @app_commands.command(name=assignComplexity, description="Assign the complexity of a bug")
    @app_commands.describe(complexity='Complexity- if unknown, select unknown')
    @app_commands.choices(complexity=[
        discord.app_commands.Choice(name='easy', value=1),
        discord.app_commands.Choice(name='moderate', value=2),
        discord.app_commands.Choice(name='hard', value=3),
        discord.app_commands.Choice(name='unknown', value=4)
        ])
    async def assignComplexity(self, interaction: discord.Interaction, 
        bugNumber = int, complexity:discord.app_commands.Choice[int]):

        #get the bug, reassign the complexity, save it, send it
        bug_embed = discord.Embed(title = "temp", 
            description= bugNumber, 
            color = discord.Color.pink())
        await interaction.response.send_message(embed=bug_embed)

    @app_commands.command(name=assignPriority, description="Assign the priority of a bug")
    @app_commands.describe(priority='Priority- if unknown, select N/A')
    @app_commands.choices(priority=[
        discord.app_commands.Choice(name='Critical', value=1),
        discord.app_commands.Choice(name='High', value=2),
        discord.app_commands.Choice(name='Medium', value=3),
        discord.app_commands.Choice(name='Low', value=4),
        discord.app_commands.Choice(name='Zero', value=4),
        discord.app_commands.Choice(name='N/A', value=5)
        ])
    async def assignPriority(self, interaction: discord.Interaction, 
        bugNumber = int, priority:discord.app_commands.Choice[int]):

        #get the bug, reassign the priority, save it, send it
        index, entry = json_handler.get_entry(bugNumber)
        entry["priority"] = priotity.name



        bug_embed = discord.Embed(title = "temp", 
            description= bugNumber, 
            color = discord.Color.white())
        await interaction.response.send_message(embed=bug_embed)


#setting up cog for the bot: will need to adjust for which discord servers get passed into guilds
async def setup(bot):
    await bot.add_cog(Bug_Report(bot), guilds=[discord.Object(id=config.GUILD_ID)])