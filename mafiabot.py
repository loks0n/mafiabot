import discord, sys
from discord.ext import commands

client = commands.Bot(command_prefix=',', description="Play mafia, with your friends, through discord.")
server_games = {}

@client.event
async def on_ready():
	log("Logged into Discord successfully.\nUsername:{0}\nID: {1}\n".format(client.user.name, client.user.id))

# Doesn't seem to ever be triggered.
@client.event
async def on_server_join(server): 
	pass 

# Remove players from game.
@client.event
async def on_voice_state_update(before, after):
	pass

# Setup server for mafiabot.
@client.command(pass_context=True)
async def setup(context):
	channels = list(context.message.channel.server.channels)
	for channel in channels:
		try:
			await client.delete_channel(channel)
		except discord.Forbidden:
			await client.edit_channel(channel, name="outgame")
	await client.create_channel(context.message.channel.server, 'ingame', type=discord.ChannelType.text)
	await client.create_channel(context.message.channel.server, 'mafia', type=discord.ChannelType.text)
	await client.create_channel(context.message.channel.server, 'jail', type=discord.ChannelType.text)
	await client.create_channel(context.message.channel.server, 'outgame', type=discord.ChannelType.voice)
	await client.create_channel(context.message.channel.server, 'ingame', type=discord.ChannelType.voice)
	
	
# Start a game of mafia.
@client.command(pass_context=True)
async def start(context):
	pass
	
# Join a started game of mafia.
@client.command(pass_context=True)
async def join(context):
	pass
	
# Vote to lynch a player in a game of mafia.
@client.command(pass_context=True)
async def vote(context):
	pass
	
	
# Safe log
def log(msg):
	sys.stdout.write(msg)
	sys.stdout.flush()
	

log("Welcome to mafiabot!\nEnter your token: ")
token = input()
client.run(token)
