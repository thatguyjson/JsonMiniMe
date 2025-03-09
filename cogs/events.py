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
from nextcord.ext import commands, tasks
from nextcord.ui import View, Select
from datetime import datetime, timedelta, timezone

"""
Constants takes variables from constants.py in Pebblehost and uses that.
"""
from constants import *
from constVariables import *

'''
Events cog
'''
class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




def setup(bot):
    bot.add_cog(EventsCog(bot))
