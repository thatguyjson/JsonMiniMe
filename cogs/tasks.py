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
            # Calculate current Pacific Time (PST or PDT)
            utc_now = datetime.utcnow()
            pacific_offset = timedelta(hours=-8 if utc_now.timetuple().tm_isdst == 0 else -7)  # Adjust for DST
            pacific_time = utc_now + pacific_offset
    
            # Check if it's exactly 6:00 AM PST
            if pacific_time.hour == 6 and pacific_time.minute == 0:
                # Fetch a random question from the 'christmas' table
                cursor.execute("SELECT question FROM christmas ORDER BY RAND() LIMIT 1")
                question = cursor.fetchone()
    
                if not question:
                    # If no questions in 'christmas', fallback to 'QuotesDB'
                    cursor.execute("SELECT Quotes FROM QuotesDB ORDER BY RAND() LIMIT 1")
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
                        if "christmas" in question:
                            cursor.execute("DELETE FROM christmas WHERE question = %s", (question_text,))
                        else:
                            cursor.execute("INSERT INTO UsedQuotesDB (UsedQuotes) VALUES (%s)", (question_text,))
                            cursor.execute("DELETE FROM QuotesDB WHERE Quotes = %s", (question_text,))
                        
                        db.commit()
                else:
                    # Log if no questions are left in both tables
                    await log_to_channel(
                        "<@639904427624628224> URGENT!!! No questions left in both 'christmas' and 'QuotesDB' tables!"
                    )
            else:
                # Sleep asynchronously until the next minute
                await asyncio.sleep(60)
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

def setup(bot):
    bot.add_cog(TasksCog(bot))
