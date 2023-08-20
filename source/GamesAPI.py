from main import timed_lru_cache, DateDisplay, LengthProcess, GameReadable
import requests
from decouple import config
import datetime
import logging

key = config("API_TOKEN")


def GameRequest(UUID):
    try:
        # Fetches recent game data from the Hypixel API.
        game = requests.get("https://api.hypixel.net/recentgames?uuid=" + UUID, headers={"API-Key": key})
        game_scode = game.status_code
        game = game.json()
    except:
        logging.warning("Something went wrong talking to the recent games API!")
        raise Exception("API appears down")

    # Status code check to prevent errors pertaining to not receiving data.
    if game_scode != 200:
        logging.warning("The API did not respond with a 200 status code, it gave a " + str(game_scode))
        raise Exception("API appears down")

    gameType, gameMap, timeEnded, timeStarted = GameProcess(game)

    return gameType, gameMap, timeEnded, timeStarted


def GameProcess(game):
    gameType = []
    gameMap = []
    timeEnded = []
    timeStarted = []
    if len(game["games"]) == 0:
        return gameType, gameMap, timeEnded, timeStarted
    else:
        for x in range(len(game["games"])):
            count = x + 1
            if count > 5:
                break
            else:
                try:
                    gameType.append(str(game["games"][x]["gameType"]))
                except:
                    gameType.append(str("No data"))

                try:
                    gameMap.append(str(game["games"][x]["gameMap"]))
                except:
                    gameMap.append(str("No data"))

                try:
                    timeEnded.append(int(game["games"][x]["ended"]))
                except:
                    timeEnded.append(int(0))

                try:
                    timeStarted.append(int(game["games"][x]["date"]))
                except:
                    timeStarted.append(int(0))

        return gameType, gameMap, timeEnded, timeStarted


# main games-list function. Returns player data
@timed_lru_cache(600)
def GamesList(uuid):
    timeStartedRead = []
    timeEndedRead = []
    timeDifference = []

    gameType, mapPlayed, timeEnded, timeStarted = GameRequest(str(uuid))

    for x in range(len(gameType)):
        gameType[x] = GameReadable(gameType[x])

    for x in range(len(gameType)):
        timeStartedRead.append(DateDisplay(timeStarted[x]))
        timeEndedRead.append(DateDisplay(timeEnded[x]))
        timeDifference.append(LengthProcess(timeStarted[x], timeEnded[x]))

    return gameType, mapPlayed, timeStartedRead, timeEndedRead, timeDifference
