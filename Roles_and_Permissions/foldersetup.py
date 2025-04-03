# Check if guild(server) folder exists
import os
def return_guild_folder(guild_id):
    folder_path=f'servers/{guild_id}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return(folder_path)