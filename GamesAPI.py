from main import timed_lru_cache, DateDisplay, LengthProcess, GameReadable
import requests
from decouple import config
import datetime

key = config("API_TOKEN")

def GameRequest(UUID):
    TimeNow = str(datetime.datetime.now().strftime("%x %X"))
    try:
        # Fetches recent game data from the Hypixel API.
        game = requests.get("https://api.hypixel.net/recentgames?key="+key+"&uuid="+UUID).json()
    except:
        print(TimeNow+" Something went wrong talking to the recent games API!")
        raise Exception("API appears down")

    r = requests.head("https://api.hypixel.net/recentgames?key="+key+"&uuid="+UUID)
    # Status code check to prevent errors pertaining to not receiving data.
    if r.status_code != 200:
        print(TimeNow+" The API did not respond with a 200 status code, it gave a "+str(r.status_code))
        raise Exception("API appears down")

    GameType, Map, TimeEnded, TimeStarted = GameProcess(game)

    return GameType, Map, TimeEnded, TimeStarted

def GameProcess(game):
    GameType = []
    Map = []
    TimeEnded = []
    TimeStarted = []
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

# main gameslist function. Returns player data
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
