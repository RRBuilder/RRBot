import requests
from main import timed_lru_cache
from decouple import config
import datetime

key = config("API_TOKEN")

def StatProcess(UUID):
    TimeNow = str(datetime.datetime.now().strftime("%x %X"))
    Coins = []
    Games = ["Arcade", "The Walls", "Mega Walls", "Smash Heroes", "Turbo Cart Racers", "SkyWars", "Paint Ball", "Cops n Crims", "TNT Games", "UHC", "Warlords", "Vampire Z", "Blitz SG", "Crazy Walls", "Arena Brawl", "Quakecraft", "Speed UHC", "SkyClash", "Build Battle", "Duels", "Murder Mystery", "Bedwars"]

    try:
        Stats = requests.get("https://api.hypixel.net/player?key="+key+"&uuid="+UUID).json()
    except:
        print("Something went wrong talking to the session API!")
        raise Exception("API appears down")

    r = requests.head("https://api.hypixel.net/player?key="+key+"&uuid="+UUID)
    if r.status_code != 200:
        print(TimeNow+" The API did not respond with a 200 status code, it gave a "+str(r.status_code))
        raise Exception("API appears down")

    try:
        Username = Stats["player"]["displayname"]
    except:
        raise Exception("Username is unknown")


    try:
        Coins.append(int(Stats["player"]["stats"]["Arcade"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["Walls"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["Walls3"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["SuperSmash"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["GingerBread"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["SkyWars"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["Paintball"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["MCGO"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["TNTGames"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["UHC"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["Battleground"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["VampireZ"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["HungerGames"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["TrueCombat"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["Arena"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["Quake"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["SpeedUHC"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["SkyClash"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["BuildBattle"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["Duels"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["MurderMystery"]["coins"]))
    except:
        Coins.append(0)

    try:
        Coins.append(int(Stats["player"]["stats"]["Bedwars"]["coins"]))
    except:
        Coins.append(0)

    return Coins, Games, Username

@timed_lru_cache(600)
def GetMostCoins(UUID):
    CoinsList, GamesList, Username = StatProcess(UUID)

    CoinsList, Gameslist = InsertionSort(CoinsList, GamesList)

    MostCoins = CoinsList[len(CoinsList)-1]
    MostCoinsGame = GamesList[len(CoinsList)-1]
    return MostCoins, MostCoinsGame, Username

def InsertionSort(CoinsList, GamesList):
    for i in range(1, len(CoinsList)):
        valueCoins = CoinsList[i]
        valueGames = GamesList[i]
        index = i-1
        while index >= 0 and valueCoins < CoinsList[index]:
            CoinsList[index+1] = CoinsList[index]
            GamesList[index+1] = GamesList[index]
            index -= 1
        CoinsList[index+1] = valueCoins
        GamesList[index+1] = valueGames

    return CoinsList, GamesList
