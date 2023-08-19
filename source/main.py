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


# Taken from stack overflow.

# Function to get rid of milliseconds


def TimeSnip(timeWhen):
    timeWhen = int(str(timeWhen)[0:-3])
    return timeWhen


# Function to fetch the UUID of the passed through user.


@lru_cache(maxsize=250)
def UUIDFetch(username):
    try:
        uuid = requests.get("https://api.mojang.com/users/profiles/minecraft/" + username)
        uuid_scode = uuid.status_code
        uuid = uuid.json()['id']
    except:
        raise Exception("Username is invalid")

    if uuid_scode != 200:
        if uuid_scode == 401 | uuid_scode == 405:
            pass
        else:
            raise Exception("Username is invalid")

    return uuid


# Generates a date.
def DateDisplay(timeVar):
    if timeVar == 0:
        dateData = "Player online or data not found."
    else:
        dateData = datetime.fromtimestamp(int(timeVar / 1000))
    return dateData


# Converts two millisecond values to length between the two in a readable format.
def LengthProcess(startTime, endTime):
    timeLength = endTime - startTime
    if timeLength < 0 or timeLength == 0:
        timeData = "Player online/Game ongoing."
    else:
        millis = int(timeLength)

        seconds = (millis / 1000) % 60
        seconds = int(seconds)

        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)

        hours = (millis / (1000 * 60 * 60)) % 24
        hours = int(hours)

        if hours == 0:
            timeData = "%dm:%ds" % (minutes, seconds)
        else:
            timeData = "%dh:%dm:%ds" % (hours, minutes, seconds)
    return timeData


# Converts games from the API to more readable forms.
def GameReadable(gameType):
    game = ""
    if gameType == "BEDWARS":
        game = "Bedwars"
        pass
    elif gameType == "UHC" or gameType == "No data" or gameType == "N/A":
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
    elif gameType == "WOOL_GAMES":
        game = "Wool Wars"
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
        game = "Arcade"
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
    # Legacy games. - Will likely be removed soon.
    elif gameType == "SKYCLASH":
        game = "Skyclash"
        pass
    elif gameType == "TRUE_COMBAT":
        game = "Crazy walls"
        pass
    return game
