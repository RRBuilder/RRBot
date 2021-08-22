from main import timed_lru_cache, DateDisplay, LengthProcess, GameReadable
import requests
from decouple import config

key = config("API_TOKEN")

def GameRequest(UUID):
    GameType = []
    Map = []
    TimeEnded = []
    TimeStarted = []
    API_Status = True
    try:
        game = requests.get("https://api.hypixel.net/recentgames?key="+key+"&uuid="+UUID).json()
    except:
        API_Status = False
    if len(game["games"]) == 0:
        pass
    else:
        for x in range(len(game["games"])):
            count = x+1
            if count > 5:
                break
            else:
                try:
                    GameType.append(str(game["games"][x]["gameType"]))
                except:
                    GameType.append(str("No data"))

                try:
                    Map.append(str(game["games"][x]["map"]))
                except:
                    Map.append(str("No data"))

                try:
                    TimeEnded.append(int(game["games"][x]["ended"]))
                except:
                    TimeEnded.append(int(0))

                try:
                    TimeStarted.append(int(game["games"][x]["date"]))
                except:
                    TimeStarted.append(int(0))

    return GameType, Map, TimeEnded, TimeStarted, API_Status

@timed_lru_cache(600)
def GamesList(uuid):
    timeStartedRead = []
    timeEndedRead = []
    timeDifference = []

    gameType, mapPlayed, timeEnded, timeStarted, API_Status = GameRequest(str(uuid))

    for x in range(len(gameType)):
        gameType[x] = GameReadable(gameType[x])

    if API_Status == False:
        for x in range(len(gameType)):
            timeStartedRead.append(int(0))
            timeEndedRead.append(int(0))
            timeDifference.append(int(0))
    else:
        for x in range(len(gameType)):
            timeStartedRead.append(DateDisplay(timeStarted[x]))
            timeEndedRead.append(DateDisplay(timeEnded[x]))
            timeDifference.append(LengthProcess(timeStarted[x], timeEnded[x]))

    return gameType, mapPlayed, timeStartedRead, timeEndedRead, timeDifference, API_Status
