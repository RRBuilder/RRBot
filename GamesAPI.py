from main import timed_lru_cache, DateDisplay, LengthProcess, GameReadable
import requests
from decouple import config

key = config("API_TOKEN")

def GameRequest(UUID):
    API_Status = True
    try:
        # Fetches recent game data from the Hypixel API.
        game = requests.get("https://api.hypixel.net/recentgames?key="+key+"&uuid="+UUID).json()
    except:
        print("Something went wrong fetching the recent games!")
        game = []
        API_Status = False
        GameType, Map, TimeEnded, TimeStarted = GameProcess(game)
        return GameType, Map, TimeEnded, TimeStarted, API_Status

    r = requests.head("https://api.hypixel.net/recentgames?key="+key+"&uuid="+UUID)
    # Status code check to prevent errors pertaining to not reciving data.
    if r.status_code != 200:
        print("The recent games API did not return a status code of 200, it returned "+str(r.status_code))
        API_Status = False

    GameType, Map, TimeEnded, TimeStarted = GameProcess(game)

    return GameType, Map, TimeEnded, TimeStarted, API_Status

def GameProcess(game):
    GameType = []
    Map = []
    TimeEnded = []
    TimeStarted = []
    try:
        if len(game["games"]) == 0:
            return GameType, Map, TimeEnded, TimeStarted
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

            return GameType, Map, TimeEnded, TimeStarted
    except:
        return GameType, Map, TimeEnded, TimeStarted

# main gmaeslist function. Returns player data
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
