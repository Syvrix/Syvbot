# Check if guild(server) folder exists
truepath = ""

import os

#Checks if guild folder exists, if not creates it.
def create_server_folder():
    if not os.path.exists('servers'):
        os.makedirs('servers')  # Create the 'servers' directory if it doesn't exist    

def return_guild_folder(guild_id):
    global truepath 
    if truepath == "":
        truepath=f'servers/{guild_id}'
        if not os.path.exists(truepath):
            os.makedirs(truepath)
    return(truepath)

def server_role_file_path(guild):
    return(return_guild_folder(guild)+"/role_permission.json")