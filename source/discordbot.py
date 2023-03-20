# Imports
import json # to handle json files
import os # to handle directories
import logging # to work with logging
import time # to time bot bootup times
from decouple import config # to work with .env file
from discord.ext import commands # command functionality for discord.py
import discord # main discord API functionality
from dotenv import load_dotenv # to work with .env file
import asyncio
import random

# File imports
import passwordgen_program as PassGen # Imports password generator source file
from main import UUIDFetch # Imports function for fetching Minecraft UUID
from GamesAPI import GamesList as GamesAPI # Imports function for pinging Hypixel API
from Session import MainProcess as SessionAPI # Imports function for pinging Hypixel API
from Coins import GetMostCoins # Imports most coins function

# Fetching file directory
realpath = os.path.realpath(__file__)
directory = realpath[0:-20]

# Setting up logging
logging.basicConfig(filename=directory+"bot.log", level = logging.INFO, format='%(levelname)s %(asctime)s %(message)s')

# Setting up the Discord API token from .env file
load_dotenv()
TOKEN = config("DISCORD_TOKEN")

# Setting preset colour variables to be used with Discord embeds
Aqua = 0x33ffff
Red = 0xff0000
Yellow = 0xffeb2a
Green = 0x80c904

def configImport():
# Imports config. Guild settings stored inside a .json file
    x = open(directory+"config.json", "r")
    data = json.load(x)
    x.close()
    return data

# Calls config import function
Config = configImport()

def get_prefix(bot, msg):
# Fetching any possible preset guild bot prefix, if none is found the default "$" is set
    Set = False
    # Searching through config file for a match in guild ID
    for y in range(len(Config["guilds"])):
        if int(Config["guilds"][y]["guildID"]) == int(msg.guild.id):
            # Returning preset prefix found in config
            return str(Config["guilds"][y]["prefix"])
            Set = True

    # Setting default prefix if none is found in config file
    if Set == False:
        return "$"

def get_pass(bot, ctx):
# Getting a boolean value to see if the pass command is turned off, and returning a boolean to be used when the pass command is ran
    Set = False
    for y in range(len(Config["guilds"])):
        if int(Config["guilds"][y]["guildID"]) == int(ctx.guild.id):
            return str(Config["guilds"][y]["pass-command"])
            Set = True

    # Checks if the pass command disabling boolean has been set in config, if not, the command is enabled by default
    if Set == False:
        return True

def get_loc(guildid):
# Function to find the matching location of a set guildID within the config.json file
    for y in range(len(Config["guilds"])):
        if Config["guilds"][y]["guildID"] == str(guildid):
            location = y
    return location

# Setting up the bot, removing the preset help command.
bot = commands.Bot(command_prefix = get_prefix)
bot.remove_command('help')


@bot.event
# Courtine ran when a command experiances an error, allows to handle non code related exceptions, for example:
# Command cooldowns or Missing user permissions. Also is used in input validation
async def on_command_error(ctx, error):

    # Error fires when a command is ran but a parameter is missing. For example the name string from !cmp
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed = discord.Embed(color = Red)
        embed.add_field(name = "Error", value = "A parameter is missing!")
        await ctx.send(embed = embed)

    # Error fires when a command is ran but the command cooldown is still in effect
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(color = Red)
        embed.add_field(name = "Error", value = "Command is on cooldown!")
        await ctx.send(embed = embed)

    # Error fires when user issuing the command is missing Discord side permissions
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        embed = discord.Embed(color = Red)
        embed.add_field(name = "Error", value = "Sorry about that, you do not have the required permissions to run this!")
        await ctx.send(embed = embed)

    # Error fires when someone uses the prefix but doesnt issue a valid command
    elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
        embed = discord.Embed(color = Red)
        embed.add_field(name = "Error", value = "This is not a valid command!")
        await ctx.send(embed = embed)

    # Error fires when the command itself fires a error
    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        #Start of error string, is constant with all exceptions.
        Start = "Command raised an exception: "

        # Error fires when the $pass command is passed a integer lower than 12
        if str(error) == Start+"Exception: Password too small":
            embed = discord.Embed(color = Red)
            embed.add_field(name = "Error", value = "That password is too small! Please ensure you enter a lenght of at least 12!")
            await ctx.send(embed = embed)

        # Error fires when the $pass command is passed a integer higher than 256
        elif str(error) == Start+"Exception: Password too big":
            embed = discord.Embed(color = Red)
            embed.add_field(name = "Error", value = "That password is too long! Please ensure you enter a lenght that is smaller than 256!")
            await ctx.send(embed = embed)

        # Error fires when the $pass command is passed a integer that isnt either 0 or 1
        elif str(error) == Start+"Exception: PassUni Invalid":
            embed = discord.Embed(color = Red)
            embed.add_field(name = "Error", value = "Please enter either 0 for ASCII or 1 for Unicode")
            await ctx.send(embed = embed)

        # Error fires when a command handling a Minecraft usernames is passed a string that is longer than 16 (MC names cannot exceed 16 characters, no point checking Mojangs API for profile if the lengh > 16)
        elif str(error) == Start+"Exception: Username too long":
            embed = discord.Embed(color = Red)
            embed.add_field(name = "Error", value = "Please enter a username with a maximum lenght of 16.")
            await ctx.send(embed = embed)

        # Error fires when Discord API shows that the bot is either Blocked or has DMs disabled, so when the bot tries to send a DM its forbidden.
        elif str(error) == Start+"Forbidden: 403 Forbidden (error code: 50007): Cannot send messages to this user":
            embed = discord.Embed(color = Red)
            embed.add_field(name = "Error", value = "Cannot send messages to this user!")
            await ctx.send(embed = embed)

        # Error fires when any command detects a API outage/no response from the Hypixel API
        elif str(error) == Start+"Exception: API appears down":
            embed = discord.Embed(color = Red)
            embed.add_field(name = "Error", value = "API appears to be down")
            await ctx.send(embed = embed)

        # Error fires when the Hypixel API returns a malformed response missing key information
        elif str(error) == Start+"Exception: Username is unknown":
            embed = discord.Embed(color = Yellow)
            embed.add_field(name = "Alert!", value = "This username returns a mainly empty file. This is likely one of those usernames that would return no name on plancke and is a general pain to work with. So it is skipped.")
            await ctx.send(embed = embed)

        # Error fires when the Mojang API cannot find the MC profile name and hence cannot return a UUID
        elif str(error) == Start+"Exception: Username is invalid":
            embed = discord.Embed(color = Red)
            embed.add_field(name = "Error", value = "Sorry, but that username is not valid! Make sure you re-enter it")
            await ctx.send(embed = embed)

        # Catching for any other errors
        else:
            await ctx.send("Some error happened, printed in console.")
            logging.error(error)
            raise error

    # Catching for any other errors
    else:
        await ctx.send("Some error happened, printed in console.")
        logging.error(error)
        raise error


@bot.event
# This is ran when the bot is ready. This function allows me to catch errors in the config file, more notably it missing any guilds inside as it is possible someone can add the bot to their guild while its offline, and then the on_guild_join will not run.
async def on_ready():

    # Logs that bot is starting and initiates time variable used to time starting process
    logging.info("Bot is starting...")
    start_time = time.time()
    guildIDs = []

    # Fetches and appens all current guilds the bot is connected to
    for guild in bot.guilds:
        guildIDs.append(guild.id)

    # Prints the amount of guilds the bot connected to
    print("The bot connected to",len(guildIDs),"guild(s).")

    LocationZ = []
    LocationY = []
    IDFoundList = []
    IDLocations = []

    # Searches through current connected to guilds for guilds within the config
    for z in range(len(guildIDs)):
        for y in range(len(Config["guilds"])):

            # Adds a check to see if the guild within the config and the guild thats been connected to is already in a pair
            if int(guildIDs[z]) == int(Config["guilds"][y]["guildID"]) and (y not in LocationY or z not in LocationZ):
                LocationY.append(y)
                LocationZ.append(z)
                IDFoundList.append(guildIDs[z])

    # Checks for any guilds are not in the config, if not, it likely means the guild added the bot without it being online, so the on_guild_join function didn't fire
    for x in range(len(guildIDs)):
        if guildIDs[x] not in IDFoundList:
            IDLocations.append(x)

    # Checks if the amount of guilds not in the config is not 0, if it is it means no guilds added the bot while the bot was down
    if len(IDLocations) != 0:
        for x in range(len(IDLocations)):
            Config["guilds"].append({"guildID" : str(guildIDs[IDLocations[x-1]]), "prefix" : "$", "pass-command" : True, "chat" : "all"})
            ##{"guilds" : []}
        with open(directory+"config.json", "w") as configFile:
            json.dump(Config, configFile)

    logging.info("The bot connected to "+str(len(guildIDs))+" guild(s).")
    logging.info("Bot is up. Time taken to initialize: "+"%s seconds" % (round(time.time() - start_time, 5)))

    #await SendDMs()

# This runs when the bot joins a guild. It checks if the bot was already in the guild and therefore has a config for the guild already set in the json file and if not it will make a new entry.

@bot.event
async def on_guild_join(guild):
    logging.info("Bot has joined a guild")
    InConfig = False
    for x in range(len(Config["guilds"])):
        if int(Config["guilds"][x]["guildID"]) == int(guild.id) and InConfig != True:
            print("Bot joined a guild, however a config is already setup for "+guild.name+". Skipping default config setting")
            InConfig = True
    if InConfig != True:
        Config["guilds"].append({"guildID" : str(guild.id), "prefix" : "$", "pass-command" : True, "chat" : "all"})
        print("Bot joined a new server, set default config for "+guild.name)
        with open(directory+"config.json", "w") as configFile:
            json.dump(Config, configFile)


# This runs every time a message is sent. This can be within a guild or a direct message channel with the bot (That is why there is a "isinstance(message.channel, discord.DMChannel)" check). This is used to fetch the prefix, respond with the bots ping message and also process commands on the message.

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        return
    else:
        location = get_loc(message.guild.id)
        if Config["guilds"][location]["chat"] == "all":
            Allowed = True
        elif Config["guilds"][location]["chat"] == str(message.channel.id):
            Allowed = True
        else:
            Allowed = False
        if message.author != bot.user:
            prefix = get_prefix(bot, message)
            if Allowed == True:
                if bot.user.mentioned_in(message):
                    await message.channel.send("Hello there! My prefix is "+prefix+" if you have anymore issues. Run: "+prefix+"Help")
                else:
                    await bot.process_commands(message)

# This is the password command. It takes the passlen - lenght of the password - and passuni - a 1 or 0 which sets either Unicode or Ascii as the go to characterset for the password. It then sends the password via a DM that auto deletes after 30 seconds.

@bot.command(name='Pass', aliases=["pass", "password", "generate"])
@commands.cooldown(1, 20, commands.BucketType.user)
async def Pass(ctx, PassLen, PassUni):
    PassComm = get_pass(bot, ctx)

    # Pass boolean variable check

    if PassComm == "False":
        embed = discord.Embed(color = Red)
        embed.add_field(name = "Error", value = "This command is disabled, please change your config or contact the server admin.")
        await ctx.send(embed = embed)
    else:
        if int(PassLen) < 12:
            raise Exception("Password too small")
        elif int(PassLen) > 256:
            raise Exception("Password too big")
        else:
            if PassUni == "1" or PassUni == "0":
                Pass = PassGen.PassProcess(int(PassLen), PassUni)
                #Checks if the password uses unicode or not and sets a string variable to append to response embed.
                if PassUni == "1":
                    UnicodeYesNo = "does"
                else:
                    UnicodeYesNo = "does not"
                channel = await ctx.message.author.create_dm()
                embed = discord.Embed(title = "Password", color = Aqua)
                embed.add_field(name = "Here is your generated password:", value = Pass)
                embed.set_footer(text = "Made by RRBuilder#5922. This password is "+PassLen+" characters long and "+UnicodeYesNo+" include unicode. This message will auto delete in 60 seconds :)")
                await channel.send(embed = embed, delete_after = 60)
                await ctx.send("Password sent to your DMs :mailbox_with_mail:")
            else:
                raise Exception("PassUni Invalid")

# Help command. Basic information about the bot and its functions for the end user.

@bot.command(name = "help", aliases = ["h", "Help", "Useage"])
async def Help(ctx):
    prefix = get_prefix(bot, ctx)
    embed = discord.Embed(title = "Help", color = Aqua)
    embed.add_field(name = "How to use the bot:", value = "This bot has a simple function. It is to return last session data from the hypixel API. In order to use the bot you need to use the CMP/Comp command. The usage for this bot is as follows: "+prefix+"CMP Username")
    embed.add_field(name = "What is this bot for?", value = "This bot will help you find out if someones account got hacked by comparing their last session data to the APIs. If they, for example, say they played Bedwars last yet they played Skywars you will be able to know!")
    embed.add_field(name = "Who made this bot?", value = "RRBuilder#5922 is the developer for this project. Contact them if you have any issues.")
    await ctx.send(embed = embed)

# "Compromised" command. Main function of the bot. Passes in the username and returns last session and recent games.

@bot.command(name = 'Comp', aliases = ["comp", "Compromised", "compromised", "hacked", "Hacked", "CMP", "cmp"])
@commands.cooldown(1, 10, commands.BucketType.user)
async def Comp(ctx, username):
    if len(username) > 16 or len(username) <= 0:
        raise Exception("Username too long")

    uuid = UUIDFetch(username)

    Session_Version, Session_LastLogin, Session_LastLogout, Session_UserLanguage, Session_LastGameType, Session_Length, Session_Username, Session_Timestamp = SessionAPI(uuid)

    Games, Maps, TimesStarted, TimesEnded, Lenghts = GamesAPI(uuid)

    embed = discord.Embed(title = "Last session.", color = Aqua)
    text = "```\nUUID: "+uuid+"```"+"```\nVersion: "+Session_Version+"```"+"```\nLast Login: "+str(Session_LastLogin)+"```"+"```\nLast Logout: "+str(Session_LastLogout)+"```"+"```\nLanguage: "+Session_UserLanguage+"```"+"```\nLast game type: "+Session_LastGameType+"```"+"```\nSession length: "+str(Session_Length)+"```"+"\nThe above happened <t:"+str(Session_Timestamp)+":R>"
    embed.add_field(name = "Here is the last player session for ```"+Session_Username+"```", value = text)
    await ctx.send(embed = embed)
    if len(Games) == 0:
        embed = discord.Embed(color = Yellow)
        embed.add_field(name = "Alert!", value = "No games were detected for the username entered! They likely haven't played any games recently. :)")
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(title = "Recent games.", color = Aqua)
        for x in range(len(Games)):
            count = x+1
            if len(Games) < count:
                pass
            else:
                text = "```\nGameType: "+str(Games[x])+"```"+"```\nMap: "+str(Maps[x])+"```"+"```\nTime Started: "+str(TimesStarted[x])+"```"+"```\nTime Ended: "+str(TimesEnded[x])+"```"+"```\nLength: "+str(Lenghts[x]+"\n\n```")
                embed.add_field(name = "Game: "+str(count), value = text)
        await ctx.send(embed = embed)

# Prefix command. Used to change and set a new prefix for the bot. Only usable by server admins. Takes in message context and the prefix as a parameter. Has a guild cooldown of 60 seconds. Also saves the prefix to the config.json file

@bot.command(name = "Prefix", aliases = ["prefix"])
@commands.has_permissions(administrator = True)
@commands.cooldown(1, 50, commands.BucketType.guild)
async def Prefix(ctx, prefix):
    location = get_loc(ctx.guild.id)
    if prefix == Config["guilds"][location]["prefix"]:
        await ctx.send("Hey! Your prefix is already set to "+prefix)
    else:
        await ctx.send("Set prefix to "+prefix)
        Config["guilds"][location]["prefix"] = prefix
        with open(directory+"config.json", "w") as configFile:
            json.dump(Config, configFile)

# Setchat command. Only usable by admins. Used to set a response channel to the bot or allows it to respond in all channels if a response channel is already set.

@bot.command(name = "Setchat", aliases = ["setac", "setchat", "chat"])
@commands.has_permissions(administrator = True)
@commands.cooldown(1, 60, commands.BucketType.guild)
async def Setchat(ctx, option):
    location = get_loc(ctx.guild.id)
    if option != "all" and option != "this":
        await ctx.send("Hey! Please use either ``all`` or ``this`` for this command :)")
    elif option == "all":
        if Config["guilds"][location]["chat"] == "all":
            await ctx.send("Your bot chat is already set to respond in all channels :)")
        else:
            await ctx.send("Your bot will now respond in all channels")
            Config["guilds"][location]["chat"] = "all"
            with open(directory+"config.json", "w") as configFile:
                json.dump(Config, configFile)
    else:
        if Config["guilds"][location]["chat"] == str(ctx.channel.id):
            await ctx.send("Your bot chat is already set to this channel :)")
        else:
            await ctx.send("Set the bot to only respond in this chat :)")
            Config["guilds"][location]["chat"] = str(ctx.channel.id)
            with open(directory+"config.json", "w") as configFile:
                json.dump(Config, configFile)

# passtoggle command. Allows a server admin to turn the password command on and off.

@bot.command(name = "passtoggle", aliases = ["passtog", "pt", "togglepass"])
@commands.has_permissions(administrator = True)
@commands.cooldown(1, 30, commands.BucketType.guild)
async def passtoggle(ctx):
    location = get_loc(ctx.guild.id)
    if Config["guilds"][location]["pass-command"] == True:
        Setting = False
        embed = discord.Embed(color = Red)
        embed.add_field(name = "Password generator",value = "Disabled!")
        await ctx.send(embed = embed)
    elif Config["guilds"][location]["pass-command"] == False:
        Setting = True
        embed = discord.Embed(color = Green)
        embed.add_field(name = "Password generator",value = "Enabled!")
        await ctx.send(embed = embed)
    else:
        await ctx.send("Well, something broke so we enabled the passcommand just in case")
        Setting = True
    Config["guilds"][location]["pass-command"] = Setting
    with open(directory+"config.json", "w") as configFile:
        json.dump(Config, configFile)

# mostcoins command. Fetches player data and inputs into two parrarel arrays then uses insersertaion sort.

@bot.command(name = "mostcoins", aliases = ["mcoins", "mc"])
@commands.cooldown(1, 10, commands.BucketType.user)
async def mostcoins(ctx, username):
    if len(username) > 16 or len(username) <= 0:
        raise Exception ("Username too long")
    uuid = UUIDFetch(username)

    MostCoins, MostCoinsGame, Username = GetMostCoins(uuid)

    text = "**Game:** ```"+str(MostCoinsGame)+"```\n**Amount:** ```"+str(MostCoins)+"```"
    embed = discord.Embed(color = Green)
    embed.add_field(name = "Most coins for "+Username, value = text)
    await ctx.send(embed = embed)

bot.run(TOKEN)
