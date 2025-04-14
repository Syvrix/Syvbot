from code import interact
import os
from pickletools import read_decimalnl_long
from unittest import result
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import dotenv_values

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
async def command_is_admin(command): # Add command to admin list if command is admin
    if command.name not in list_admin_commands:
        list_admin_commands.append(command.name)

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