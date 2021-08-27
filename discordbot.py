import json
from decouple import config
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import discord
from dotenv import load_dotenv
import passwordgen_program as PassGen
from main import UUIDFetch
from GamesAPI import GamesList as GamesAPI
from Session import MainProcess as SessionAPI
import time

load_dotenv()
TOKEN = config("DISCORD_TOKEN")


#Imports Config

def configImport():
    x = open("config.json", "r")
    data = json.load(x)
    x.close()
    return data

Config = configImport()

def get_prefix(bot, msg):
    Set = False
    for y in range(len(Config["guilds"])):
        if int(Config["guilds"][y]["guildID"]) == int(msg.guild.id):
            return str(Config["guilds"][y]["prefix"])
            Set = True
    if Set == False:
        return "$"

def get_pass(bot, ctx):
    Set = False
    for y in range(len(Config["guilds"])):
        if int(Config["guilds"][y]["guildID"]) == int(ctx.guild.id):
            return str(Config["guilds"][y]["pass-command"])
            Set = True
    if Set == False:
        return True

def get_loc(guildid):
    location = 0
    for y in range(len(Config["guilds"])):
        if Config["guilds"][y]["guildID"] == str(guildid):
            location = y
    return location

bot = commands.Bot(command_prefix = get_prefix)
bot.remove_command('help')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("A parameter is missing!")
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Command is on cooldown!")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Sorry about that, you do not have the required permissions to run this!")
    else:
        await ctx.send("Some error happened, printed in console.")
        print(error)

#Notifies when the bot connects
@bot.event
async def on_ready():
    guildIDs = []
    for guild in bot.guilds:
        guildIDs.append(guild.id)
    z = len(guildIDs)
    print("The bot connected to",z,"guild(s).")
    LocationZ = []
    LocationY = []
    IDFoundList = []
    IDLocations = []
    for z in range(z):
        for y in range(len(Config["guilds"])):
            if int(guildIDs[z]) == int(Config["guilds"][y]["guildID"]) and (y not in LocationY or z not in LocationZ):
                LocationY.append(y)
                LocationZ.append(z)
                IDFoundList.append(guildIDs[z])
    for x in range(len(guildIDs)):
        if guildIDs[x] not in IDFoundList:
            IDLocations.append(x)
    if len(IDLocations) != 0:
        for x in range(len(IDLocations)):
            Config["guilds"].append({"guildID" : str(guildIDs[IDLocations[x-1]]), "prefix" : "$", "pass-command" : True, "chat" : "all"})
            ##{"guilds" : []}
        with open("config.json", "w") as configFile:
            json.dump(Config, configFile)

@bot.event
async def on_guild_join(guild):
    InConfig = False
    for x in range(len(Config["guilds"])):
        if int(Config["guilds"][x]["guildID"]) == int(guild.id) and InConfig != True:
            print("Bot joined a guild, however a config is already setup for"+guild.name+". Skipping default config setting")
            InConfig = True
        else:
            pass
    if InConfig == False:
        Config["guilds"].append({"guildID" : str(guild.id), "prefix" : "$", "pass-command" : True, "chat" : "all"})
        print("Bot joined a new server, set default config for "+guild.name)
        with open("config.json", "w") as configFile:
            json.dump(Config, configFile)


@bot.event
async def on_message(message):
    location = 0
    Allowed = False
    if isinstance(message.channel, discord.DMChannel):
        pass
    else:
        for x in range(len(Config["guilds"])):
            if int(Config["guilds"][x]["guildID"]) == int(message.guild.id):
                location = x
        if Config["guilds"][location]["chat"] == "all":
            Allowed = True
        elif Config["guilds"][location]["chat"] == str(message.channel.id):
            Allowed = True
        else:
            return
        if Allowed == True:
            await bot.process_commands(message)
        if message.author != bot.user:
            prefix = get_prefix(bot, message)
        if bot.user.mentioned_in(message):
            await message.channel.send("Hello there! My prefix is "+prefix+" if you have anymore issues. Run: "+prefix+"Help")


@bot.command(name='Pass', aliases=["pass", "password", "generate"])
@commands.cooldown(1, 60, commands.BucketType.user)
async def Pass(ctx, PassLen, PassUni):
    PassComm = get_pass(bot, ctx)
    UnicodeYesNo: ""
    if PassComm == "False":
        await ctx.send("This command is disabled, please change your config or contact the server admin.")
    else:
        Pass = PassGen.PassProcess(int(PassLen), PassUni)
        member = ctx.message.author
        #Checks if the password uses unicode or not
        if PassUni == "1" or PassUni == "yes" or PassUni == "Yes":
            UnicodeYesNo = "does"
        else:
            UnicodeYesNo = "does not"
        channel = await member.create_dm()
        embed = discord.Embed(title="Password", color=0x33ffff)
        embed.add_field(name="Here is your generated password:", value=Pass)
        embed.set_footer(text="Made by RRBuilder#5922. This password is "+PassLen+" characters long and "+UnicodeYesNo+" include unicode. This message will auto delete in 60 seconds :)")
        await channel.send(embed=embed, delete_after=60)
        await ctx.send("Password sent to your DMs :mailbox_with_mail:")


@bot.command(name="help", aliases=["h", "Help", "Useage"])
async def Help(ctx):
    prefix = get_prefix(bot, ctx)
    embed = discord.Embed(title="Help", color=0x33ffff)
    embed.add_field(name="How to use the bot:", value="This bot has a simple function. It is to return last session data from the hypixel API. In order to use the bot you need to use the CMP/Comp command. The usage for this bot is as follows: "+prefix+"CMP Username")
    embed.add_field(name="What is this bot for?", value="This bot will help you find out if someones account got hacked by comparing their last session data to the APIs. If they, for example, say they played Bedwars last yet they played Skywars you will be able to know!")
    embed.add_field(name="Who made this bot?", value="RRBuilder#5922 is the developer for this project. Contact them if you have any issues.")
    await ctx.send(embed=embed)


@bot.command(name='Comp', aliases=["comp", "Compromised", "compromised", "hacked", "Hacked", "CMP", "cmp"])
@commands.cooldown(1, 25, commands.BucketType.user)
async def Comp(ctx, username):
    text = ""
    uuid, success = UUIDFetch(username)
    if success == False:
        await ctx.send("Sorry, but that username is not valid! Make sure you re-enter it")
    else:
        Version, LastLoginRead, LastLogoutRead, UserLang, LastGame, Length, UsernameRead, API_Status, When = SessionAPI(uuid)
        Games, Maps, TimesStarted, TimesEnded, Lens, API_Status = GamesAPI(uuid)
        if API_Status == False:
            await ctx.send("The API appears to be down.")
        else:
            if UsernameRead == "Unknown":
                await ctx.send("This username returns a mainly empty file. This is likely one of those usernames that would return no name on plancke and is a general pain to work with. So it is skipped.")
            else:
                embed = discord.Embed(title="Last session.", color=0x33ffff)
                text = "```\nUUID: "+uuid+"```"+"```\nVersion: "+Version+"```"+"```\nLast Login: "+str(LastLoginRead)+"```"+"```\nLast Logout: "+str(LastLogoutRead)+"```"+"```\nLanguage: "+UserLang+"```"+"```\nLast game type: "+LastGame+"```"+"```\nSession length: "+str(Length)+"```"+"\nThe above happened <t:"+str(When)+":R>"
                embed.add_field(name="Here is the last player session for ```"+UsernameRead+"```", value=text)
                await ctx.send(embed=embed)
                if len(Games) == 0:
                    await ctx.send("No games were detected for the username entered! They likely haven't played any games recently. :)")
                else:
                    embed = discord.Embed(title="Recent games.", color=0x33ffff)
                    for x in range(len(Games)):
                        count = x+1
                        if len(Games) < count:
                            pass
                        else:
                            text = "```\nGameType: "+str(Games[x])+"```"+"```\nMap: "+str(Maps[x])+"```"+"```\nTime Started: "+str(TimesStarted[x])+"```"+"```\nTime Ended: "+str(TimesEnded[x])+"```"+"```\nLength: "+str(Lens[x]+"\n\n```")
                            embed.add_field(name="Game: "+str(count), value=text)
                    await ctx.send(embed=embed)

@bot.command(name="Prefix", aliases=["prefix"])
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 60, commands.BucketType.guild)
async def Prefix(ctx, prefix):
    location = get_loc(ctx.guild.id)
    if prefix == Config["guilds"][location]["prefix"]:
        await ctx.send("Hey! Your prefix is already set to "+prefix)
    else:
        await ctx.send("Set prefix to "+prefix)
        Config["guilds"][location]["prefix"] = prefix
        with open("config.json", "w") as configFile:
            json.dump(Config, configFile)

@bot.command(name="Setchat", aliases=["setac", "setchat", "chat"])
@commands.has_permissions(administrator=True)
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
            with open("config.json", "w") as configFile:
                json.dump(Config, configFile)
    elif option == "this":
        ChannelID = str(ctx.channel.id)
        if Config["guilds"][location]["chat"] == ChannelID:
            await ctx.send("Your bot chat is already set to this channel :)")
        else:
            await ctx.send("Set the bot to only respond in this chat :)")
            Config["guilds"][location]["chat"] = ChannelID
            with open("config.json", "w") as configFile:
                json.dump(Config, configFile)


bot.run(TOKEN)
