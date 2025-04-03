from code import interact
import os
from unittest import result
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import dotenv_values

# Import functions
from Roles_and_Permissions.FetchPerms import save_roles_permissions
from Roles_and_Permissions.FetchPerms import get_available_perms
from Roles_and_Permissions.FetchPerms import get_roles_by_permission



# Intent is used to only fetch data im out after.
intents = discord.Intents.default()
intents.members = True  # To allow access to member data
intents.guilds = True # allow bot access to server data

# Generate Bot instance & login
## Defnitions and tokens ##
client_token=dotenv_values(".env")
client_token=client_token.get("DISCORD_TOKEN")
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

##### Slash commands #####
@tree.command(name="roles", description="Lists your Discord roles") 
async def save_roles(interaction: discord.Interaction):
    guild = interaction.guild
    
    if guild:
        await save_roles_permissions(guild)
        await interaction.response.send_message("Roles has been saved", ephemeral=True)
    else:
        await interaction.response.send_message("Unable to fetch roles, insufficient permissions")
    

@tree.command(name="listrolesperms", description="List all roles sectioned under permissions.")
async def list_role_perms(interaction: discord.Interaction):
    guild = interaction.guild

    if guild is None:
        await interaction.response.send_message("Command must be ran in a server")
        return
    
    ## Collect all roles and perms ##
    result = await get_roles_by_permission(guild)
    ## Send the collected result ""
    await interaction.response.send_message(result)
        
## Start bot and loggin"
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    if not os.path.exists('servers\list_all_role_perms.json'):
        print("getting role perms list...")
        await get_available_perms()
        print("DONE: getting role perm list ")
    else:
        print("official perms list already generated.. skipping...")
    
    await tree.sync() # sync slash commands.
    #await tree.sync(guild=discord.Object(id=1308124482942271656)) # syncing development server id.
    print("Awaiting commands....")

    
    # Save roles & permissions for all guilds.
    #for guild in bot.guilds:
    #    await save_roles_permissions(guild)

# Run the bot
bot.run(f'{client_token}')