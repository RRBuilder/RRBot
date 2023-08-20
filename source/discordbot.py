# Imports
import json  # to handle json files
import os  # to handle directories
import logging  # to work with logging
import time  # to time bot bootup times
from decouple import config  # to work with .env file
from discord.ext import commands  # command functionality for discord.py
import discord  # main discord API functionality
from dotenv import load_dotenv  # to work with .env file

# File imports
import passwordgen_program as PassGen  # Imports password generator source file
from main import UUIDFetch  # Imports function for fetching Minecraft UUID
from GamesAPI import GamesList as GamesAPI  # Imports function for pinging Hypixel API
from Session import MainProcess as SessionAPI  # Imports function for pinging Hypixel API
from Coins import GetMostCoins  # Imports most coins function

# Fetching file directory
realpath = os.path.realpath(__file__)
directory = realpath[0:-20]

# setting up logging
logging.basicConfig(filename=directory + "bot.log", level=logging.INFO, format='%(levelname)s %(asctime)s %(message)s')

# setting up the Discord API token from .env file
load_dotenv()
TOKEN = config("DISCORD_TOKEN")

# setting preset colour variables to be used with Discord embeds
aqua = 0x33ffff
red = 0xff0000
yellow = 0xffeb2a
green = 0x80c904

def configImport():
    # Imports config. Guild settings stored inside a .json file
    x = open(directory + "config.json", "r")
    data = json.load(x)
    x.close()
    return data


# Calls config import function
config = configImport()


def get_prefix(bot, msg):
    # Fetching any possible preset guild bot prefix, if none is found the default "$" is set
    prefixSet = False
    # Searching through config file for a match in guild ID
    for y in range(len(config["guilds"])):
        if int(config["guilds"][y]["guildID"]) == int(msg.guild.id):
            # Returning preset prefix found in config
            prefixSet = True
            return str(config["guilds"][y]["prefix"])

    # setting default prefix if none is found in config file
    if not prefixSet:
        return "$"


def get_pass(bot, ctx):
    # Getting a boolean value to see if the pass command is turned off, and returning a boolean to be used when the pass command is ran
    passwordToggle = False
    for y in range(len(config["guilds"])):
        if int(config["guilds"][y]["guildID"]) == int(ctx.guild.id):
            passwordToggle = True
            return str(config["guilds"][y]["pass-command"])

    # Checks if the pass command disabling boolean has been set in config, if not, the command is enabled by default
    if not passwordToggle:
        return True


def get_loc(guildID):
    location = -1
    # Function to find the matching location of a set guildID within the config.json file
    for y in range(len(config["guilds"])):
        if config["guilds"][y]["guildID"] == str(guildID):
            location = y
    return location


# setting up the bot, removing the preset help command.
bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command('help')


@bot.event
# Courtine ran when a command experiences an error, allows to handle non code related exceptions, for example:
# Command cool-downs or Missing user permissions. Also is used in input validation
async def on_command_error(ctx, error):
    # Error fires when a command is ran but a parameter is missing. For example the name string from !cmp
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.add_field(name="Error", value="A parameter is missing!")
        await ctx.send(embed=embed)

    # Error fires when a command is ran but the command cooldown is still in effect
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(color=red)
        embed.add_field(name="Error", value="Command is on cooldown!")
        await ctx.send(embed=embed)

    # Error fires when user issuing the command is missing Discord side permissions
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        embed = discord.Embed(color=red)
        embed.add_field(name="Error", value="Sorry about that, you do not have the required permissions to run this!")
        await ctx.send(embed=embed)

    # Error fires when someone uses the prefix but doesn't issue a valid command
    elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
        embed = discord.Embed(color=red)
        embed.add_field(name="Error", value="This is not a valid command!")
        await ctx.send(embed=embed)

    # Error fires when the command itself fires an error
    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        # start of error string, is constant with all exceptions.
        start = "Command raised an exception: "

        # Error fires when the $pass command is passed an integer lower than 12
        if str(error) == start + "Exception: Password too small":
            embed = discord.Embed(color=red)
            embed.add_field(name="Error",
                            value="That password is too small! Please ensure you enter a length of at least 12!")
            await ctx.send(embed=embed)

        # Error fires when the $pass command is passed an integer higher than 256
        elif str(error) == start + "Exception: Password too big":
            embed = discord.Embed(color=red)
            embed.add_field(name="Error",
                            value="That password is too long! Please ensure you enter a lenght that is smaller than 256!")
            await ctx.send(embed=embed)

        # Error fires when the $pass command is passed an integer that isn't either 0 or 1
        elif str(error) == start + "Exception: passUni Invalid":
            embed = discord.Embed(color=red)
            embed.add_field(name="Error", value="Please enter either 0 for ASCII or 1 for Unicode")
            await ctx.send(embed=embed)

        # Error fires when a command handling a Minecraft usernames is passed a string that is longer than 16 (MC 
        # names cannot exceed 16 characters, no point checking Mojangs API for profile if the lengh > 16)
        elif str(error) == start + "Exception: Username too long":
            embed = discord.Embed(color=red)
            embed.add_field(name="Error", value="Please enter a username with a maximum lenght of 16.")
            await ctx.send(embed=embed)

        # Error fires when Discord API shows that the bot is either Blocked or has DMs disabled, so when the bot 
        # tries to send a DM its forbidden.
        elif str(error) == start + "Forbidden: 403 Forbidden (error code: 50007): Cannot send messages to this user":
            embed = discord.Embed(color=red)
            embed.add_field(name="Error", value="Cannot send messages to this user!")
            await ctx.send(embed=embed)

        # Error fires when any command detects an API outage/no response from the Hypixel API
        elif str(error) == start + "Exception: API appears down":
            embed = discord.Embed(color=red)
            embed.add_field(name="Error", value="API appears to be down")
            await ctx.send(embed=embed)

        # Error fires when the Hypixel API returns a malformed response missing key information
        elif str(error) == start + "Exception: Username is unknown":
            embed = discord.Embed(color=yellow)
            embed.add_field(name="Alert!",
                            value="This username returns a mainly empty file. This is likely one of those usernames that would return no name on plancke and is a general pain to work with. So it is skipped.")
            await ctx.send(embed=embed)

        # Error fires when the Mojang API cannot find the MC profile name and hence cannot return a UUID
        elif str(error) == start + "Exception: username is invalid":
            embed = discord.Embed(color=red)
            embed.add_field(name="Error", value="Sorry, but that username is not valid! Make sure you re-enter it")
            await ctx.send(embed=embed)

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
# This is ran when the bot is ready. This function allows me to catch errors in the config file, more notably it's 
# missing any guilds inside as it is possible someone can add the bot to their guild while its offline, and then the 
# on_guild_join will not run.
async def on_ready():
    # Logs that bot is starting and initiates time variable used to time starting process
    logging.info("Bot is starting...")
    start_time = time.time()
    guildIDs = []

    # Fetches and appends all current guilds the bot is connected to
    for guild in bot.guilds:
        guildIDs.append(guild.id)

    # Prints the amount of guilds the bot connected to
    print("The bot connected to", len(guildIDs), "guild(s).")

    locationZ = []
    locationY = []
    IDFoundList = []
    IDLocations = []

    # Searches through current connected to guilds for guilds within the config
    for z in range(len(guildIDs)):
        for y in range(len(config["guilds"])):

            # Adds a check to see if the guild within the config and the guild thats been connected to is already in 
            # a pair
            if int(guildIDs[z]) == int(config["guilds"][y]["guildID"]) and (y not in locationY or z not in locationZ):
                locationY.append(y)
                locationZ.append(z)
                IDFoundList.append(guildIDs[z])

    # Checks for any guilds are not in the config, if not, it likely means the guild added the bot without it being 
    # online, so the on_guild_join function didn't fire
    for x in range(len(guildIDs)):
        if guildIDs[x] not in IDFoundList:
            IDLocations.append(x)

    # Checks if the amount of guilds not in the config is not 0, if it is it means no guilds added the bot while the 
    # bot was down
    if len(IDLocations) != 0:
        for x in range(len(IDLocations)):
            config["guilds"].append(
                {"guildID": str(guildIDs[IDLocations[x - 1]]), "prefix": "$", "pass-command": True, "chat": "all"})
            # {"guilds" : []}
        with open(directory + "config.json", "w") as configFile:
            json.dump(config, configFile)

    logging.info("The bot connected to " + str(len(guildIDs)) + " guild(s).")
    logging.info("Bot is up. Time taken to initialize: " + "%s seconds" % (round(time.time() - start_time, 5)))


# This runs when the bot joins a guild. It checks if the bot was already in the guild and therefore has a config for 
# the guild already set in the json file and if not it will make a new entry.

@bot.event
async def on_guild_join(guild):
    logging.info("Bot has joined a guild")
    inConfig = False
    for x in range(len(config["guilds"])):
        if int(config["guilds"][x]["guildID"]) == int(guild.id) and inConfig != True:
            print(
                "Bot joined a guild, however a config is already setup for " + guild.name + ". Skipping default config setting")
            inConfig = True
    if not inConfig:
        config["guilds"].append({"guildID": str(guild.id), "prefix": "$", "pass-command": True, "chat": "all"})
        print("Bot joined a new server, set default config for " + guild.name)
        with open(directory + "config.json", "w") as configFile:
            json.dump(config, configFile)


# This runs every time a message is sent. This can be within a guild or a direct message channel with the bot (That is why there is a "isinstance(message.channel, discord.DMChannel)" check). This is used to fetch the prefix, respond with the bots ping message and also process commands on the message.

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        return
    else:
        location = get_loc(message.guild.id)
        if config["guilds"][location]["chat"] == "all":
            allowed = True
        elif config["guilds"][location]["chat"] == str(message.channel.id):
            allowed = True
        else:
            allowed = False
        if message.author != bot.user:
            prefix = get_prefix(bot, message)
            if allowed:
                if bot.user.mentioned_in(message):
                    await message.channel.send(
                        "Hello there! My prefix is " + prefix + " if you have anymore issues. Run: " + prefix + "Help")
                else:
                    await bot.process_commands(message)


# This is the password command. It takes the passlen - lenght of the password - and passuni - a 1 or 0 which sets 
# either Unicode or Ascii as the go to characterset for the password. It then sends the password via a DM that auto 
# deletes after 30 seconds.

@bot.command(name='Password', aliases=["pass", "password", "generate"])
@commands.cooldown(1, 20, commands.BucketType.user)
async def Password(ctx, passLen, passUni):
    passComm = get_pass(bot, ctx)

    # password boolean variable check

    if passComm == "False":
        embed = discord.Embed(color=red)
        embed.add_field(name="Error",
                        value="This command is disabled, please change your config or contact the server admin.")
        await ctx.send(embed=embed)
    else:
        if int(passLen) < 12:
            raise Exception("Password too small")
        elif int(passLen) > 256:
            raise Exception("Password too big")
        else:
            if passUni == "1" or passUni == "0":
                password = PassGen.PassProcess(int(passLen), passUni)
                # Checks if the password uses unicode or not and sets a string variable to append to response embed.
                if passUni == "1":
                    unicodeStringToggle = "does"
                else:
                    unicodeStringToggle = "does not"
                channel = await ctx.message.author.create_dm()
                embed = discord.Embed(title="Password", color=aqua)
                embed.add_field(name="Here is your generated password:", value=password)
                embed.set_footer(
                    text="Made by RRBuilder#5922. This password is " + passLen + " characters long and " + unicodeStringToggle + " include unicode. This message will auto delete in 60 seconds :)")
                await channel.send(embed=embed, delete_after=60)
                await ctx.send("Password sent to your DMs :mailbox_with_mail:")
            else:
                raise Exception("passUni Invalid")


# Help command. Basic information about the bot and its functions for the end user.

@bot.command(name="help", aliases=["h", "Help", "Usage"])
async def Help(ctx): 
    prefix = get_prefix(bot, ctx)
    embed = discord.Embed(title="Help", color=aqua)
    embed.add_field(name="How to use the bot:",
                    value="This bot has a simple function. It is to return last session data from the hypixel API. In "
                          "order to use the bot you need to use the CMP/Comp command. The usage for this bot is as "
                          "follows: " + prefix + "CMP username")
    embed.add_field(name="What is this bot for?",
                    value="This bot will help you find out if someones account got hacked by comparing their last "
                          "session data to the APIs. If they, for example, say they played Bedwars last yet they "
                          "played Skywars you will be able to know!")
    embed.add_field(name="Who made this bot?",
                    value="RRBuilder#5922 is the developer for this project. Contact them if you have any issues.")
    await ctx.send(embed=embed)


# "Compromised" command. Main function of the bot. Passes in the username and returns last session and recent games.

@bot.command(name='Comp', aliases=["comp", "Compromised", "compromised", "hacked", "Hacked", "CMP", "cmp"])
@commands.cooldown(1, 10, commands.BucketType.user)
async def Comp(ctx, username):
    if len(username) > 16 or len(username) <= 0:
        raise Exception("username too long")

    uuid = UUIDFetch(username)

    sessionVersion, sessionLastLogin, sessionLastLogout, sessionUserLanguage, sessionLastGameType, sessionLength, sessionUsername, sessionTimestamp = SessionAPI(
        uuid)

    gamesList, maps, timesStarted, timesEnded, lengths = GamesAPI(uuid)

    embed = discord.Embed(title="Last session.", color=aqua)
    text = "```\nUUID: " + uuid + "```" + "```\nVersion: " + sessionVersion + "```" + "```\nLast Login: " + str(
        sessionLastLogin) + "```" + "```\nLast Logout: " + str(
        sessionLastLogout) + "```" + "```\nLanguage: " + sessionUserLanguage + "```" + "```\nLast game type: " + sessionLastGameType + "```" + "```\nSession length: " + str(
        sessionLength) + "```" + "\nThe above happened <t:" + str(sessionTimestamp) + ":R>"
    embed.add_field(name="Here is the last player session for ```" + sessionUsername + "```", value=text)
    await ctx.send(embed=embed)
    if len(gamesList) == 0:
        embed = discord.Embed(color=yellow)
        embed.add_field(name="Alert!",
                        value="No games were detected for the username entered! They likely haven't played any games "
                              "recently. :)")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Recent games.", color=aqua)
        for x in range(len(gamesList)):
            count = x + 1
            if len(gamesList) < count:
                pass
            else:
                text = "```\nGameType: " + str(gamesList[x]) + "```" + "```\nMap: " + str(
                    maps[x]) + "```" + "```\nTime Started: " + str(timesStarted[x]) + "```" + "```\nTime Ended: " + str(
                    timesEnded[x]) + "```" + "```\nLength: " + str(lengths[x] + "\n\n```")
                embed.add_field(name="Game: " + str(count), value=text)
        await ctx.send(embed=embed)


# Prefix command. Used to change and set a new prefix for the bot. Only usable by server admins. Takes in message context and the prefix as a parameter. Has a guild cooldown of 60 seconds. Also saves the prefix to the config.json file

@bot.command(name="Prefix", aliases=["prefix"])
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 50, commands.BucketType.guild)
async def Prefix(ctx, prefix):
    location = get_loc(ctx.guild.id)
    if prefix == config["guilds"][location]["prefix"]:
        await ctx.send("Hey! Your prefix is already set to " + prefix)
    else:
        await ctx.send("set prefix to " + prefix)
        config["guilds"][location]["prefix"] = prefix
        with open(directory + "config.json", "w") as configFile:
            json.dump(config, configFile)


# SetChat command. Only usable by admins. Used to set a response channel to the bot or allows it to respond in all channels if a response channel is already set.

@bot.command(name="SetChat", aliases=["setac", "setchat", "chat"])
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 60, commands.BucketType.guild)
async def SetChat(ctx, option):
    location = get_loc(ctx.guild.id)
    if option != "all" and option != "this":
        await ctx.send("Hey! Please use either ``all`` or ``this`` for this command :)")
    elif option == "all":
        if config["guilds"][location]["chat"] == "all":
            await ctx.send("Your bot chat is already set to respond in all channels :)")
        else:
            await ctx.send("Your bot will now respond in all channels")
            config["guilds"][location]["chat"] = "all"
            with open(directory + "config.json", "w") as configFile:
                json.dump(config, configFile)
    else:
        if config["guilds"][location]["chat"] == str(ctx.channel.id):
            await ctx.send("Your bot chat is already set to this channel :)")
        else:
            await ctx.send("set the bot to only respond in this chat :)")
            config["guilds"][location]["chat"] = str(ctx.channel.id)
            with open(directory + "config.json", "w") as configFile:
                json.dump(config, configFile)


# passtoggle command. Allows a server admin to turn the password command on and off.

@bot.command(name="passtoggle", aliases=["passtog", "pt", "togglepass"])
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 30, commands.BucketType.guild)
async def PassToggle(ctx):
    location = get_loc(ctx.guild.id)
    if config["guilds"][location]["pass-command"] == True:
        setting = False
        embed = discord.Embed(color=red)
        embed.add_field(name="Password generator", value="Disabled!")
        await ctx.send(embed=embed)
    elif config["guilds"][location]["pass-command"] == False:
        setting = True
        embed = discord.Embed(color=green)
        embed.add_field(name="Password generator", value="Enabled!")
        await ctx.send(embed=embed)
    else:
        await ctx.send("Well, something broke so we enabled the passcommand just in case")
        setting = True
    config["guilds"][location]["pass-command"] = setting
    with open(directory + "config.json", "w") as configFile:
        json.dump(config, configFile)


# most-coins command. Fetches player data and inputs into two parallel arrays then uses insertion sort.

@bot.command(name="mostcoins", aliases=["mcoins", "mc"])
@commands.cooldown(1, 10, commands.BucketType.user)
async def MostCoins(ctx, username):
    if len(username) > 16 or len(username) <= 0:
        raise Exception("username too long")
    uuid = UUIDFetch(username)

    mostCoins, mostCoinsGame, username = GetMostCoins(uuid)

    text = "**Game:** ```" + str(mostCoinsGame) + "```\n**Amount:** ```" + str(mostCoins) + "```"
    embed = discord.Embed(color=green)
    embed.add_field(name="Most coins for " + username, value=text)
    await ctx.send(embed=embed)


bot.run(TOKEN)
