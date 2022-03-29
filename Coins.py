import requests
from main import timed_lru_cache
from decouple import config

key = config("API_TOKEN")

def StatProcess(UUID):
    Coins = []
    Games = ["Arcade", "The Walls", "Mega Walls", "Smash Heroes", "Turbo Cart Racers", "SkyWars", "Paint Ball", "Cops n Crims", "TNT Games", "UHC", "Warlords", "Vampire Z", "Blitz SG", "Crazy Walls", "Arena Brawl", "Quakecraft", "Speed UHC", "SkyClash", "Build Battle", "Duels", "Murder Mystery", "Bedwars"]
    API_Status = True

    try:
        Stats = requests.get("https://api.hypixel.net/player?key="+key+"&uuid="+UUID).json()
    except:
        API_Status = False
        print("Something went wrong talking to the session API!")

    r = requests.head("https://api.hypixel.net/player?key="+key+"&uuid="+UUID)
    if r.status_code != 200:
        API_Status = False
        print("The API did not respond with a 200 status code, it gave a "+str(r.status_code))

    try:
        Username = Stats["player"]["displayname"]
    except:
        Username = "Unknown"


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

    return Coins, Games, Username, API_Status

@timed_lru_cache(600)
def GetMostCoins(UUID):
    CoinsList, GamesList, Username, API_Status = StatProcess(UUID)

    CoinsList, Gameslist = InsertionSort(CoinsList, GamesList)

    MostCoins = CoinsList[len(CoinsList)-1]
    MostCoinsGame = GamesList[len(CoinsList)-1]
    return MostCoins, MostCoinsGame, Username, API_Status

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
