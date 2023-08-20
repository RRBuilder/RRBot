import requests
from main import timed_lru_cache
from decouple import config
import datetime

key = config("API_TOKEN")


def StatProcess(UUID):
    timeNow = str(datetime.datetime.now().strftime("%x %X"))
    coinsList = []
    gamesList = ["Arcade", "The Walls", "Mega Walls", "Smash Heroes", "Turbo Cart Racers", "SkyWars", "Paint Ball",
                 "Cops n Crims", "TNT games", "UHC", "Warlords", "Vampire Z", "Blitz SG", "Crazy Walls",
                 "Arena Brawl", "Quakecraft", "Speed UHC", "SkyClash", "Build Battle", "Duels", "Murder Mystery",
                 "Bedwars"]

    try:
        stats = requests.get("https://api.hypixel.net/player?uuid=" + UUID, headers={"API-Key": key})
        stats_scode = stats.status_code
        stats = stats.json()
    except:
        print("Something went wrong talking to the session API!")
        raise Exception("API appears down")

    if stats_scode != 200:
        print(timeNow + " The API did not respond with a 200 status code, it gave a " + str(stats_scode))
        raise Exception("API appears down")

    try:
        username = stats["player"]["displayname"]
    except:
        raise Exception("username is unknown")

    try:
        coinsList.append(int(stats["player"]["stats"]["Arcade"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["Walls"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["Walls3"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["SuperSmash"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["GingerBread"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["SkyWars"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["Paintball"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["MCGO"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["TNTGames"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["UHC"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["Battleground"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["VampireZ"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["HungerGames"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["TrueCombat"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["Arena"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["Quake"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["SpeedUHC"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["SkyClash"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["BuildBattle"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["Duels"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["MurderMystery"]["coins"]))
    except:
        coinsList.append(0)

    try:
        coinsList.append(int(stats["player"]["stats"]["Bedwars"]["coins"]))
    except:
        coinsList.append(0)

    return coinsList, gamesList, username


@timed_lru_cache(600)
def GetMostCoins(UUID):
    coinsList, gamesList, username = StatProcess(UUID)

    coinsListSorted, gamesListSorted = InsertionSort(coinsList, gamesList)

    mostCoins = coinsListSorted[len(coinsListSorted) - 1]
    mostCoinsGame = gamesList[len(coinsListSorted) - 1]
    return mostCoins, mostCoinsGame, username


def InsertionSort(coinsListSorted, gamesList):
    for i in range(1, len(coinsListSorted)):
        valueCoins = coinsListSorted[i]
        valueGames = gamesList[i]
        index = i - 1
        while index >= 0 and valueCoins < coinsListSorted[index]:
            coinsListSorted[index + 1] = coinsListSorted[index]
            gamesList[index + 1] = gamesList[index]
            index -= 1
        coinsListSorted[index + 1] = valueCoins
        gamesList[index + 1] = valueGames

    return coinsListSorted, gamesList
