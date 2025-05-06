import asyncio
cmd1="add birthday"
cmd2="delete users"

list_admin_commands=[]
print("Printing list after initiation.")
print(list_admin_commands)

async def command_is_admin(integration):
    #check if command already is added to list
    if integration not in list_admin_commands:
        list_admin_commands.append(integration)
        print("Command added to admin list")
        print(list_admin_commands)

async def run_script():
    await command_is_admin(cmd1)
    await command_is_admin(cmd2)
run_script()

asyncio.run(run_script())
print("### Script done ###")