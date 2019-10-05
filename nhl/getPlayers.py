import urllib.request
import json
import time
from datetime import datetime, timedelta

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
key_list = list(static_dict.keys())

def printStats(day, key_list):
    for key in key_list:
        errorFlag = False
        r = urllib.request.urlopen("https://statsapi.web.nhl.com/api/v1/people/{}/stats?stats=gameLog&season={}".format(key, season)).read()
        player = json.loads(r.decode('utf-8'))
        try:
            if day == player["stats"][0]["splits"][0]["date"]:
                re = urllib.request.urlopen("https://statsapi.web.nhl.com//api/v1/game/{}/boxscore".format(str(player["stats"][0]["splits"][0]["game"]["gamePk"]))).read()
                game = json.loads(re.decode('utf-8'))
                if player["stats"][0]["splits"][0]["isHome"]:
                    homeTeam = player["stats"][0]["splits"][0]["team"]["name"]
                    awayTeam = player["stats"][0]["splits"][0]["opponent"]["name"]
                else:
                    homeTeam = player["stats"][0]["splits"][0]["opponent"]["name"]
                    awayTeam = player["stats"][0]["splits"][0]["team"]["name"]
                    homeGoals = game["teams"]["home"]["teamStats"]["teamSkaterStats"]["goals"]
                    awayGoals = game["teams"]["away"]["teamStats"]["teamSkaterStats"]["goals"]
                print("{} {}+{}, {}, {}min, +/- {}, {} vs. {}, {}-{}".format(static_dict.get(key),
                                                                 player["stats"][0]["splits"][0]["stat"][
                                                                     "goals"],
                                                                 player["stats"][0]["splits"][0]["stat"][
                                                                     "assists"],
                                                                 player["stats"][0]["splits"][0]["stat"][
                                                                     "timeOnIce"],
                                                                 player["stats"][0]["splits"][0]["stat"][
                                                                     "penaltyMinutes"],
                                                                 player["stats"][0]["splits"][0]["stat"][
                                                                     "plusMinus"],
                                                                 homeTeam, awayTeam, homeGoals, awayGoals))
        except:
            errorFlag = True
        if errorFlag:
            try:
                if day == player["stats"][0]["splits"][0]["date"]:
                    print( "{} {}/{} {}".format(static_dict.get(key),
                                     player["stats"][0]["splits"][0]["stat"]["goalsAgainst"],
                                     player["stats"][0]["splits"][0]["stat"]["shotsAgainst"],
                                     player["stats"][0]["splits"][0]["stat"]))
            except:
                errorFlag = False


# print(today)
# printStats(today, key_list)
print(dday)
printStats(dday, key_list)
print(ddayMinus)
printStats(ddayMinus, key_list)
print("It took {} seconds".format(int(time.time() - epoch_time_start)))

