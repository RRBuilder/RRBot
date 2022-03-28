import requests
from functools import lru_cache, wraps
from datetime import datetime, timedelta

# Tiems LRU cache wrapped function.
def timed_lru_cache(seconds: int, maxsize: int = 128):

    def wrapper_cache(func):

        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)

        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
    #Taken from stack overflow. 

# Function to get rid of miliseconds
def TimeSnip(timewhen):
    timewhen = int(str(timewhen)[0:-3])
    return timewhen

# Function to fetch the UUID of the passed through user.
@lru_cache(maxsize = 250)
def UUIDFetch(username):
    uuid = ""

    uuidurl = f'https://api.mojang.com/users/profiles/minecraft/{username}?'

    uuidget = requests.get(uuidurl)

    r = requests.head(uuidurl)
    if r.status_code != 200:
        success = False
    else:
        uuid = uuidget.json()['id']
        success = True
    return uuid, success

# Generates a date.
def DateDisplay(timevar):
    if timevar == 0:
        DateData = "Player online or data not found."
    else:
        DateData = datetime.fromtimestamp(int(timevar/1000))
    return DateData

# Converts two milisecond values to lenght between the two in a readable format.
def LengthProcess(Start, End):
    Length = End - Start
    if Length < 0 or Length == 0:
        TimeData = "Player online/Game ongoing."
    else:
        Milis = int(Length)

        Seconds = (Milis/1000)%60
        Seconds = int(Seconds)

        Minutes = (Milis/(1000*60))%60
        Minutes = int(Minutes)

        Hours = (Milis/(1000*60*60))%24
        Hours = int(Hours)

        if Hours == 0:
            TimeData = "%dm:%ds" % (Minutes, Seconds)
        else:
            TimeData = "%dh:%dm:%ds" % (Hours, Minutes, Seconds)
    return TimeData

# Converts games from the API to more readable forms.
def GameReadable(gameType):
    game = ""
    if gameType == "BEDWARS":
        game = "Bedwars"
        pass
    elif gameType == "UHC" or gameType == "No data"  or gameType == "N/A":
        game = gameType
        pass
    elif gameType == "SKYWARS":
        game = "Skywars"
        pass
    elif gameType == "BUILD_BATTLE":
        game = "Build battle"
        pass
    elif gameType == "DUELS":
        game = "Duels"
        pass
    elif gameType == "PROTOTYPE":
        game = "Prototype"
        pass
    elif gameType == "HOUSING":
        game = "Housing"
        pass
    elif gameType == "PIT":
        game = "Pit"
        pass
    elif gameType == "MURDER_MYSTERY":
        game = "Murder mystery"
        pass
    elif gameType == "MCGO":
        game = "Cops and crims"
        pass
    elif gameType == "BATTLEGROUND":
        game = "Warlords"
        pass
    elif gameType == "GINGERBREAD":
        game = "Turbo cart racers"
        pass
    elif gameType == "LEGACY":
        game = "Classic games"
        pass
    elif gameType == "SMP":
        game = "Smp"
        pass
    elif gameType == "REPLAY":
        game = "Replay"
        pass
    elif gameType == "SKYBLOCK":
        game = "Skyblock"
        pass
    elif gameType == "SUPER_SMASH":
        game = "Smash heroes"
        pass
    elif gameType == "SPEED_UHC":
        game = "Speed UHC"
        pass
    elif gameType == "WALLS3":
        game = "Megawalls"
        pass
    elif gameType == "ARENA":
        game = "Arena Brawl"
        pass
    elif gameType == "ARCADE":
        game = "Aracade"
        pass
    elif gameType == "VAMPIREZ":
        game = "VampireZ"
        pass
    elif gameType == "TNTGAMES":
        game = "TNT Games"
        pass
    elif gameType == "SURVIVAL_GAMES":
        game = "Blitz SG"
        pass
    elif gameType == "PAINTBALL":
        game = "Paintball"
        pass
    elif gameType == "WALLS":
        game = "The Walls"
        pass
    elif gameType == "QUAKECRAFT":
        game = "Quake"
        pass
    #Legacy games. - Will likely be removed soon.
    elif gameType == "SKYCLASH":
        game = "Skyclash"
        pass
    elif gameType == "TRUE_COMBAT":
        game = "Crazy walls"
        pass
    return game
