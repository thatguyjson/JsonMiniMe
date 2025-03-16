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
        welcomeChannel = self.bot.get_channel(welcomeChannel_ID)
        if welcomeChannel is not None:
            message_index = random.randint(1, 40)
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
                11: f"Hey {str(member.mention)} if you were a vegetable, you'd be a cute-cumber.",
                12: f"{str(member.mention)}’s smile could light up the entire server. Like seriously.",
                13: f"Hold up, did {str(member.mention)} just walk into the room and raise the temperature?",
                14: f"Welcome {str(member.mention)}, you just added 100% more charm to the server.",
                15: f"Is it just me, or did the server just get 10x cooler the moment {str(member.mention)} showed up?",
                16: f"{str(member.mention)}’s aura is so bright, I need shades just to look at them",
                17: f"Did someone call for a showstopper? {str(member.mention)} has arrived, people.",
                18: f"Hey {str(member.mention)}, are you a magician? Because every time you’re around, everything else disappears.",
                19: f"Just in: {str(member.mention)} is here to steal hearts and look fabulous while doing it.",
                20: f"Looking at {str(member.mention)} right now... I’m convinced they just broke the scale for 'attractive'.",
                21: f"Watch out, {str(member.mention)} just entered the server and instantly made it 10x more stylish.",
                22: f"{str(member.mention)} is proof that beauty can be both stunning and effortless.",
                23: f"Okay, but {str(member.mention)} is literally out here redefining what 'gorgeous' means.",
                24: f"{str(member.mention)} walked in like they owned the place, and honestly... they do.",
                25: f"Is it just me, or did the vibe get way cooler the moment {str(member.mention)} joined?",
                26: f"That moment when {str(member.mention)} joined and made the server sparkle ✨",
                27: f"Welcome to the server, {str(member.mention)}! I’m pretty sure you just made the atmosphere 100% more magnetic.",
                28: f"{str(member.mention)}’s glow is so bright, I might need to put on sunglasses inside.",
                29: f"Attention, everyone: {str(member.mention)} has arrived, and with them, a whole new level of elegance.",
                30: f"Hey {str(member.mention)}, are you a comet? Because you just rocketed to the top of my 'cool people' list.",
                31: f"Did {str(member.mention)} just walk in or did the whole server just get a major glow-up?",
                32: f"Hold on, is {str(member.mention)} secretly a model? Because they just *slayed* this entrance.",
                33: f"How do you do it, {str(member.mention)}? Look this good and still manage to stay humble?",
                34: f"Did {str(member.mention)} just set the bar for how to make an entrance? Because that was iconic.",
                35: f"{str(member.mention)} is here, and it's like the whole server just leveled up in style.",
                36: f"Welcome {str(member.mention)}! The only thing more stunning than your entrance is your vibe.",
                37: f"Hey {str(member.mention)}, is there a secret to being this fabulous, or were you just born this way?",
                38: f"I thought I knew what charm looked like until {str(member.mention)} showed up.",
                39: f"Don’t mind me, I’m just sitting here trying to figure out how {str(member.mention)} manages to look this good all the time.",
                40: f"Let's be real, {str(member.mention)} is here to make us all look a little less fabulous in comparison",
}
            welcome_message = messages[message_index]
            await welcomeChannel.send(welcome_message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
    
        if member is None or guild is None:
            return
        if payload.user_id == 1280817864357445663:
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

        elif payload.message_id == message_ids.get('bot_changelog_message_id') and str(payload.emoji) == BotChangelogRole:
            role = nextcord.utils.get(guild.roles, name=BotChangelogName)
            if role is not None:
                await member.add_roles(role)
                await log_to_channel(f"Assigned {BotChangelogName} to {member.display_name}")
                
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
        if payload.user_id == 1280817864357445663:
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

        elif payload.message_id == message_ids.get('bot_changelog_message_id') and str(payload.emoji) == BotChangelogRole:
            role = nextcord.utils.get(guild.roles, name=BotChangelogName)
            if role is not None:
                await member.remove_roles(role)
                await log_to_channel(f"Removed {BotChangelogName} from {member.display_name}")
                
        elif payload.message_id == message_ids.get('color_message_id'):
            for role_name, emoji in color_role.values():
                if str(payload.emoji) == emoji:
                    role = nextcord.utils.get(guild.roles, name=role_name)
                    if role:
                        await member.remove_roles(role)
                        await log_to_channel(f"Removed {role_name} from {member.display_name}")
                    break

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        
        staff_channel = self.bot.get_channel(STAFF_CHANNEL_ID)
        if staff_channel:
            embed = nextcord.Embed(title="Message Deleted", color=nextcord.Color.red())
            embed.add_field(name="User", value=message.author.name, inline=True)
            embed.add_field(name="Channel", value=message.channel.name, inline=True)
            embed.add_field(name="Content", value=message.content or "No content", inline=False)
            await staff_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: # checks if the msg is sent by bot ; if it is, it ignores
            return
        
        msg_channel_id = message.channel.id # grab channel id as a variable
        msg_channel = self.bot.get_channel(msg_channel_id) # grab channel using id variable
        msg = message.content # grab the listened msg as a variable to use
        if msg_channel_id == TO_DO_CHANNEL_ID:
            bot_msg_1 = await msg_channel.send('Adding your message as a task.')
            time.sleep(1)
            task_msg = await msg_channel.send(msg)
            await task_msg.add_reaction(remove_task_emoji)
            await bot_msg_1.delete()
        
        else:
            return

def setup(bot):
    bot.add_cog(EventsCog(bot))
