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
from bot import db, cursor, cursor_dict

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
                    qotd_channel = self.bot.get_channel(QOTD_CHANNEL_ID)
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

    @tasks.loop(minutes=5)
    async def refresh_to_do_list(self):
        cursor_dict.execute("SELECT * FROM TO_DO")
        tasks = cursor_dict.fetchall()
        task_message = "\n".join([f"{row['id']}: {row['task']}" for row in tasks])
        channel = self.bot.get_channel(TO_DO_CHANNEL_ID)
        await channel.purge(limit=100)
        if task_message:
            await channel.send("""
# Welcome to the TO_DO Channel! 

## In order to add a new task please use
`?newtask <task>`
### For example:
- ?newtask Buy cat litter from costco


## In order to complete a task, please use
`?completetask <id>`
### For example:
- ?completetask 2""")
            await channel.send(f"Here are the current outstanding tasks!\n{task_message}")
        else:
            await channel.send(f'{dripMention} there was an error i think...')
        

def setup(bot):
    bot.add_cog(TasksCog(bot))
