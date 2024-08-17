import requests
from bs4 import BeautifulSoup

def get_all_data(url):
  response = requests.get(url)
  response.encoding = response.apparent_encoding
  soup = BeautifulSoup(response.text, 'html.parser')

  tables = soup.find_all("table", {"class": "rosterlisttbl"})
  roster_table = tables[0]
  roster_heads = roster_table.find_all("tr", {"class": "rosterMainHead"})
  roster_rows = roster_table.find_all("tr")
  optioned_table = tables[1]
  optioned_heads = optioned_table.find_all("tr", {"class": "rosterMainHead"})
  optioned_rows = optioned_table.find_all("tr")

  roster_data = get_data(roster_heads, roster_rows)
  optioned_data = get_data(optioned_heads, optioned_rows)
  
  synthetic_data = {"roster": roster_data, "optioned": optioned_data}
  
  return synthetic_data

def get_data(players_table_heads, players_table_rows):
  player_dict = {}   
  position_in_table = []
  for head in players_table_heads:
      position = head.find("th", {"class": "rosterPos"}).get_text()
      position_in_table.append(position)

  row_counter = -1
  current_position_players = []
  
  for row in players_table_rows:
    if row.get("class")[0] == "rosterMainHead":
      row_counter += 1
      if row_counter >= 1:
        player_dict.update({position_in_table[row_counter-1]:current_position_players})
        current_position_players = []
      
    elif row.get("class")[0] == "rosterPlayer":
      number = row.find("td").get_text() # first td
      name = row.find("td", {"class": "rosterRegister"}).get_text().replace("　", "")
      current_position_players.append({"number":number, "name":name})
    
    elif row.get("class")[0] == "rosterRetire":
      continue
     
    else:
      print("Error: Unexpected Class Name -> " + row.get("class")[0])  
      break

  player_dict.update({position_in_table[row_counter]:current_position_players}) # for the last position
  
  return player_dict

