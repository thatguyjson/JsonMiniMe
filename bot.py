'''
JsonMiniMe is a discord bot created using the Nextcord API Wrapper.
This was created by Jason, also known as @Drip___ on discord!
For any questions, feel free to add and dm me on discord "drip___"
'''

import nextcord
import mysql.connector
import asyncio
import time
import random
import requests
import json
import re
from nextcord.ext import commands, tasks
from nextcord.ui import View, Select
from datetime import datetime, timedelta, timezone

"""
Constants takes variables from constants.py in Pebblehost and uses that.
"""
from constants import botToken
from constants import DBhost, DBuser, DBpassword, DBdatabase, DBport
from constVariables import *

"""
these intents allow the bot to track member activity, read messages, monitor reactions,
receive server-level events, and listen to messages in guilds. All these are necessary for bot functionality
like moderation, command handling, and reacting to user input.
"""
intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.guild_messages = True

'''
commands.bot(command_prefix='', intents=intents), we are setting the prefix
that commands will run in discord itself. intents=intents is telling the bot
to use the intents we previously set to True above so that we can use it and
make the bot more versatile.
'''
bot = commands.Bot(command_prefix='?', intents=intents)

# this is used somewhere i think???
message_ids = {}
