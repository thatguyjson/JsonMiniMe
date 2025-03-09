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
Database commands cog -> Will hold any commands that alter the DB in some major way.
'''
class DBCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def createuser(self, ctx):
        if ctx.channel.id != 1343127549861167135:
            await ctx.send("Please go to <#1343127549861167135> to create your profile!")
            return
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        user_discord_id = ctx.author.id # grabs the users ID
        user_name = ctx.author.name # grabs the users discord name
        user_joined_at = str(ctx.author.joined_at)[:19] # grabs when the user joined the server // example data: 2021-05-01 12:34:56
        user_created_at = str(ctx.author.created_at)[:19] # grabs when the user created their account // example data: 2021-05-01 12:34:56
    
        # Blocks if the user already has a profile
        cursor.execute("SELECT 1 FROM Users WHERE user_discord_id = %s", (user_discord_id,))
        userCheck = cursor.fetchone()  # Fetch the first result
        if userCheck:
            await ctx.send(f'Hey <@{user_discord_id}>! You already have a profile. Please don\'t try creating more!')
            return
    
        
        # User_gender grab
        while True:
            await ctx.send("Please enter your gender (Male, Female, M,  F, NB, or NonBinary):")
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=60)
                user_gender = msg.content.lower()
                if user_gender not in ["male", "female", "m", "f", "nb", "nonbinary"]:
                    await ctx.send("Invalid input. Please enter Male, Female, M,  F, NB, or NonBinary")
                    continue  # Repeat the loop if input is invalid
                if user_gender == "m":
                    user_gender = "male"
                elif user_gender == "f":
                    user_gender = "female"
                elif user_gender == "nb" or user_gender == "nonbinary":
                    user_gender == "Non-Binary"
    
                await ctx.send(f"Gender set to: {user_gender.capitalize()} ✅")
                break  # Exit the loop if input is valid
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond! ❌")
                return
    
        # user_pronouns grab
        while True:
            await ctx.send(
                "Please enter the number corresponding to your pronouns:\n"
                "1️⃣ - He/Him\n"
                "2️⃣ - She/Her\n"
                "3️⃣ - He/They\n"
                "4️⃣ - She/They\n"
                "5️⃣ - They/Them"
            )
        
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=60)
                pronoun_choices = {"1": "He/Him", "2": "She/Her", "3": "He/They", "4": "She/They", "5": "They/Them"}
                
                if msg.content not in pronoun_choices:
                    await ctx.send("Invalid input. Please enter 1, 2, 3, 4, or 5.")
                    continue
        
                user_pronouns = pronoun_choices[msg.content]
                await ctx.send(f"Pronouns set to: {user_pronouns} ✅")
                break
        
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond! ❌")
                return
    
        # User_age grab
        while True:
            await ctx.send("Please respond with your age!")
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=60)
                if len(msg.content) > 2:
                    await ctx.send("Please enter a valid age.")
                    continue
                user_age = msg.content
                user_age = int(user_age)
                await ctx.send(f"Set your age to {user_age}!")
                break
        
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond! ❌")
                return
    
        
        # User_date_of_birth grab
        while True:
            await ctx.send("Please enter your date of birth in the format YYYY-MM-DD:")
        
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=60)
                date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        
                if not re.match(date_pattern, msg.content):
                    await ctx.send("Invalid format! Please enter your date of birth in YYYY-MM-DD format (e.g., 2000-05-15).")
                    continue
        
                user_date_of_birth = msg.content
                await ctx.send(f"Date of birth set to: {user_date_of_birth} ✅")
                break
        
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond! ❌")
                return
    
        
        try:
            print(f"DEBUG: {user_discord_id}, {user_name}, {user_gender}, {user_pronouns}, {user_age}, {user_date_of_birth}, {user_joined_at}, {user_created_at}")
            cursor.execute(
                """
                INSERT INTO Users (user_discord_id, user_name, user_gender, user_pronouns, user_age, user_date_of_birth, user_joined_at, user_created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (user_discord_id, user_name, user_gender, user_pronouns, user_age, user_date_of_birth, user_joined_at, user_created_at),
            )
    
    
            db.commit()
            await ctx.send("User data successfully saved to the database! ✅")
    
        except Exception as e:
            await ctx.send(f"An error occurred while saving your data: {e}")
    
    @commands.command()
    async def updateuser(self, ctx):
        if ctx.channel.id != 1343127549861167135:
            await ctx.send("Please use <#1343127549861167135> for all commands related to user profiles!")
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        member = ctx.author.id
        # Blocks if the user if they dont have a profile
        cursor.execute("SELECT 1 FROM Users WHERE user_discord_id = %s", (member,))
        userCheck = cursor.fetchone()  # Fetch the first result
        if userCheck == None:
            await ctx.send(f'Hey <@{member}>! You dont have a profile. Please make one using ?createuser')
            return
        await ctx.send(
                f'Hey <@{member}>! What would you like to change about your profile?\n'
                "1️⃣ - Gender\n"
                "2️⃣ - Pronouns\n"
                "3️⃣ - Age\n"
                "4️⃣ - Birthday\n"
                "5️⃣ - Add a Profile Bio!"
            )
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60)
            if msg.content == "1":
                while True:
                    await ctx.send("Please enter your preferred gender (Male, Female, M,  F, NB, or NonBinary):")
                    try:
                        msg = await self.bot.wait_for("message", check=check, timeout=60)
                        user_gender = msg.content.lower()
                        if user_gender not in ["male", "female", "m", "f", "nb", "nonbinary"]:
                            await ctx.send("Invalid input. Please enter Male, Female, M,  F, NB, or NonBinary")
                            continue  # Repeat the loop if input is invalid
                        if user_gender == "m":
                            user_gender = "male"
                        elif user_gender == "f":
                            user_gender = "female"
                        elif user_gender == "nb" or user_gender == "nonbinary":
                            user_gender == "Non-Binary"
                            await ctx.send(f"Gender set to: {user_gender.capitalize()} ✅")
                            break
            
                        await ctx.send(f"Gender set to: {user_gender.capitalize()} ✅")
                        break  # Exit the loop if input is valid
                    except asyncio.TimeoutError:
                        await ctx.send("You took too long to respond! ❌")
                        return
                try:
                    cursor.execute(
                        """
                        UPDATE Users
                        SET user_gender = %s
                        WHERE user_discord_id = %s
                        """,
                        (user_gender, member),
                    )
                    db.commit()
                    await ctx.send("User data successfully saved to the database! ✅")
            
                except Exception as e:
                    await ctx.send(f"An error occurred while saving your data: {e}")
            elif msg.content == "2":
                while True:
                    await ctx.send(
                        "Please enter the number corresponding to your pronouns:\n"
                        "1️⃣ - He/Him\n"
                        "2️⃣ - She/Her\n"
                        "3️⃣ - He/They\n"
                        "4️⃣ - She/They\n"
                        "5️⃣ - They/Them"
                    )
                
                    try:
                        msg = await self.bot.wait_for("message", check=check, timeout=60)
                        pronoun_choices = {"1": "He/Him", "2": "She/Her", "3": "He/They", "4": "She/They", "5": "They/Them"}
                        
                        if msg.content not in pronoun_choices:
                            await ctx.send("Invalid input. Please enter 1, 2, 3, 4, or 5.")
                            continue
                
                        user_pronouns = pronoun_choices[msg.content]
                        await ctx.send(f"Pronouns set to: {user_pronouns} ✅")
                        break
                
                    except asyncio.TimeoutError:
                        await ctx.send("You took too long to respond! ❌")
                        return
                try:
                    cursor.execute(
                        """
                        UPDATE Users
                        SET user_pronouns = %s
                        WHERE user_discord_id = %s
                        """,
                        (user_pronouns, member),
                    )
                    db.commit()
                    await ctx.send("User data successfully saved to the database! ✅")
            
                except Exception as e:
                    await ctx.send(f"An error occurred while saving your data: {e}")
            elif msg.content == "3":
                while True:
                    await ctx.send("Please respond with your age!")
                    try:
                        msg = await self.bot.wait_for("message", check=check, timeout=60)
                        if len(msg.content) > 2:
                            await ctx.send("Please enter a valid age.")
                            continue
                        user_age = msg.content
                        user_age = int(user_age)
                        await ctx.send(f"Set your age to {user_age}!")
                        break
                
                    except asyncio.TimeoutError:
                        await ctx.send("You took too long to respond! ❌")
                        return
                try:
                    cursor.execute(
                        """
                        UPDATE Users
                        SET user_age = %s
                        WHERE user_discord_id = %s
                        """,
                        (user_age, member),
                    )
                    db.commit()
                    await ctx.send("User data successfully saved to the database! ✅")
            
                except Exception as e:
                    await ctx.send(f"An error occurred while saving your data: {e}")
            elif msg.content == "4":
                while True:
                    await ctx.send("Please enter your date of birth in the format YYYY-MM-DD:")
                    try:
                        msg = await self.bot.wait_for("message", check=check, timeout=60)
                        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
                
                        if not re.match(date_pattern, msg.content):
                            await ctx.send("Invalid format! Please enter your date of birth in YYYY-MM-DD format (e.g., 2000-05-15).")
                            continue
                
                        user_date_of_birth = msg.content
                        await ctx.send(f"Date of birth set to: {user_date_of_birth} ✅")
                        break
                
                    except asyncio.TimeoutError:
                        await ctx.send("You took too long to respond! ❌")
                        return
                try:
                    cursor.execute(
                        """
                        UPDATE Users
                        SET user_date_of_birth = %s
                        WHERE user_discord_id = %s
                        """,
                        (user_date_of_birth, member),
                    )
                    db.commit()
                    await ctx.send("User data successfully saved to the database! ✅")
            
                except Exception as e:
                    await ctx.send(f"An error occurred while saving your data: {e}")
            elif msg.content == "5":
                while True:
                    await ctx.send("Please enter a bio! (Max 255 characters)")
                    try:
                        msg = await self.bot.wait_for("message", check=check, timeout=180)
                        if len(msg.content) > 255:
                            await ctx.send(f'HEY! <@{member}> I SAID ONLY 255 CHARACTERS MAX!!!')
                            continue
                        user_bio = str(msg.content)
                        await ctx.send("I added/updated your profiles BIO! Thanks!")
                        break
                    except asyncio.TimeoutError:
                        await ctx.send("You took too long to respond! ❌")
                        return
                try:
                    cursor.execute(
                        """
                        UPDATE Users
                        SET user_bio = %s
                        WHERE user_discord_id = %s
                        """,
                        (user_bio, member),
                    )
                    db.commit()
                    await ctx.send("User data successfully saved to the database! ✅")
            
                except Exception as e:
                    await ctx.send(f"An error occurred while saving your data: {e}")
        except:
            await ctx.send("You didnt enter a correct value... Please try running the command again...")
            return
    
    @commands.command()
    async def aboutme(ctx):
        if ctx.channel.id != 1343127549861167135:
            await ctx.send(f"Please use <#1343127549861167135> and not <#{ctx.channel.id}>!")
        user_discord_id = ctx.author.id
        cursor.execute("SELECT 1 FROM Users WHERE user_discord_id = %s", (user_discord_id,))
        userCheck = cursor.fetchone()  # Fetch the first result
        if userCheck is None:
            await ctx.send(f'Hey <@{user_discord_id}>! You don\'t seem to have a profile. Please try making one using ?createuser')
            return
    
        name = ctx.author.nick
        if name == None:
            name = ctx.author.name
        
        # Fetching data for the profile
        cursor.execute("SELECT user_name, user_gender, user_pronouns, user_age, user_date_of_birth, user_bio, user_joined_at, user_created_at FROM Users WHERE user_discord_id = %s", (user_discord_id,))
        user_data = cursor.fetchone()
    
        if user_data is None:
            await ctx.send(f'Hey <@{user_discord_id}>! We encountered an issue retrieving your profile information.')
            return
        
        user_name, user_gender, user_pronouns, user_age, user_date_of_birth, user_bio, user_joined_at, user_created_at = user_data
        
        # Prepare the embed
        aboutMeEmbed = nextcord.Embed(
            title=f"Get to know {name}!",
            description=f"{name}'s Discord name is {user_name} and they were born on {user_date_of_birth}",
            color=0xff00ea
        )
        
        aboutMeEmbed.set_author(
            name=f"{name}'s About Me!",
            icon_url=str(ctx.author.avatar.url)
        )
        
        aboutMeEmbed.add_field(
            name=f"{name}'s Gender",
            value=f"{name} identifies as {user_gender}",
            inline=True
        )
        aboutMeEmbed.add_field(
            name=f"{name}'s Pronouns",
            value=f"{name} uses {user_pronouns} pronouns",
            inline=True
        )
        aboutMeEmbed.add_field(
            name=f"{name}'s Age",
            value=f"{name} is {user_age} years old",
            inline=True
        )
        aboutMeEmbed.add_field(
            name=f"{name}'s User Bio",
            value=user_bio or 'No bio set.',
            inline=False
        )
        aboutMeEmbed.add_field(
            name=f"{name}'s Server Join Date",
            value=f"{name} joined the server on {str(user_joined_at)[:10]}",
            inline=True
        )
        aboutMeEmbed.add_field(
            name=f"{name}'s Account Creation",
            value=f"{name} created their account on {str(user_created_at)[:10]}",
            inline=True
        )
        
        # Send the embed
        await ctx.send(embed=aboutMeEmbed)
    
    @commands.command()
    async def whois(ctx, member: nextcord.Member = None):
        if member == None:
            await ctx.send(f"Please @ a member when using this command like this! ?whois {dripMention}")
            return
        if ctx.channel.id != 1343127549861167135:
            await ctx.send(f"Please use <#1343127549861167135> and not <#{ctx.channel.id}>!")
            return
        user_discord_id = member.id
        cursor.execute("SELECT 1 FROM Users WHERE user_discord_id = %s", (user_discord_id,))
        userCheck = cursor.fetchone()  # Fetch the first result
        if userCheck is None:
            await ctx.send(f'Hey <@{ctx.author.id}>, it doesnt seem like <@{member.id}> has a profile. Please have them make one using ?createuser')
            return
    
        name = member.display_name
        
        # Fetching data for the profile
        cursor.execute("SELECT user_name, user_gender, user_pronouns, user_age, user_date_of_birth, user_bio, user_joined_at, user_created_at FROM Users WHERE user_discord_id = %s", (user_discord_id,))
        user_data = cursor.fetchone()
    
        if user_data is None:
            await ctx.send(f'Hey <@{user_discord_id}>! We encountered an issue retrieving your profile information.')
            return
        
        user_name, user_gender, user_pronouns, user_age, user_date_of_birth, user_bio, user_joined_at, user_created_at = user_data
        
        # Prepare the embed
        aboutMeEmbed = nextcord.Embed(
            title=f"Get to know {name}!",
            description=f"{name}'s Discord name is {user_name} and they were born on {user_date_of_birth}",
            color=0xff00ea
        )
        
        aboutMeEmbed.set_author(
            name=f"{name}'s About Me!",
            icon_url=str(member.display_avatar)
        )
        
        aboutMeEmbed.add_field(
            name=f"{name}'s Gender",
            value=f"{name} identifies as {user_gender}",
            inline=True
        )
        aboutMeEmbed.add_field(
            name=f"{name}'s Pronouns",
            value=f"{name} uses {user_pronouns} pronouns",
            inline=True
        )
        aboutMeEmbed.add_field(
            name=f"{name}'s Age",
            value=f"{name} is {user_age} years old",
            inline=True
        )
        aboutMeEmbed.add_field(
            name=f"{name}'s User Bio",
            value=user_bio or 'No bio set.',
            inline=False
        )
        aboutMeEmbed.add_field(
            name=f"{name}'s Server Join Date",
            value=f"{name} joined the server on {str(user_joined_at)[:10]}",
            inline=True
        )
        aboutMeEmbed.add_field(
            name=f"{name}'s Account Creation",
            value=f"{name} created their account on {str(user_created_at)[:10]}",
            inline=True
        )
        
        # Send the embed
        await ctx.send(embed=aboutMeEmbed)

def setup(bot):
    bot.add_cog(DBCog(bot))
