'''
HERE ARE ALL IMPORTS NEEDED FOR COGS
'''
import nextcord
import mysql.connector
import asyncio
import time
import random
import requests
import json
import re
import pytz
import os
from nextcord.ext import commands, tasks, slash_commands
from nextcord.ui import View, Select
from datetime import datetime, timedelta, timezone

"""
Constants takes variables from constants.py in Pebblehost and uses that.
"""
from constants import *
from constVariables import *
from bot import db, cursor

'''
General commands cog
'''
class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def praise(self, ctx, member: nextcord.Member = None):
        if member is None:
          await ctx.send("Please ping the user you would like to praise!")
        else:
          message_index = random.randint(1, 9)
          messages = {
                  1: f"{member.mention}, you look so good right now.",
                  2: f"{member.mention}, I love you.",
                  3: f"{member.mention}, you deserve a gold star.",
                  4: f"{member.mention}, youre quite the gem, a lovely one at that.",
                  5: f"{member.mention}, you always brighten my day.",
                  6: f"{member.mention}, good job kitten.",
                  7: f"womp womp {member.mention}, no praise for you :(",
                  8: f"{member.mention}, you can be my skibidi rizzler.",
                  9: f"{member.mention}, I would choose you in a garden of roses.",
            }
          await ctx.send(messages[message_index])

    @commands.slash_command(name="ping", description="Ping the bot")
    async def ping(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Shut the fuck up")

def setup(bot):
    bot.add_cog(GeneralCog(bot))
