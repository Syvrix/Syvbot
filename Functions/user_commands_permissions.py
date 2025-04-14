class CommandCheckFailure(Exception):
    pass

# Runs all checks for code readability
async def command_check_all(interaction):
    await command_is_in_server(interaction)
    await is_user_admin(interaction)

# Check if command is ran in server
async def command_is_in_server(interaction):
    if interaction.guild is None:
        await interaction.response.send_message("Command must be ran in a server")
        raise CommandCheckFailure()
    
# Check if user is administrator
async def is_user_admin(interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("User is not administrator",ephemeral=True)
        raise CommandCheckFailure()