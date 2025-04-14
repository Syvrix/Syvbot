import discord
import random

#    Channels  #
CHANNEL_TOKEN_ID = 1193453486872997918 # Ukiyo
#CHANNEL_TOKEN_ID = 1193453486872997918 # Ukiyo
TEST_CHANNEL_TOKEN_ID = 1308124484091383820
## Channels END ##

# Custom Emojis
emoji = '<:bbuk_bunnyholdinghearts:953801325588668477>'
## Custom Emojis END ##

async def react_to_message(bot: discord.Client, message: discord.message):
    # Dont react if own message
    print(f"Message author id: {message.author.id}")
    if message.author ==bot.user or message.author.id==1193491075818594364:
        return
    
    # check if message is in channel
    if message.channel.id in [CHANNEL_TOKEN_ID, TEST_CHANNEL_TOKEN_ID]:
        #Add emoji/reaction
        print("new selfie post detected...\nadding emojis.")
        #print([e.name for e in message.guild.emojis]) # Prints out emojis bot has access to.
        try:
            await message.add_reaction('<:bbuk_bunnyholdinghearts:953801325588668477>')
            await message.add_reaction('<:BunsHeart:1024132221004681227>')
            await message.add_reaction('<:mmuk_flowers:971767935385362492>')
        except discord.errors.NotFound:
            print("Message no longer exists")
    
### FUN REACTION SECTION####
    fun=False #True = enabled, False = disabled
    
    #if message.author.id ==111031468846817280:
    #    await message.add_reaction('<:BunsHeart:1024132221004681227>')
     
    if fun:
        if message.channel.id == 1193389202755309678: 
            #if message.author.id ==343615168611221506 or message.author.id == 689266904048992290:
            if message.author.id ==1069536707860504586:
                print("Message recorded from user rin or cam")
                
                nr=random.randint(1,2)
                if nr == 1:
                    regional_characters=['🇱','🇴','🇸','🇪','🇷']
                if nr == 2:
                    regional_characters=['🇬','🇦','🇾']
                #regional_characters=['🇱','🇴','🇸','🇪','🇷'] 
                for reg_emoji in regional_characters:
                    await message.add_reaction(reg_emoji)  # Regional indicator for 'L'
                    
            if message.author.id == 239475824837918721 or message.author.id==273922715059093505:
                print("##### Message recorded from user 'Sy' #####")
                #regional_characters_gremlin=['🇬','🇷','🇪','🇲','🇱','🇮','🇳']
                nr=random.randint(1,2)
                if nr == 1:
                    regional_characters=['🇱','🇴','🇸','🇪','🇷']
                if nr == 2:
                    regional_characters=['🇬','🇦','🇾']
                for reg_emoji in regional_characters:
                    await message.add_reaction(reg_emoji)  # Regional indicator for 'L'
                    

