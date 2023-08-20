import requests
from main import timed_lru_cache, DateDisplay, LengthProcess, GameReadable, TimeSnip
from decouple import config
import time
import logging

key = config("API_TOKEN")


# Function to request the stats of a player.
def StatsRequest(UUID):
    try:
        # fetches the player stats of a player.
        stats = requests.get("https://api.hypixel.net/player?uuid=" + UUID, headers={"API-Key": key})
        stats_scode = stats.status_code
        stats = stats.json()
    except:
        logging.warning("Something went wrong talking to the session API!")
        raise Exception("API appears down")

    if stats_scode != 200:
        logging.warning("The API did not respond with a 200 status code, it gave a " + str(stats_scode))
        raise Exception("API appears down")

    try:
        username = stats["player"]["displayname"]
    except:
        raise Exception("username is unknown")

    try:
        version = stats["player"]["mcVersionRp"]
    except:
        version = "N/A"

    try:
        lastLogin = stats["player"]["lastLogin"]
    except:
        lastLogin = 0

    try:
        lastLogout = stats["player"]["lastLogout"]
    except:
        lastLogout = 0

    if lastLogout < lastLogin or lastLogout == lastLogin:
        lastLogout = 0

    try:
        userLanguage = stats["player"]["userLanguage"]
    except:
        userLanguage = "N/A"

    try:
        lastGame = stats["player"]["mostRecentGameType"]
    except:
        lastGame = "N/A"

    return version, lastLogin, lastLogout, userLanguage, lastGame, username


# Main function used to process the player data
@timed_lru_cache(600)
def MainProcess(UUID):
    version, lastLogin, lastLogout, userLanguage, lastGame, username = StatsRequest(UUID)

    lastLoginReadable = DateDisplay(lastLogin)
    lastLogoutReadable = DateDisplay(lastLogout)

    if lastLogout < 0 or lastLogout == 0:
        timestamp = int(time.time())
    else:
        timestamp = TimeSnip(lastLogout)

    length = LengthProcess(lastLogin, lastLogout)

    lastGame = GameReadable(lastGame)

    return version, lastLoginReadable, lastLogoutReadable, userLanguage, lastGame, length, username, timestamp
