import urllib.request
import json
import time
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

# Use a service account
cred = credentials.Certificate('d4b4f69f6fe6.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection(u'nhl')

season = "20192020"
today = str(datetime.strftime(datetime.now() - timedelta(0), '%Y-%m-%d'))
dday = str(datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d'))
ddayMinus = str(datetime.strftime(datetime.now() - timedelta(2), '%Y-%m-%d'))
epoch_time_start = int(time.time())
static_dict = {8475222: 'Sami Vatanen', 8473463: 'Leo Komarov', 8481554: 'Kaapo Kakko', 8480945: 'Juuso Riikola',
               8471695: 'Tuukka Rask', 8477499: 'Rasmus Ristolainen', 8480035: 'Henri Jokiharju',
               8480045: 'Ukko-Pekka Luukkonen', 8476469: 'Joel Armia', 8477476: 'Artturi Lehkonen',
               8480829: 'Jesperi Kotkaniemi', 8477953: 'Kasperi Kapanen', 8479290: 'Kalle Kossila',
               8475287: 'Erik Haula', 8476882: 'Teuvo Teravainen', 8478427: 'Sebastian Aho',
               8477493: 'Aleksander Barkov', 8479404: 'Henrik Borgstrom', 8476874: 'Olli Maatta',
               8481639: 'Oliwer Kaski', 8470047: 'Valtteri Filppula', 8471469: 'Pekka Rinne',
               8475798: 'Mikael Granlund', 8476447: 'Miikka Salomaki', 8477424: 'Juuse Saros',
               8479976: 'Juuso Valimaki', 8475820: 'Joonas Donskoi', 8478420: 'Mikko Rantanen',
               8475156: 'Mikko Koskinen', 8476440: 'Markus Granlund', 8475825: 'Jani Hakanpaa', 8476902: 'Esa Lindell',
               8478449: 'Roope Hintz', 8480036: 'Miro Heiskanen', 8476914: 'Joonas Korpisalo',
               8478906: 'Markus Nutivaara', 8469459: 'Mikko Koivu', 8480005: 'Kristian Vesalainen',
               8478915: 'Sami Niku', 8479339: 'Patrik Laine', 8481572: 'Ville Heinola', 8481649: 'Joona Luoto',
               8477293: 'Antti Raanta', 8481573: 'Marcus Kallionkieli'}
#static_dict = {8476914: 'Joonas Korpisalo'}
key_list = list(static_dict.keys())

result_dict= {}

def dayResultsToDict(day, key_list):
    """

    :param day:
    :param key_list:
    :return:
    """
    for key in key_list:
        errorFlag = False
        r = urllib.request.urlopen(
            "https://statsapi.web.nhl.com/api/v1/people/{}/stats?stats=gameLog&season={}".format(key, season)).read()
        player = json.loads(r.decode('utf-8'))
        try:
            if day == player["stats"][0]["splits"][0]["date"]:
                playerStats = player["stats"][0]["splits"][0]["stat"]
                playerTeam = player["stats"][0]["splits"][0]["team"]["name"]
                (homeTeam, homeGoals, awayTeam, awayGoals, isOT) = getTeamsAndGoals(player)
                player_dict= {}
                player_dict["id"] = key
                player_dict["goals"] = playerStats["goals"]
                player_dict["assists"] = playerStats["assists"]
                player_dict["timeOnIce"] = playerStats["timeOnIce"]
                player_dict["penaltyMinutes"] = playerStats["penaltyMinutes"]
                player_dict["plusMinus"] = playerStats["plusMinus"]
                player_dict["homeTeam"] = homeTeam
                player_dict["homeGoals"] = homeGoals
                player_dict["awayTeam"] = awayTeam
                player_dict["awayGoals"] = awayGoals
                player_dict["playerTeam"] = playerTeam
                player_dict["isOT"] = isOT
                result_dict[static_dict.get(key)] = player_dict
        except:
            errorFlag = True
        if errorFlag:
            try:
                goalerStats = player["stats"][0]["splits"][0]["stat"]
                goalerTeam = player["stats"][0]["splits"][0]["team"]["name"]
                if day == player["stats"][0]["splits"][0]["date"]:
                    (homeTeam, homeGoals, awayTeam, awayGoals, isOT) = getTeamsAndGoals(player)
                    player_dict = {}
                    player_dict["id"] = key
                    player_dict["goalsAgainst"] = goalerStats["goalsAgainst"]
                    player_dict["shotsAgainst"] = goalerStats["shotsAgainst"]
                    player_dict["savePercentage"] = goalerStats["savePercentage"]
                    player_dict["playerTeam"] = goalerTeam
                    player_dict["homeTeam"] = homeTeam
                    player_dict["homeGoals"] = homeGoals
                    player_dict["awayTeam"] = awayTeam
                    player_dict["awayGoals"] = awayGoals
                    player_dict["isOT"] = isOT
                    result_dict[static_dict.get(key)] = player_dict
            except:
                errorFlag = False
    return result_dict

def getGoals(homeGoals, awayGoals, player):
    """

    :param homeGoals:
    :param awayGoals:
    :param player:
    :return tuple of homeGoals(string), awayGoals(string), isOT(string:
    """
    isOT = "false"
    if homeGoals == awayGoals:
        isOT = "OT"
        if player["stats"][0]["splits"][0]["isOT"]:
            if (player["stats"][0]["splits"][0]["isWin"] & player["stats"][0]["splits"][0]["isHome"]):
                homeGoals += 1
            else:
                awayGoals += 1
        else:
            isOT = "SO"
            if (player["stats"][0]["splits"][0]["isWin"] & player["stats"][0]["splits"][0]["isHome"]):
                homeGoals += 1
            else:
                awayGoals += 1
    return (homeGoals, awayGoals, isOT)

def getTeamsAndGoals(player):
    """

    :param player:
    :return:
    """
    if player["stats"][0]["splits"][0]["isHome"]:
        homeTeam = player["stats"][0]["splits"][0]["team"]["name"]
        awayTeam = player["stats"][0]["splits"][0]["opponent"]["name"]
    else:
        homeTeam = player["stats"][0]["splits"][0]["opponent"]["name"]
        awayTeam = player["stats"][0]["splits"][0]["team"]["name"]
    re = urllib.request.urlopen("https://statsapi.web.nhl.com/api/v1/game/{}/boxscore".format(
        str(player["stats"][0]["splits"][0]["game"]["gamePk"]))).read()
    game = json.loads(re.decode('utf-8'))
    homeGoals = game["teams"]["home"]["teamStats"]["teamSkaterStats"]["goals"]
    awayGoals = game["teams"]["away"]["teamStats"]["teamSkaterStats"]["goals"]
    isOT = "false"
    if homeGoals == awayGoals:
        (homeGoals, awayGoals, isOT) = getGoals(homeGoals, awayGoals, player)
    return (homeTeam, homeGoals, awayTeam, awayGoals, isOT)

print(dday)
result_dict = dayResultsToDict(dday, key_list)
print("It took {} seconds".format(int(time.time() - epoch_time_start)))
final_dict = {"stats":result_dict, "timestamp":datetime.now(), "gameDay":dday}
print(final_dict)
db.collection(u'nhl').document(dday).set(final_dict)

