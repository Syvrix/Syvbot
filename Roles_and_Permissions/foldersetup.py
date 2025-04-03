# Check if guild(server) folder exists
truepath = ""

import os
def return_guild_folder(guild_id):
    global truepath 
    if truepath == "":
        truepath=f'servers/{guild_id}'
        if not os.path.exists(truepath):
            os.makedirs(truepath)
    return(truepath)

def server_role_file_path(guild):
    return(return_guild_folder(guild)+"/role_permission.json")