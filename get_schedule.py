import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_game_data(urls):
  now = datetime.now()
  year = str(now.year)
  month = str(now.month)
  day = str(now.day)
  
  url = urls["head"] + year + urls["middle"] + month.zfill(2) + urls["tail"]
  date_id = "date" + month.zfill(2) + day.zfill(2)
  
  response = requests.get(url)
  response.encoding = response.apparent_encoding
  soup = BeautifulSoup(response.text, 'html.parser')

  table = soup.find("table") # len of table should be 1.
  games = table.find_all("tr", {"id": date_id})
  
  game_list = []
  organized = True
  for game in games:
    home_team = game.find("div", {"class": "team1"})
    if home_team:
      home_team = home_team.get_text()
      away_team = game.find("div", {"class": "team2"}).get_text()
      game_list.append({"home_team": home_team, "away_team": away_team})
    else:
      organized = False
      break

  game_data = {year + month.zfill(2) + day.zfill(2):[ {"organized": organized}, {"game_list": game_list}]}

  return game_data