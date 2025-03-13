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
forfun = commands.Bot(command_prefix='!', intents=intents)

# this is used somewhere i think???
message_ids = {}
cogs_folder = 'cogs'

"""
DB Connection below grabs all DB info related stuff in order to connect from Constants
"""
db = mysql.connector.connect(
    host=DBhost,
    user=DBuser,
    password=DBpassword,
    database=DBdatabase,
    port=DBport
)
cursor = db.cursor()

'''
async functions that im adding to run asap ig?
'''
async def is_owner(ctx):
    role = nextcord.utils.get(ctx.guild.roles, name=ROLE_NAME)
    return role in ctx.author.roles

async def is_drip(ctx):
    return ctx.author.id == 639904427624628224

async def log_to_channel(message):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        # grabs UTC
        utc_now = datetime.now(pytz.utc)
        # grabs PST
        pst_zone = pytz.timezone('US/Pacific')
        # makes pst_time in pst from UTC
        pst_time = utc_now.astimezone(pst_zone)
        # format the timestamp to Year-Month-Day Hour-Minute-Seconds
        timestamp = pst_time.strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"**[{timestamp}]** {message}"
        await log_channel.send(log_message)

for filename in os.listdir(cogs_folder):
        if filename.endswith('.py'):  # Only load Python files
            cog_name = f"cogs.{filename[:-3]}"  # Remove the .py extension
            try:
                bot.load_extension(cog_name)
                print(f"Loaded cog: {cog_name}")
            except Exception as e:
                print(f"Failed to load cog {cog_name}: {e}")

"""
down below is on_ready + bot.run
"""
@forfun.event
async def on_ready():
    global welcomeChannel
    welcomeChannel = bot.get_channel(1280813683789791305)
    if welcomeChannel is None:
        await log_to_channel("Could not find the welcome channel.")
    else:
        await log_to_channel(f'Logged in as {forfun.user.name}.')
    
@bot.event
async def on_ready():
    global welcomeChannel
    welcomeChannel = bot.get_channel(1280813683789791305)
    if welcomeChannel is None:
        await log_to_channel("Could not find the welcome channel.")
    else:
        await log_to_channel(f'Logged in as {bot.user.name}. Now commencing all startup processes.')

    # Verify Roles Message
    channel1 = bot.get_channel(1280805997790887978)
    if channel1 is not None:
        try:
            await channel1.purge(limit=100)  # Limit the number of messages to purge
            verify_message = await channel1.send("React with ✅ to become a Tenant!")
            await verify_message.add_reaction("✅")
            message_ids["verify_message_id"] = verify_message.id
            await log_to_channel("Verify role setup complete.")
        except Exception as e:
            await log_to_channel(f"Error setting up verify role: {e}")

    # Server Updates and Event Updates Messages
    channel2 = bot.get_channel(1299261004169089066)
    if channel2 is not None:
        try:
            await channel2.purge(limit=100)
            server_update_message = await channel2.send("React with ✨ to gain the Server Updates Role")
            await server_update_message.add_reaction("✨")
            event_update_message = await channel2.send("React with ☄️ to gain the Event Updates Role")
            await event_update_message.add_reaction("☄️")
            bot_changelog_message = await channel2.send("React with 🤖 to be notified of any Bot Changes")
            await bot_changelog_message.add_reaction("🤖")

            message_ids["server_update_message_id"] = server_update_message.id
            message_ids["event_update_message_id"] = event_update_message.id
            message_ids["bot_changelog_message_id"] = bot_changelog_message.id
            await log_to_channel("Server, Event, and Bot role setup is complete.")
        except Exception as e:
            await log_to_channel(f"Error setting up update roles: {e}")

    # Color Roles Message
    try:
        color_message = "\n".join([f"{emoji} - {role}" for role, emoji in color_role.values()])
        color_message_sent = await channel2.send(
            f"React to the image with the color you would like:\n**Available color roles:**\n{color_message}"
        )
        message_ids["color_message_id"] = color_message_sent.id

        for _, emoji in color_role.values():
            await color_message_sent.add_reaction(emoji)
    except Exception as e:
        await log_to_channel(f"Error setting up color roles: {e}")
    tasks_cog = bot.get_cog('TasksCog')
    tasks_cog.qotd_task.start()
    await log_to_channel('started QOTD')
    tasks_cog.keep_connection_alive.start()
    await log_to_channel('started DB connection')
    await log_to_channel(f'{dripMention} BOT IS SET UP AND READY TO GO!')

async def run_bots():
    task1 = asyncio.create_task(bot.start(botToken))
    task2 = asyncio.create_task(forfun.start(botToken2))

    await asyncio.gather(task1, task2)

if __name__ == "__main__":
    asyncio.run(run_bots())
