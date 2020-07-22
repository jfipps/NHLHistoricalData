# Import file used to grab team standings and displays

import json
import ssl
import urllib.request

# Sort key for points
def SortPoints(val):
    return val[1]

# Parsing team info json link
def get_json_data(team_info_url):
    response = urllib.request.urlopen(team_info_url)
    team_info_data = json.loads(response.read())
    return team_info_data

# Puts standings data into list
def get_standings_data(team_info_data):
    teams = []
    for team in team_info_data['records']:
        teams.append(team)
    return teams

# Gets team name and points
def get_team_points(teams):
    first = []
    second = []
    league_counter = 0
    for team in teams:
        division_counter = 0
        first.append(team['teamRecords'])
        while division_counter < (len(first[league_counter])):
            second.append([first[league_counter][division_counter]['team']['name'], first[league_counter][division_counter]['points']])
            division_counter += 1
        league_counter += 1
    second.sort(key=SortPoints, reverse = True)
    return second

# Displays team names and points
def display(sorted_teams):
    for team in sorted_teams:
        print(f"{team[0]} --- Points: {team[1]}")

