import os

from dotenv import dotenv_values
envvars= dotenv_values(".env")
print(envvars.get("DISCORD_TOKEN"))