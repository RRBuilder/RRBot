import requests
from main import timed_lru_cache, DateDisplay, LengthProcess, GameReadable, TimeSnip
from decouple import config
import time

key = config("API_TOKEN")

# Fucntion to request the stats of a player.
def StatsRequest(UUID):
    API_Status = True
    try:
        #fetches the player stats of a player.
        Stats = requests.get("https://api.hypixel.net/player?key="+key+"&uuid="+UUID).json()
    except:
        API_Status = False
        print("Something went wrong talking to the session API!")

    r = requests.head("https://api.hypixel.net/player?key="+key+"&uuid="+UUID)
    if r.status_code != 200:
        print("The API did not respond with a 200 status code, it gave a "+str(r.status_code))
        API_Status = False

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

    try:
        Username = Stats["player"]["displayname"]
    except:
        Username = "Unknown"

    return Version, LastLogin, LastLogout, UserLang, LastGame, Username, API_Status

#Main function used to process the player data
@timed_lru_cache(600)
def MainProcess(UUID):
    Version, LastLogin, LastLogout, UserLang, LastGame, Username, API_Status = StatsRequest(UUID)
    LastLoginRead = DateDisplay(LastLogin)
    LastLogoutRead = DateDisplay(LastLogout)
    if LastLogout < 0 or LastLogout == 0:
        LastLogout = time.time()
        When = str(LastLogout)[0:-8]
    else:
        When = TimeSnip(LastLogout)
    if LastLogin == 0:
        Length = "Player online/Game ongoing."
    else:
        Length = LengthProcess(LastLogin, LastLogout)
    LastGame = GameReadable(LastGame)
    return Version, LastLoginRead, LastLogoutRead, UserLang, LastGame, Length, Username, API_Status, When
