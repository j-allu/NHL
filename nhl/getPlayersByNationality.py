import urllib.request
import json
country="SWE"
url_teams = 'https://statsapi.web.nhl.com/api/v1/teams'
url_roster = "/roster"

req_teams = urllib.request.Request(url_teams)
r = urllib.request.urlopen(req_teams).read()
teams = json.loads(r.decode('utf-8'))

r = urllib.request.urlopen("{}/{}{}".format(url_teams,1,url_roster)).read()
roster = json.loads(r.decode('utf-8'))

dict_players={}
for item in teams['teams']:
     team_id = (item["id"])
     url_roster_test = "{}/{}{}".format(url_teams,team_id,url_roster)
     print(url_roster_test)
     r = urllib.request.urlopen(url_roster_test).read()
     roster = json.loads(r.decode('utf-8'))
     for item2 in roster["roster"]:
         print(item2)
         person_id = item2["person"]["id"]
         person_name = item2["person"]["fullName"]
         re = urllib.request.urlopen("https://statsapi.web.nhl.com/api/v1/people/{}".format(person_id)).read()
         person = json.loads(re.decode('utf-8'))
         nationality = (person["people"][0]["nationality"])
         if nationality == country:
             dict_players[person_id] = person_name
print(dict_players)
with open('{}_players.txt'.format(country), 'w') as f:
    print(dict_players, file=f)

