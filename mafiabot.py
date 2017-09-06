#!/usr/bin/python3

import discord, sys, asyncio
from discord.ext import commands

"""
This program is a discord bot, through which mafia can be played.
"""
 
BOT_PREFIX = '!'
BOT_DESCRIPTION = "Play mafia, with your friends, through discord."
JOIN_LENGTH = 10
NIGHT_LENGTH = 10
DAY_LENGTH = 20
 
bot = commands.Bot(command_prefix=BOT_PREFIX, description=BOT_DESCRIPTION)

class Villager():

    def __init__(self):
        pass


class Player():

    def __init__(self, member, role):
        self.member = member
        self.role = role
        self.alive = True


class Game():

    def __init__(self):
        self.open = False
        self.started = False
        self.members = [] # List of discord.Member objects
        self.players = [] # List of Player objects
        self.day = True

    async def start(self):
        self.open = True
        # Establish server context
        self.server = bot.get_server("355001416680734743")
        self.alive_channel_text = self.get_channel("alive")
        self.dead_channel_text = self.get_channel("dead")
        self.alive_channel_voice = self.get_channel("Alive")
        self.dead_channel_voice = self.get_channel("Dead")
        
        # Waiting period
        await asyncio.sleep(JOIN_LENGTH)
        self.open = False
        self.started = True
        await bot.send_message(self.alive_channel_text, "A game is starting...")
        
        # Assign roles
        for member in self.members:
            # TODO: Random role assignment
            self.players.append(Player(member, Villager()))
        
        # Set permissions
        for member in self.server.members:
            if member in self.members:
                overwrite = discord.PermissionOverwrite()
                overwrite.read_messages = False
                overwrite.send_message = False
                await bot.edit_channel_permissions(self.dead_channel_text, member, overwrite)
                overwrite = discord.PermissionOverwrite()
                overwrite.connect = False
                await bot.edit_channel_permissions(self.dead_channel_voice, member, overwrite)
                if not member.voice.voice_channel == None:
                    await bot.move_member(member, self.alive_channel_voice)
            else:
                overwrite = discord.PermissionOverwrite()
                overwrite.read_messages = True
                overwrite.send_message = False
                await bot.edit_channel_permissions(self.alive_channel_text, member, overwrite)
                overwrite = discord.PermissionOverwrite()
                overwrite.connect = False
                await bot.edit_channel_permissions(self.alive_channel_voice, member, overwrite)
                if not member.voice.voice_channel == None:
                    await bot.move_member(member, self.dead_channel_voice)
        
        # Start day/night cycle
        while True:
            await self.to_day()
            await asyncio.sleep(DAY_LENGTH)
            await self.to_night()
            await asyncio.sleep(NIGHT_LENGTH)
            
    def get_channel(self, name):
        for channel in self.server.channels:
            if channel.name == name:
                return channel
        
    async def to_day(self):
        await bot.send_message(self.alive_channel_text, "The sun is rising...")
        for player in self.players:
            if player.alive:
                overwrite = discord.PermissionOverwrite()
                overwrite.read_messages = True
                overwrite.send_message = True
                await bot.edit_channel_permissions(self.alive_channel_text, player.member, overwrite)
                await bot.server_voice_state(player.member, mute=False, deafen=False)
        await asyncio.sleep(1)
        await bot.send_message(self.alive_channel_text, "Day has begun.")
        self.day = True
        
    async def to_night(self):
    	# TODO: Check if game is won
        await bot.send_message(self.alive_channel_text, "The sun is setting...")
        for player in self.players:
            if player.alive:
               overwrite = discord.PermissionOverwrite()
               overwrite.read_messages = True
               overwrite.send_message = False
               await bot.edit_channel_permissions(self.alive_channel_text, player.member, overwrite)
               await bot.server_voice_state(player.member ,mute=True, deafen=True)
        await asyncio.sleep(1)
        await bot.send_message(self.alive_channel_text, "Night has begun.")
        self.day = False


# On bot start
@bot.event
async def on_ready():
    log("Authenticated token successfully.\n")
    log("Username: {0}\nID: {1}\n".format(bot.user.name, bot.user.id))

# Remove players from game.
@bot.event
async def on_voice_state_update(before, after):
    pass

# Start a game of mafia.
@bot.command(pass_context=True)
async def start(context):
    if game.started or game.open:
        await bot.say("A game cannot be started, because one is already open or started!")
    else:
        bot.loop.create_task(game.start())
        await bot.say("A game is open to join! Type !join to join!")

# Resets all channel override permissions
@bot.command(pass_context=True)
async def resetchannelperms(context):
    for channel in context.server.channels:
          for target in channel.overwrites:
            await bot.delete_channel_permission(channel, target)

# Join a started game of mafia.
@bot.command(pass_context=True)
async def join(context):
    if game.open and not (context.message.author in game.members):
        game.members.append(context.message.author)
        await bot.say("{} has joined the game!".format(context.message.author.name))
    else:
        await bot.say("A game is not open, or you are already in the game!")

# Vote to lynch a player in a game of mafia.
@bot.command(pass_context=True)
async def vote(context, member: discord.Member):
    pass
  
# End game
@bot.command(pass_context=True)
async def stop():
    bot.close()


# Safe log
def log(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()

if __name__ == '__main__':
    log("Welcome to mafiabot!\nEnter your token: ")
    game = Game()
    try:
        bot.run(input())
    finally:
        bot.close()
