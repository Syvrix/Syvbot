# Syvbot
Discord bot to all roles and role permissions.

## Setup ##
Use venv to create virtual enviroment
    python3 venv venv
    .\venv\Scripts\activate
pip install -r requirements.txt


## .env file ##
in bot.py to start the bot discord requires a token to be passed. (see the last line in bot.py)
This token is retrieved from the application dashboard.

rename sample.env to .env and enter the token.

## if you update packages ##
run 'pip freeze > requirements.txt' in terminal