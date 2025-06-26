from code import interact
import os
from pickletools import read_decimalnl_long
from unittest import result
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import dotenv_values
import yt_dlp # NEW
from collections import deque # NEW
import asyncio # NEW

# Import functions
from Roles_and_Permissions.FetchPerms import save_roles_permissions
from Roles_and_Permissions.FetchPerms import get_available_perms
from Roles_and_Permissions.FetchPerms import get_roles_by_permission
from Roles_and_Permissions.foldersetup import server_role_file_path
from Functions.user_commands_permissions import command_is_in_server, command_check_all
from Functions.react_to_messages import react_to_message

# Lists and globals
## List that stores what commands are for admins only 
list_admin_commands=[]

# Add command to admin list if command is admin
async def command_is_admin(integration):
    #check if command already is added to list
    if integration.command.name not in list_admin_commands:
        list_admin_commands.append(integration.command.name)

# BOT properties
## Intent is used to only fetch data im out after. 
intents = discord.Intents.default()
intents.members = True  # To allow access to member data
intents.guilds = True # allow bot access to server data
intents.message_content = True

# Create the structure for queueing songs - Dictionary of queues
SONG_QUEUES = {}

async def search_ytdlp_async(query, ydl_opts):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: _extract(query, ydl_opts))

def _extract(query, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query, download=False)

# Generate Bot instance & login
## Defnitions and tokens ##
envars=dotenv_values(".env")
server_name=envars.get("SERVER_NAME")
client_token=envars.get("DISCORD_TOKEN")
if client_token == None:
    print("No client token found in .env file")
    exit
else:
    bot = commands.Bot(command_prefix='!', intents=intents)
    tree = bot.tree
        
@bot.command()
async def get_guild(ctx):
    print("running get_guild")
    guild = ctx.guild
    if guild:
        await ctx.send("Found guild")
        return(guild)
    else:
        await ctx.send("Unable to retrieve a guild")
    
async def save_roles(ctx):
    """Command to save the roles and permissions manually."""
    await save_roles_permissions(get_guild)

# Only display slash commands for users if they are administrator 
async def sync_commands():
    """Dynamically sync commands based on permissions."""
    for guild in bot.guilds:
        # Get the list of commands for the current guild
        commands = await bot.tree.fetch_commands(guild=guild)
        
        # If the user doesn't have admin permissions, remove the admin command
        for command in commands:
            if command.name == "admin_command":
                if not guild.get_member(bot.user.id).guild_permissions.administrator:
                    await bot.tree.remove_command(command.name, guild=guild)

#### Slash commands #####

#MUSIC BOT
@tree.command(name="skip", description="Skips the current playing song")
async def skip(interaction: discord.Interaction):
        # Add command if admin.
    admin_command=True
    if admin_command:
        await command_is_admin(interaction)
    try:
        await command_check_all(interaction) # Go through all tests.
    except: return
    
    if interaction.guild.voice_client and (interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
        interaction.guild.voice_client.stop()
        await interaction.response.send_message("Skipped the current song.")
    else:
        await interaction.response.send_message("Not playing anything to skip.")


@tree.command(name="pause", description="Pause the currently playing song.")
async def pause(interaction: discord.Interaction):
            # Add command if admin.
    admin_command=True
    if admin_command:
        await command_is_admin(interaction)
    try:
        await command_check_all(interaction) # Go through all tests.
    except: return

    voice_client = interaction.guild.voice_client

    # Check if the bot is in a voice channel
    if voice_client is None:
        return await interaction.response.send_message("I'm not in a voice channel.")

    # Check if something is actually playing
    if not voice_client.is_playing():
        return await interaction.response.send_message("Nothing is currently playing.")
    
    # Pause the track
    voice_client.pause()
    await interaction.response.send_message("Playback paused!")


@tree.command(name="resume", description="Resume the currently paused song.")
async def resume(interaction: discord.Interaction):
            # Add command if admin.
    admin_command=True
    if admin_command:
        await command_is_admin(interaction)
    try:
        await command_check_all(interaction) # Go through all tests.
    except: return

    voice_client = interaction.guild.voice_client

    # Check if the bot is in a voice channel
    if voice_client is None:
        return await interaction.response.send_message("I'm not in a voice channel.")

    # Check if it's actually paused
    if not voice_client.is_paused():
        return await interaction.response.send_message("I’m not paused right now.")
    
    # Resume playback
    voice_client.resume()
    await interaction.response.send_message("Playback resumed!")


@tree.command(name="stop", description="Stop playback and clear the queue.")
async def stop(interaction: discord.Interaction):
            # Add command if admin.
    admin_command=True
    if admin_command:
        await command_is_admin(interaction)
    try:
        await command_check_all(interaction) # Go through all tests.
    except: return

    voice_client = interaction.guild.voice_client

    # Check if the bot is in a voice channel
    if not voice_client or not voice_client.is_connected():
        return await interaction.response.send_message("I'm not connected to any voice channel.")

    # Clear the guild's queue
    guild_id_str = str(interaction.guild_id)
    if guild_id_str in SONG_QUEUES:
        SONG_QUEUES[guild_id_str].clear()

    # If something is playing or paused, stop it
    if voice_client.is_playing() or voice_client.is_paused():
        voice_client.stop()

    # (Optional) Disconnect from the channel
    await voice_client.disconnect()

    await interaction.response.send_message("Stopped playback and disconnected!")


@tree.command(name="play", description="Play a song or add it to the queue.")
@app_commands.describe(song_query="Search query")
async def play(interaction: discord.Interaction, song_query: str):
            # Add command if admin.
    admin_command=True
    if admin_command:
        await command_is_admin(interaction)
    try:
        await command_check_all(interaction) # Go through all tests.
    except: return

    await interaction.response.defer()

    voice_channel = interaction.user.voice.channel

    if voice_channel is None:
        await interaction.followup.send("You must be in a voice channel.")
        return

    voice_client = interaction.guild.voice_client

    if voice_client is None:
        voice_client = await voice_channel.connect()
    elif voice_channel != voice_client.channel:
        await voice_client.move_to(voice_channel)

    ydl_options = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        "noplaylist": True,
        "youtube_include_dash_manifest": False,
        "youtube_include_hls_manifest": False,
        'source_address': '0.0.0.0',
    }

    query = "ytsearch1: " + song_query
    results = await search_ytdlp_async(query, ydl_options)
    tracks = results.get("entries", [])

    if tracks is None:
        await interaction.followup.send("No results found.")
        return

    first_track = tracks[0]
    audio_url = first_track["url"]
    title = first_track.get("title", "Untitled")

    guild_id = str(interaction.guild_id)
    if SONG_QUEUES.get(guild_id) is None:
        SONG_QUEUES[guild_id] = deque()

    SONG_QUEUES[guild_id].append((audio_url, title))

    if voice_client.is_playing() or voice_client.is_paused():
        await interaction.followup.send(f"Added to queue: **{title}**")
    else:
        await interaction.followup.send(f"Added to queue: **{title}**")
        await play_next_song(voice_client, guild_id, interaction.channel)


async def play_next_song(voice_client, guild_id, channel):
    if SONG_QUEUES[guild_id]:
        audio_url, title = SONG_QUEUES[guild_id].popleft()

        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn -c:a libopus -b:a 96k",
            # Remove executable if FFmpeg is in PATH
        }

        source = discord.FFmpegOpusAudio(audio_url, **ffmpeg_options, executable="bin\\ffmpeg\\ffmpeg.exe")

        def after_play(error):
            if error:
                print(f"Error playing {title}: {error}")
            asyncio.run_coroutine_threadsafe(play_next_song(voice_client, guild_id, channel), bot.loop)

        voice_client.play(source, after=after_play)
        asyncio.create_task(channel.send(f"Now playing: **{title}**"))
    else:
        await voice_client.disconnect()
        SONG_QUEUES[guild_id] = deque()

# 1
@tree.command(name="roles", description="Creates a file with all your roles and their permissions in JSON format.") 
async def save_roles(interaction: discord.Interaction):
    guild = interaction.guild
        # Add command if admin.
    admin_command=True
    if admin_command:
        await command_is_admin(interaction)
    try:
        await command_check_all(interaction) # Go through all tests.
    except: return
    
    if guild:
        await save_roles_permissions(guild)
        #await interaction.response.send_message("Roles has been saved", ephemeral=True)
        p = server_role_file_path(guild)
        with open(p, 'rb') as f:
            await interaction.response.send_message(file=discord.File(f, p), ephemeral=True)
    else:
        await interaction.response.send_message("Unable to fetch roles, insufficient permissions")
    
# 2
@tree.command(name="listrolesperms", description="List all roles sectioned under permissions.")
async def list_role_perms(interaction: discord.Interaction):
    # Add command if admin.
    admin_command=True
    if admin_command:
        await command_is_admin(interaction)
    try:
        await command_check_all(interaction) # Go through all tests.
    except: return
    
    ## Collect all roles and perms ##
    result = await get_roles_by_permission(interaction.guild)
    ## Send the collected result ""
    await interaction.response.send_message(result, ephemeral=True)
    
## Start bot and loggin"
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    if not os.path.exists('servers/list_all_role_perms.json'):
        print("getting role perms list...")
        await get_available_perms()
        print("DONE: getting role perm list ")
    else:
        print("official perms list already generated.. skipping...")
    
    
        # Set status: Playing ServerName
        game = discord.Game(name=server_name)  # ← Replace with your custom text
        await bot.change_presence(status=discord.Status.online, activity=game)
    
    await tree.sync() # sync slash commands.
    #await tree.sync(guild=discord.Object(id=1308124482942271656)) # syncing development server id.
    print("Awaiting commands....")

    
    # Save roles & permissions for all guilds.
    #for guild in bot.guilds:
    #    await save_roles_permissions(guild)

# Active listening
## Reacting to posts
@bot.event
async def on_message(message):
    print(f"Message recorded: {message}")
    await react_to_message(bot, message)
    await bot.process_commands(message)

# Run the bot
bot.run(f'{client_token}')
