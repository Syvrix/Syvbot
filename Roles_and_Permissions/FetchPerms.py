# FetchPerms
## Import modules and necissities. ##
import json # Data strucutre and management for files.
import discord
import os
from .foldersetup import return_guild_folder # Code to create folder/dump data
from collections import defaultdict




async def save_roles_permissions(guild):
    # Fetch the guild (server) you are in
    # guild = bot.get_guild(YOUR_GUILD_ID)  # Replace with your guild ID

    # Ensure the bot is connected to the server
    if guild is None:
        print("Bot is not connected to the guild.")
        return

    # Prepare data to save
    roles_data = []
    
    for role in guild.roles:
        role_data = {
            "name": role.name,
            "permissions": [perm[0] for perm in role.permissions if perm[1]]  # Only include active permissions
        }
        print("appending role data")
        roles_data.append(role_data)
    
    # Save to a JSON file
    folder_path=return_guild_folder(guild.id)
    file_path=os.path.join(folder_path, "roles_permissions.json")
    print("saving to json file: " + folder_path)
    with open(file_path, "w") as f:
        json.dump(roles_data, f, indent=4)
    
    print("Roles and permissions saved to roles_permissions.json")
    return roles_data

## Create a list of all available permissions to a user ##
async def get_available_perms():
    path='servers/list_all_role_perms.json'
    if not os.path.exists(path):
        all_permissions = list(discord.Permissions.VALID_FLAGS.keys())
        with open(path, 'w') as f:
            json.dump(all_permissions, f, indent=4)
            
            
async def get_roles_by_permission(guild):
    # Get the roles data from the file
    roles_data = await save_roles_permissions(guild)
    print(roles_data)
    if not roles_data:
        return "no roles found"
    
    # Load all possible permissions from the "List_all_role_perm.json" file
    with open('servers/list_all_role_perms.json', 'r') as f:
        all_permissions = json.load(f)
    
    #initilize a dictionary to store perms as key:value pairs.
    permission_groups = defaultdict(list)
    
    # Loop throuh each role's permissions and group the roles
    for role in roles_data:
        role_name = role["name"]
        permissions = role["permissions"]
        
        for permission in permissions:
            if permission in all_permissions:
                permission_groups[permission].append(role_name)
                
    # Convert dic to normal dic for clean output.
    permission_groups= dict(permission_groups)
    
    # Format the result as string for display.
    result = ""
    for permission, roles in permission_groups.items():
        result+= f"**{permission}**: {', '.join(roles)}\n"
        
    return result
        
