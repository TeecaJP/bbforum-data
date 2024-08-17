import requests
from bs4 import BeautifulSoup
import json, configparser

import get_players, get_schedule

config = configparser.ConfigParser()
config.read("src/urls.ini", encoding="utf-8")
config_team_urls = config["TEAM-URLS"]
config_schedule_urls = config["SCHEDULE-URLS"]

game_data = get_schedule.get_game_data(config_schedule_urls)

with open("src/game_schedule.json", "w", encoding="utf-8") as f:
    json.dump(game_data, f, ensure_ascii=False, indent=4)

players_data = {}
for team in config_team_urls:
  data = get_players.get_all_data(config_team_urls[team])
  players_data[team] = data
  print("SUCCESS: " + team + "'s data was obtained.")

with open("src/players_by_position.json", "w", encoding="utf-8") as f:
    json.dump(players_data, f, ensure_ascii=False, indent=4)