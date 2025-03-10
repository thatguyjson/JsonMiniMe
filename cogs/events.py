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
from bot import db, cursor, message_ids, log_to_channel

'''
Events cog
'''
class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if welcomeChannel is not None:
            message_index = random.randint(1, 11)
            messages = {
                1: f"DAMN {str(member.mention)} looks GOOD TODAY",
                2: f"{str(member.mention)} just joined! Hows it goin' cutie :3",
                3: f"{str(member.mention)} just fell from heaven. Oh how lucky we are",
                4: f"{str(member.mention)} looks absolutely stunning. Welcome!",
                5: f"{str(member.mention)} looks just like a dream, prettiest person we've ever seen",
                6: f"{str(member.mention)} has got to be the best looking person here :O",
                7: f"Hey {str(member.mention)}, whats cookin good lookin ; )",
                8: f"The way {str(member.mention)} joined the server. Very Demure. Very Mindful",
                9: f"{str(member.mention)} may look good, but can they handle this craziness? Welcome!",
                10: f"{str(member.mention)} are you https? Because without you, im ://",
                11: f"Hey {str(member.mention)} if you were a vegetable, you'd be a cute-cumber."
            }
            welcome_message = messages[message_index]
            await welcomeChannel.send(welcome_message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
    
        if member is None or guild is None:
            return
        if payload.user_id == 1280817864357445663: #checks if bot
            return
    
        if payload.message_id == message_ids.get('verify_message_id') and str(payload.emoji) == VerifyRole:
            role = nextcord.utils.get(guild.roles, name=VerifyName)
            if role is not None:
                await member.add_roles(role)
                await log_to_channel(f'Assigned {VerifyName} to {member.display_name}')
    
        elif payload.message_id == message_ids.get('server_update_message_id') and str(payload.emoji) == ServerUpdateRole:
            role = nextcord.utils.get(guild.roles, name=ServerUpdateName)
            if role is not None:
                await member.add_roles(role)
                await log_to_channel(f"Assigned {ServerUpdateName} to {member.display_name}")
    
        elif payload.message_id == message_ids.get('event_update_message_id') and str(payload.emoji) == EventUpdateRole:
            role = nextcord.utils.get(guild.roles, name=EventUpdateName)
            if role is not None:
                await member.add_roles(role)
                await log_to_channel(f"Assigned {EventUpdateName} to {member.display_name}")
        elif payload.message_id == message_ids.get('color_message_id'):
            for role_name, emoji in color_role.values():
                if str(payload.emoji) == emoji:
                    role = nextcord.utils.get(guild.roles, name=role_name)
                    if role:
                        await member.add_roles(role)
                        await log_to_channel(f"Assigned {role_name} to {member.display_name}")
                    break
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
    
        if member is None or guild is None:
            return
        if payload.user_id == 1280817864357445663: # checks if bot
            return
    
        if payload.message_id == message_ids.get('verify_message_id') and str(payload.emoji) == VerifyRole:
            role = nextcord.utils.get(guild.roles, name=VerifyName)
            if role is not None:
                await member.remove_roles(role)
                await log_to_channel(f'Removed {VerifyName} from {member.display_name}')
    
        elif payload.message_id == message_ids.get('server_update_message_id') and str(payload.emoji) == ServerUpdateRole:
            role = nextcord.utils.get(guild.roles, name=ServerUpdateName)
            if role is not None:
                await member.remove_roles(role)
                await log_to_channel(f"Removed {ServerUpdateName} from {member.display_name}")
    
        elif payload.message_id == message_ids.get('event_update_message_id') and str(payload.emoji) == EventUpdateRole:
            role = nextcord.utils.get(guild.roles, name=EventUpdateName)
            if role is not None:
                await member.remove_roles(role)
                await log_to_channel(f"Removed {EventUpdateName} from {member.display_name}")
        elif payload.message_id == message_ids.get('color_message_id'):
            for role_name, emoji in color_role.values():
                if str(payload.emoji) == emoji:
                    role = nextcord.utils.get(guild.roles, name=role_name)
                    if role:
                        await member.remove_roles(role)
                        await log_to_channel(f"Removed {role_name} from {member.display_name}")
                    break

    @commands.Cog.listener()
    async def on_message_delete(message):
        if message.author.self.bot:
            return
        
        staff_channel = self.bot.get_channel(STAFF_CHANNEL_ID)
        if staff_channel:
            embed = nextcord.Embed(title="Message Deleted", color=nextcord.Color.red())
            embed.add_field(name="User", value=message.author.name, inline=True)
            embed.add_field(name="Channel", value=message.channel.name, inline=True)
            embed.add_field(name="Content", value=message.content or "No content", inline=False)
            await staff_channel.send(embed=embed)



def setup(bot):
    bot.add_cog(EventsCog(bot))
