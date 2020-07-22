# Import file used to gather team name information. Passes this along to NHLRoster.py

import json
import ssl
import urllib.request

# Puts team info into list
def get_teams_data(season):
    # Parsing team info json link
    team_info_url = "http://statsapi.web.nhl.com/api/v1/teams?season=" + season
    response = urllib.request.urlopen(team_info_url)
    team_info_data = json.loads(response.read())
    teams = []
    for team in team_info_data['teams']:
        teams.append(team)
    return teams

# Grabbing team names, then sorts by name
def parse_and_sort(teams):
    team_names = []
    for team in teams:
        team_names.append([team['name'], team['id']])
    team_names.sort()
    return team_names

# # Creates new URL based on team ID and pulls stats for the team
def get_stats_data(team_name, teams, season):
    stats = []
    team_exists = False
    for team in teams:
        if (team_name.strip().lower() in team[0].strip().lower()):
            # URL grabs team standings and stats for the given season
            stats_URL = f'http://statsapi.web.nhl.com/api/v1/teams/{team[1]}/stats?season={season}'
            stats_Response = urllib.request.urlopen(stats_URL)
            stats_Data = json.loads(stats_Response.read())
            stats.append(stats_Data)
            team_exists = True
    if team_exists == False:
        return "Not in list"

    return stats

# Adds team name and stats to lists. Displays current record and points. Returns created list
def display_team_stats(stats):
    team_Stats = []
    for stat in stats:
        team_Stats.append([stat['stats'][0]['splits'][0]['stat'], stat['stats'][1]['splits'][0]['team']])

    return team_Stats
