import requests
from main import timed_lru_cache, DateDisplay, LengthProcess, GameReadable, TimeSnip
from decouple import config
import time
import datetime
import logging

key = config("API_TOKEN")

# Fucntion to request the stats of a player.
def StatsRequest(UUID):
    try:
        #fetches the player stats of a player.
        Stats = requests.get("https://api.hypixel.net/player?key="+key+"&uuid="+UUID).json()
    except:
        logging.warning("Something went wrong talking to the session API!")
        raise Exception("API appears down")

    r = requests.head("https://api.hypixel.net/player?key="+key+"&uuid="+UUID)
    if r.status_code != 200:
        logging.warning("The API did not respond with a 200 status code, it gave a "+str(r.status_code))
        raise Exception("API appears down")

    try:
        Username = Stats["player"]["displayname"]
    except:
        raise Exception("Username is unknown")

    try:
        Version = Stats["player"]["mcVersionRp"]
    except:
        Version = "N/A"

    try:
        LastLogin = Stats["player"]["lastLogin"]
    except:
        LastLogin = 0

    try:
        LastLogout = Stats["player"]["lastLogout"]
    except:
        LastLogout = 0

    if LastLogout < LastLogin or LastLogout == LastLogin:
        LastLogout = 0

    try:
        UserLang = Stats["player"]["userLanguage"]
    except:
        UserLang = "N/A"

    try:
        LastGame = Stats["player"]["mostRecentGameType"]
    except:
        LastGame = "N/A"

    return Version, LastLogin, LastLogout, UserLang, LastGame, Username

#Main function used to process the player data
@timed_lru_cache(600)
def MainProcess(UUID):
    Version, LastLogin, LastLogout, UserLang, LastGame, Username = StatsRequest(UUID)

    LastLoginReadable = DateDisplay(LastLogin)
    LastLogoutReadable = DateDisplay(LastLogout)

    if LastLogout < 0 or LastLogout == 0:
        Timestamp = int(time.time())
    else:
        Timestamp = TimeSnip(LastLogout)

    Length = LengthProcess(LastLogin, LastLogout)

    LastGame = GameReadable(LastGame)

    return Version, LastLoginReadable, LastLogoutReadable, UserLang, LastGame, Length, Username, Timestamp
