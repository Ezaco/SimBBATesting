import requests
import json

url = 'https://simnba.azurewebsites.net/'

def GetMatchData(home, away):
    res = requests.get(url + 'cbb/match/data/' + home+'/'+away)
    if res.status_code == 200:
        return res.json()
    return False

def SendStats(dto):
    obj = json.dumps(dto, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    r = requests.post(url + 'admin/results/import/', data=obj)
