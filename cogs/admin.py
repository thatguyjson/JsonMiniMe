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
def owner shit
'''
async def is_owner(ctx):
    role = nextcord.utils.get(ctx.guild.roles, name=ROLE_NAME)
    return role in ctx.author.roles

async def is_drip(ctx):
    return ctx.author.id == 639904427624628224

'''
Admin commands cog
'''
class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_owner)
    async def add_question(self, ctx, *, question=None):
        if question:
          sql = "INSERT INTO QuotesDB (quotes) VALUES (%s)"
          val = (question,)
          cursor.execute(sql, val)
          db.commit()  # Save the changes to the database
          await ctx.send(f"Question added: {question}")
        else:
          await ctx.send("Please include a question in this format. ?add_question <Question>")

    @commands.command()
    @commands.check(is_owner)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: nextcord.Member = None, *, reason=None):
        if user == None:
            await ctx.send("Please enter a user!")
            return
    
        await user.kick(reason=reason)
        await ctx.send(f'Kicked {user.name} for reason: {reason}')
    
    @commands.command()
    @commands.check(is_owner)
    @commands.has_permissions(ban_members=True)
    async def evict(self, ctx, user: nextcord.Member = None, *, reason=None):
        if user == None:
            await ctx.send("Please enter a user!")
            return
    
        await user.ban(reason=reason)
        await ctx.send(f'Banned {user.name} for reason: {reason}')

    @commands.command()
    @commands.check(is_drip)
    async def add_dob(self, ctx, member: nextcord.Member = None, dob: str = None):
        if member == None: # If member wasnt mentioned, dont continue command
            await ctx.send("Please mention a user in order to use this command!")
            return
        if dob == None: # If dob wasnt mentioned, dont continue command
            await ctx.send("Please enter a DOB in this format: YYYY-MM-DD")
            return
        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
        except ValueError:
            await ctx.send("Invalid date format! Please use YYYY-MM-DD.")
            return
        user_id = member.id
        user_dob = dob_date
        try:
            cursor.execute(
                """
                INSERT INTO HardCodedDOBs (user_id, user_dob)
                VALUES (%s, %s)
                """,
                (user_id, user_dob),
            )
            db.commit()
            await ctx.send("User data successfully saved to the database! ✅")
        except Exception as e:
            await ctx.send(f"An error occurred while saving your data: {e}")
    
    @commands.command()
    @commands.check(is_owner)
    async def sql(self, ctx, *, query: str = None):
        if query == None:
            await ctx.send("Please input a query you want to run.")
            return
        try: 
            cursor.execute(f'{query};')
            if 'select' in query.lower():
                selected_data = cursor.fetchall()
                formatted_data = "\n".join([str(row) for row in selected_data])
                await ctx.send(f"**Query Results:**\n{formatted_data}")
                return
            else:
                db.commit()
                await ctx.send(f"Succesfully ran: ```\n{query}\n```")
        except Exception as e:
            # Catch any other unexpected errors
            await ctx.send(f"An unexpected error occurred: {str(e)}")

    @commands.command()
    @commands.check(is_owner)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        if amount <= 0:
            await ctx.send("Please specify a positive number of messages to delete.", delete_after=5)
            return
    
        try:
            deleted = await ctx.channel.purge(limit=amount + 1)
            confirmation = await ctx.send(f"✅ Deleted {len(deleted)} messages.", delete_after=5)
        except nextcord.Forbidden:
            await ctx.send("❌ I don't have permission to delete messages in this channel.", delete_after=5)
        except nextcord.HTTPException as e:
            await ctx.send(f"❌ An error occurred: {e}", delete_after=5)
    
    
    @commands.command()
    @commands.check(is_drip)
    async def restart(self, ctx):
        if ctx.author.id != dripID:
            await ctx.send(f"Please dont use this command unless youre {dripMention}! Thanks!")
            return
            
        close_message = await ctx.send("Restarting Bot, Please wait")
        for i in range(1, 4):
            await close_message.edit(content=f"Restarting Bot, Please wait{'.' * i}")
            time.sleep(0.5)
        await self.bot.close()

    @commands.command()
    @commands.check(is_drip)
    async def newrelease(self, ctx):
        
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        await ctx.send(f"Good job on the new release <@{ctx.author.id}>! Can you please provide the name of the release?")
        try:
            RNmsg = await self.bot.wait_for("message", check=check, timeout=60)
            release_name = RNmsg.content
            await ctx.send(f"Gotcha, the release name is {release_name}!")
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond! ❌")
            return

        
        await ctx.send(f"Thank you for that <@{ctx.author.id}>! Can you please provide the version in this format? v0.0.0")
        try:
            RVmsg = await self.bot.wait_for("message", check=check, timeout=60)
            release_version = RVmsg.content
            await ctx.send(f"Gotcha, the release version is {release_version}!")
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond! ❌")
            return

        await ctx.send(f"Amazing! Lastly, can you please provide me with the Release link?")
        try:
            RLmsg = await self.bot.wait_for("message", check=check, timeout=60)
            release_link = RLmsg.content
            await ctx.send(f"Thank you! Thats all I need!")
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond! ❌")
            return
        
        draft_message = await ctx.send("Drafting message and sending in <#1299230549789118526>")
        for i in range(1, 4):
            await draft_message.edit(content=f"Drafting message and sending in <#1299230549789118526>{'.' * i}")
            time.sleep(0.5)

        channel = self.bot.get_channel(BOT_CHANGELOG_CHANNEL_ID)
        await channel.send(f'''
||@everyone||

# 🚀  __**New Release just dropped! See it below!**__
-# Sent by <@{ctx.author.id}> ~ Thanks :3


### *Release Info:*
- Release Name: `{release_name}`
- Release Version: `{release_version}`

### *See the full release down below! Thank you!!*
[Click Me For The Release!]({release_link})
''')

def setup(bot):
    bot.add_cog(AdminCog(bot))
