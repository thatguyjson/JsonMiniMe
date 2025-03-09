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
from bot import db, cursor

'''
Tasks cog
'''
class TasksCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=1)
    async def qotd_task(self):
        """
        Task to send the Question of the Day (QOTD) at 6 AM PST daily.
        """
        try:
            pacific = pytz.timezone("US/Pacific")
            pacific_time = datetime.now(pacific)
    
            # Check if it's exactly 6:00 AM PST
            if pacific_time.hour == 6 and pacific_time.minute == 0:
                # Fetch a random question from the 'christmas' table
                cursor.execute("SELECT quotes FROM QuotesDB ORDER BY RAND() LIMIT 1")
                question = cursor.fetchone()
    
                if question:
                    question_text = question[0]  # Extract question text
    
                    # Send the QOTD to the specified channel
                    qotd_channel = bot.get_channel(QOTD_CHANNEL_ID)
                    if qotd_channel:
                        await qotd_channel.send(
                            "@everyone\n🌟 **Question of the Day** 🌟\n{}".format(question_text)
                        )

                        # Move the used question to the appropriate table
                        cursor.execute("INSERT INTO UsedQuotesDB (UsedQuotes) VALUES (%s)", (question_text,))
                        cursor.execute("DELETE FROM QuotesDB WHERE Quotes = %s", (question_text,))
                        db.commit()
                else:
                    # Log if no questions are left in both tables
                    await log_to_channel(
                        "<@639904427624628224> URGENT!!! No questions left in 'QuotesDB' table!"
                    )
                    
        except Exception as e:
            # Log errors for debugging
            await log_to_channel(f"Error in QOTD task: {e}")
    
    
    @tasks.loop(hours=3)
    async def keep_connection_alive(self):
        cursor.execute("SELECT UsedQuotes FROM UsedQuotesDB where id = 3")
        aliveQuote = cursor.fetchone()
        if aliveQuote:
          debug_channel = self.bot.get_channel(1307966892853432391)
          if debug_channel:
            await debug_channel.send(aliveQuote)

    @tasks.loop(minutes=1)
    async def check_github_releases(self):
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        headers = {"Accept": "application/vnd.github.v3+json"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            release = response.json()
            release_id = release["id"]
            
            if LAST_RELEASE is None:
                LAST_RELEASE = release_id  # Initialize on first run
                return
    
            if release_id != LAST_RELEASE:
                LAST_RELEASE = release_id
                title = release["name"]
                url = release["html_url"]
                message = f"🚀 New release: [{title}]({url})!"
    
                channel = bot.get_channel(CHANNEL_ID)
                if channel:
                    await channel.send(message)

def setup(bot):
    bot.add_cog(TasksCog(bot))
